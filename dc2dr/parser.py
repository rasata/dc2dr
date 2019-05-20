import yaml
from dc2dr.sorting import sort_service
import pprint

def run_commands(path):
    f = open(path)
    y = yaml.safe_load(f)
    return parse_compose_file(y)


def parse_compose_file(yaml_file):
    services = yaml_file['services']
    sorted_services = sort_service(services)
    parsed_services = []
    # Get standalone containers
    sorted_elements = [list(k)[0] for k in sorted_services ]
    for ident, params in services.items():
        if ident not in sorted_elements:
            parsed_services.append(parse_service(ident,params))
    # Get other containers
    for d in sorted_services:
        for k, v in d.items():
            parsed_services.append(parse_service(k, v))
    
                
    commands = []
    for s in parsed_services:
        commands.append(write_run_command(s))
    return commands
import pprint

def parse_service(name, service):
    docker_args = {'name': name}
    docker_args['image'] = parse_image(service['image'])
    for arg in ['depends_on', 'links', 'ports', 'expose', 'environment', 'command', 'volumes']:
        if arg in service:
            docker_args[arg] = globals()['parse_' + arg](service[arg])
    return docker_args


def write_run_command(service):
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


def parse_image(image):
    return image


def parse_depends_on(deps):
    return to_docker_arg(deps, " --link={0} ")


def parse_links(links):
    return parse_depends_on(links)


def parse_ports(ports):
    return to_docker_arg(ports, " -p {0} ")


def parse_expose(exports):
    return to_docker_arg(exports, " --expose={0} ")


def parse_environment(envs):
    string = ""
    for elt in envs:
        if isinstance(elt, str):
            string += ' -e {} '.format(elt)
        if isinstance(elt, dict):
            for k, v in envs.items():
                string += ' -e {0}="{1}" '.format(k, v)
    return string


def parse_volumes(envs):
    volumes = ""
    for elt in envs:
        volumes += ' -v {} '.format(elt)
    return volumes


def parse_command(command):
    if type(command) is list:
        return ' '.join(command)
    else:
        return command


def to_docker_arg(args, str_format):
    string = ""
    for a in args:
        string += str_format.format(a)
    return string
