import os
from pathlib import Path
from PIL import Image

CONVERTABLE_IMAGE_EXT = [".png", ".PNG", ".tiff", ".TIFF", ".tif", ".TIF", ".jpeg", ".JPEG", ".JPG"]
def main(args) -> None:
    targets = []
    input_paths = [Path(x) for x in args.input]
    for input_path in input_paths:
        if input_path.is_file():
            targets.append(input_path)
        else:
            for ext in CONVERTABLE_IMAGE_EXT:
                targets += input_path.glob(f"*{ext}")
    
    for src in targets:
        dst = (Path(args.output) if args.output else src.parent) / f"{src.stem}.jpg"
        dst.parent.mkdir(exist_ok=True)
        with Image.open(src) as im:
            im.convert("RGB").save(dst)
        
        if args.delete:
            src.unlink()

    if args.delete_identifiers:
        for input_path in input_paths:
            if input_path.is_dir():
                for fpath in input_path.glob(f"*.Identifier"):
                    fpath.unlink()

if __name__ == "__main__":
    import argparse
    def str2bool(v) -> bool:
        if isinstance(v, bool):
            return v
        if v.lower() in ("yes", "true", "t", "y", "1"):
            return True
        elif v.lower() in ("no", "false", "f", "n", "0"):
            return False
        else:
            raise argparse.ArgumentTypeError("Boolean value expected.")
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        action="append",
        required=True,
        help="The path to an input image or directory.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="If provided, specify a path to an output directory. Otherwise, jpgs will be created alongside the input images.",
    )
    parser.add_argument(
        "--delete",
        type=str2bool,
        default=True,
        help="If True, delete the source images.",
    )
    parser.add_argument(
        "--delete_identifiers",
        type=str2bool,
        default=True,
        help="If True, delete any identifier files.",
    )
    args, unparsed = parser.parse_known_args()

    main(args)
    