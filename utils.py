from ruamel.yaml import YAML


def load_tagset(fn):
    return yaml.load(open(fn)).get("tags")


def load_image_tags(data):
    fn = data / "tags.yml"
    if fn.exists():
        return yaml.load(open(fn))


def save_image_tags(data, image_tags):
    fn = data / "tags.yml"
    yaml.dump(image_tags, open(fn, "w"))


def my_yaml():
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.explicit_start = True
    return yaml


yaml = my_yaml()
