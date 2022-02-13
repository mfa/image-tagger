import csv
from collections import defaultdict
from pathlib import Path

import click

from utils import yaml


@click.command()
@click.option(
    "--folder", type=click.Path(exists=True), help="folder with tag.yml files"
)
def main(folder):
    data = defaultdict(dict)
    labellers = []
    for fn in Path(folder).glob("*.yml"):
        labeller_id = fn.name.split("-")[-1].split(".")[0]
        labellers.append(labeller_id)
        for image_name, tags in yaml.load(open(fn)).items():
            for tag, value in tags.items():
                if tag == "blured":
                    tag = "blurred"
                if tag == "blurred":
                    data[image_name][labeller_id] = {tag: value}
    test_files = [
        "G0010979.JPG",
        "G0024366.JPG",
        "G0024374.JPG",
        "G0035338.JPG",
        "G0036079.JPG",
        "G0036150.JPG",
        "G0036961.JPG",
        "G0036970.JPG",
        "G0037131.JPG",
        "G0048173.JPG",
        "G0010980.JPG",
        "G0024305.JPG",
        "G0024699.JPG",
        "G0035344.JPG",
        "G0036295.JPG",
        "G0047578.JPG",
        "G0047667.JPG",
        "G0047850.JPG",
        "G0048119.JPG",
        "G0048219.JPG",
    ]
    # return as csv
    with open(Path(folder) / "comparision.csv", "w", newline="") as csvfile:
        fieldnames = ["image_name", "test"] + [i for i in labellers] + ["agreement"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for image_name, d in sorted(data.items()):
            if d.keys() == set(labellers):
                row = {"image_name": image_name, "test": image_name in test_files}
                for k, v in d.items():
                    for tag, value in v.items():
                        row[k] = tag if value else f"not_{tag}"

                row["agreement"] = len(set([row[i] for i in d.keys()])) == 1

                writer.writerow(row)


if __name__ == "__main__":
    main()
