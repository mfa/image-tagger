import shutil
from pathlib import Path

import click

from utils import yaml


@click.command()
@click.option("--images", type=click.Path(exists=True), help="folder with images")
@click.option("--data", type=click.Path(exists=True), help="folder load tags from")
@click.option(
    "--destination", type=click.Path(exists=True), help="copy images to this folder"
)
@click.option("--tagname", help="tag to filter by")
def main(images, data, destination, tagname):
    fn = Path(data) / "tags.yml"
    if not fn.exists():
        click.echo(f"tags.yml not found in {data}")

    dest = Path(destination)
    (dest / tagname).mkdir(exist_ok=True)
    (dest / f"not_{tagname}").mkdir(exist_ok=True)

    for image_name, tags in yaml.load(open(fn)).items():
        tags = dict(tags)
        folder = tagname if tags.get(tagname) else f"not_{tagname}"
        print(f"{image_name} to {folder}")
        shutil.copy(Path(images) / image_name, dest / folder)


if __name__ == "__main__":
    main()
