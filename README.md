# dc2dr

Convert Docker Compose to Docker Run Commands


* Free software: MIT license


## Features


Takes a docker-compose file, gives back a list of docker run commands.

The supported docker-compose keys are:

  - `depends_on`
  - `links`
  - `ports`
  - `expose`
  - `environment`
  - `command`
  - `image`
  
Added by Xavier Malet
  - `volumes`
  
## Usage (from original doc)

From this dir you can run:

```commandline
python ./dc2dr/cli.py tests/example-compose.yml
```

Or from in a python script:

```python
from dc2dr import parser
path = "path\\to\\docker_compose.yml"
docker_parser = parser.DockerComposeFileParser(path)


# You can pass an .env file to change environment vars on the fly
path_to_envi = "path\\to\\.env"
docker_parser = parser.DockerComposeFileParser(path, path_to_envi)

# get the docker run commands in a list and print them
for i in docker_parser.get_docker_run_commands():
	print(i)
```



## Credits

Project modified from this [github repo](https://github.com/alexhumphreys/dc2dr)