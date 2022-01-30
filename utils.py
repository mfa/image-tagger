from ruamel.yaml import YAML


def load_tags(fn):
    return yaml.load(open(fn)).get("tags")


def my_yaml():
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.explicit_start = True
    return yaml


yaml = my_yaml()
