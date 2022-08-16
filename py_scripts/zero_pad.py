import os
from pathlib import Path
from PIL import Image

CONVERTABLE_IMAGE_EXT = [".jpg", ".jpeg", ".JPG", ".JPEG"]


def guarantee_n_digit_zero_pad(i: int, n: int = 4) -> str:
    zero_pad = max(0, n - len(str(i)))
    return "0" * zero_pad + str(i)


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
        try:
            numeric_value = int(src.stem)
            dst = (
                src.parent
                / f"{guarantee_n_digit_zero_pad(numeric_value, n=args.n)}{src.suffix}"
            )
            os.rename(src, dst)
        except Exception:
            print(f"Failed for: {src}")


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
        "--n", type=int, default=4, help="Number of zeros",
    )
    args, unparsed = parser.parse_known_args()

    main(args)
