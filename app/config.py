import yaml

_config = {}

with open('config.yaml', 'r') as out:

	_config.update(yaml.safe_load(out.read()))


if __name__ == '__main__':
	print(_config)