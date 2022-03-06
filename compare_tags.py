import csv
import math
from collections import defaultdict
from pathlib import Path

import click

from utils import yaml


def calc_votes(labellers, row, vote):
    return len([row[i] for i in labellers if row[i] == vote])


@click.command()
@click.option(
    "--folder", type=click.Path(exists=True), help="folder with tags-<name>.yml files"
)
@click.option("--tagname", default="blurred")
def main(folder, tagname):
    data = defaultdict(dict)
    labellers = []
    for fn in Path(folder).glob("*-*.yml"):
        # assumes tags-<name>.yml files, i.e. tags-mfa.yml
        labeller_id = fn.name.split("-")[-1].split(".")[0]
        labellers.append(labeller_id)
        for image_name, tags in yaml.load(open(fn)).items():
            for tag, value in tags.items():
                if tag == tagname:
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

    with open(Path(folder) / "comparision.csv", "w", newline="") as csvfile:
        fieldnames = (
            ["image_name", "test"]
            + [i for i in sorted(labellers)]
            + ["agreement", "majority_value", "majority"]
        )
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for image_name, d in sorted(data.items()):
            # only use images all labellers decided for
            if d.keys() == set(labellers):
                row = {"image_name": image_name, "test": image_name in test_files}
                for k, v in d.items():
                    for tag, value in v.items():
                        row[k] = tag if value else f"not_{tag}"

                row["agreement"] = len(set([row[i] for i in labellers])) == 1

                pos_votes = calc_votes(labellers, row, tagname)
                neg_votes = calc_votes(labellers, row, f"not_{tagname}")
                half = math.ceil(len(labellers) / 2)
                row["majority"] = (pos_votes > half) or (neg_votes > half)
                row["majority_value"] = (
                    tagname if pos_votes > neg_votes else f"not_{tagname}"
                )

                writer.writerow(row)


if __name__ == "__main__":
    main()
