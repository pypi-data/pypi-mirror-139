"""
Runs imgd with student output against expected output
and produces images showing the pixel differences.

Only works on EdStem!

Example usage:
   > from cse_163_utils import run_imgd
   >
   > def main():
   >     print("Running all functions in your main method."
   >           " This may take a minute or so:")
   >     hw5.main()
   >     print()
   >     for plot_name in PLOTS:
   >         run_imgd(f"expected/{plot_name}", plot_name)

Author: Ryan Siu
"""

import os
import subprocess

from typing import List

from PIL import ImageDraw, Image, ImageFont


IMGD_ARGS = [
    "--pixel-correct-threshold", "0.985",
    "--diff-mode", "always",
    "--correct-colour", "ffffff",
]


def no_diffs():
    """
    Replaces a blank generated diff image with one that has
    "No Differences Found" written on it
    """
    msg = "No Differences Found"
    ttf = "LiberationSans-Bold.ttf"

    image = Image.open("diff.png")
    width, height = image.size

    fontsize = 1
    font = ImageFont.truetype(ttf, fontsize)
    fraction = 0.5

    while font.getsize(msg)[0] < fraction * width:
        # iterate until the text size is just larger
        #    than the criteria
        fontsize += 1
        font = ImageFont.truetype(ttf, fontsize)

    ImageDraw.Draw(image).text((width / 4, height / 2),
                               msg, font=font, fill=(0, 0, 0))
    image.save("diff.png")


def run_imgd(expected: str, actual: str, args: List[str]=IMGD_ARGS):
    """
    Runs imgd of student output against expected.
    Produces diff image only if both student and expected output exist.
    """
    if not os.path.exists(actual):
        print(f"Could not find: {actual}. Be sure you're calling all plot"
              " functions in main")
        print()
    elif not os.path.exists(expected):
        print(f"Could not find: {expected}")
        print()
    else:
        print(f"Running image comparison tool on {actual}...")

        # Run's EdStem's imgd program. Outputs the differences to diff.png
        output = subprocess.run(["/opt/ed/bin/imgd", expected, actual]
                                + args, capture_output=True)
        output = output.stdout.decode("utf-8")

        # Report no diffs if it is a perfect match
        if "100.00%" in output:
            no_diffs()

        # If it was successfull, rename the filename to something more descriptive
        if "Your image's" not in output:  # !dimensions mismatch
            new_name = os.path.splitext(actual)[0]
            os.rename("diff.png", f"{new_name}_diff.png")
        print(output)
    print()


if __name__ == "__main__":
    main()
