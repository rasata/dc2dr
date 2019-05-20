import yaml

from dc2dr.sorting import sort_service


class DockerComposeFileParser(object):
	
	def __init__(self, docker_compose_path: str) -> None:
		
		self._dc_path = docker_compose_path
		self._docker_file = open(self._dc_path)
		self._dc_yaml_file = yaml.safe_load(self._docker_file)
		self.parsers = {'depends_on': self._parse_depends_on,
		                'links': self._parse_links,
		                'ports': self._parse_ports,
		                'expose': self._parse_expose,
		                'environment': self._parse_environment,
		                'command': self._parse_command,
		                'volumes': self._parse_volumes}
	
	def get_docker_run_commands(self) -> list:
		"""
		Get docker run commands by parsing the docker-compose.yml file
		:return: list of docker run commands
		"""
		return [self._create_docker_run_command(s) for s in self._get_list_of_services()]
	
	def _get_list_of_services(self) -> list:
		"""
		get a list of services present in the docker-compose file
		:return:
		"""
		services = self._dc_yaml_file['services']
		parsed_services = []
		# TODO : Remove that...
		sorted_services = sort_service(services)
		# Get standalone containers
		sorted_elements = [list(k)[0] for k in sorted_services]
		for ident, params in services.items():
			if ident not in sorted_elements:
				parsed_services.append(self._parse_service(ident, params))
		# Get other containers
		for d in sorted_services:
			for k, v in d.items():
				parsed_services.append(self._parse_service(k, v))
		return parsed_services
	
	def _create_docker_run_command(self, service: dict) -> str:
		"""
		Create a docker run command by reading a service dict
		:param service: service to parse
		:type service: dict
		:return: the docker run command
		:rtype: str
		"""
		command = ""
		prefix = "docker run -d --name={0} ".format(service['name'])
		command += prefix
		for arg in ['depends_on', 'links', 'ports', 'expose', 'environment', 'volumes']:
			if arg in service:
				command += service[arg]
		command += service['image']
		if 'command' in service:
			command += ' {0}'.format(service['command'])
		return command
	
	def _parse_service(self, service_name, service_params):
		docker_args = {'name': service_name, 'image': service_params['image']}
		
		service_arguments = [args for args in service_params if args in
		                     ['depends_on', 'links', 'ports', 'expose', 'environment', 'command', 'volumes']]
		
		for arg in service_arguments:
			docker_args[arg] = self.parsers[arg](service_params[arg])
		return docker_args
	
	def _parse_depends_on(self, deps):
		return self._to_docker_arg(deps, " --link={0} ")
	
	def _parse_links(self, links):
		return self._parse_depends_on(links)
	
	def _parse_ports(self, ports):
		return self._to_docker_arg(ports, " -p {0} ")
	
	def _parse_expose(self, exports):
		return self._to_docker_arg(exports, " --expose={0} ")
	
	def _parse_environment(self, envs):
		string = ""
		for elt in envs:
			if isinstance(elt, str):
				string += ' -e {} '.format(elt)
			if isinstance(elt, dict):
				for k, v in envs.items():
					string += ' -e {0}="{1}" '.format(k, v)
		return string
	
	def _parse_volumes(self, envs):
		volumes = ""
		for elt in envs:
			volumes += ' -v {} '.format(elt)
		return volumes
	
	def _parse_command(self, command):
		if type(command) is list:
			return ' '.join(command)
		else:
			return command
	
	def _to_docker_arg(self, args, str_format):
		string = ""
		for a in args:
			string += str_format.format(a)
		return string
