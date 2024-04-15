import json
import image_generator
import gif_generator
from PIL import Image


def load_config(filename):
    with open(filename, "r") as f:
        return json.load(f)


def main():
    settings = load_config("config.json")

    if Image.open(settings["mask_location"]).is_animated:
        gif_generator.run(settings)
    else:
        image_generator.run(settings)


if __name__ == "__main__":
    main()
