from PIL import Image
import json


def load_config(filename):
    with open(filename, "r") as f:
        return json.load(f)

def main():
    # Settings
    config = load_config("config.json")
    num_of_columns = config.get("num_of_columns")
    num_of_slices = config.get("num_of_slices")
    offset = config.get("offset")
    background_location = config.get("background_location")
    mask_location = config.get("mask_location")

    # Set up background
    pattern = Image.open(background_location)
    width = pattern.width
    height = pattern.height

    # Set up mask and scale according to number of slices
    mask = Image.open(mask_location)
    new_height = int((num_of_slices * width * mask.height) / mask.width)
    mask = mask.resize(((num_of_slices) * width, new_height))

    if mask.height > height:
        print("num_of_slices is too high")
        exit()

    def pasteMask(slice):
        # Create transparent mask in shape of background slice
        mask_size = (
            (mask.width * slice) / num_of_slices,
            0,
            (mask.width * (slice + 1)) / num_of_slices,
            mask.height,
        )

        mask_cropped = mask.crop(mask_size)
        result_mask = Image.new("RGBA", (width, mask.height), (255, 255, 255, 0))
        result_mask.paste(mask_cropped, (0, 0))

        # Keep track of left most slice + a little voodoo to make mask centered
        if(num_of_slices % 2 == 0):
            left_slice = int(num_of_columns / 2) + slice - int(num_of_slices/2) + 1
        else:
            left_slice = int(num_of_columns / 2) + slice - int(num_of_slices/2)

        # Crop background to fit the mask
        temp_background = result.crop(
            (
                left_slice * width - (offset * slice),
                int(height / 2 - result_mask.height / 2),
                (left_slice + 1) * width - (offset * slice),
                int(height / 2 + result_mask.height / 2),
            )
        )

        # Paste masked background back to the result background
        for i in range(num_of_columns - left_slice):
            result.paste(
                temp_background,
                (
                    width * (i - 1 + left_slice + 1) - offset * (slice + 1),
                    int(height / 2 - temp_background.height / 2),
                ),
                mask=result_mask,
            )

    result = Image.new(mode="RGB", size=(width * num_of_columns, height), color=0)
    for i in range(num_of_columns):
        result.paste(pattern, (i * pattern.width, 0))

    for i in range(num_of_slices):
        pasteMask(i)

    result.show()

if __name__ == "__main__":
    main()