# -*- coding: utf-8 -*-

import click

from dc2dr import parser


def parse_yml(path):

	run_commands = parser.DockerComposeFileParser(path).get_docker_run_commands()
	for c in run_commands:
		print(c)


@click.command()
@click.argument('f', type=click.Path(exists=True))
def main(f):
	parse_yml(f)


if __name__ == "__main__":
	main()
