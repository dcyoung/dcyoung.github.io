from pathlib import Path
from PIL import Image

CONVERTABLE_IMAGE_EXT = [".jpg", ".jpeg", ".JPG", ".JPEG"]


def main(args) -> None:
    targets = []
    input_paths = [Path(x) for x in args.input]
    for input_path in input_paths:
        if input_path.is_file():
            targets.append(input_path)
        else:
            for ext in CONVERTABLE_IMAGE_EXT:
                targets += input_path.rglob(f"*{ext}")

    for src in targets:
        with Image.open(src) as im:
            im = im.convert("RGB")
            if max(im.size) > args.max_dim:
                scale = args.max_dim / max(im.size)
                new_size = tuple((int(d * scale) for d in im.size))
                im = im.resize(new_size, Image.ANTIALIAS)
                im.save(src)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        action="append",
        required=True,
        help="The path to an input image or directory.",
    )
    parser.add_argument(
        "--max_dim",
        type=int,
        default=1920,
        help="If >0, downsize any oversized images.",
    )
    args, unparsed = parser.parse_known_args()

    main(args)
