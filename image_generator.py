from PIL import Image


def run(settings):
    def apply_mask_slice(slice, mask, result, bg_width, bg_height, num_of_columns):
        # Create transparent mask in shape of background slice
        mask_size = (
            (mask.width * slice) / num_of_slices,
            0,
            (mask.width * (slice + 1)) / num_of_slices,
            mask.height,
        )

        mask_cropped = mask.crop(mask_size)
        result_mask = Image.new("RGBA", (bg_width, mask.height), (255, 255, 255, 0))
        result_mask.paste(mask_cropped, (0, 0))

        # Keep track of left most slice + a little voodoo to make mask centered
        if num_of_slices % 2 == 0:
            left_slice = int(num_of_columns / 2) + slice - int(num_of_slices / 2) + 1
        else:
            left_slice = int(num_of_columns / 2) + slice - int(num_of_slices / 2)

        # Crop background to fit the mask
        temp_background = result.crop(
            (
                left_slice * bg_width - (offset * slice),
                int(bg_height / 2 - result_mask.height / 2),
                (left_slice + 1) * bg_width - (offset * slice),
                int(bg_height / 2 + result_mask.height / 2),
            )
        )

        # Paste masked background back to the result background
        for i in range(num_of_columns - left_slice):
            result.paste(
                temp_background,
                (
                    bg_width * (i - 1 + left_slice + 1) - offset * (slice + 1),
                    int(bg_height / 2 - temp_background.height / 2),
                ),
                mask=result_mask,
            )

    def make_frame():
        # Set up background
        try:
            pattern = Image.open(background_location)
        except:
            print(
                "ERROR: That background doesn't seem to exist :(\nPlease double check the path\nTerminating"
            )
            exit()

        width = pattern.width
        height = pattern.height

        if settings["num_of_columns"] == "Auto":
            num_of_columns = round((1920 * (height / 1080)) / width)
        else:
            num_of_columns = settings["num_of_columns"]

        # Set up mask and scale according to number of slices
        try:
            mask = Image.open(mask_location)
        except:
            print(
                "ERROR: That mask doesn't seem to exist :(\nPlease double check the path\nTerminating"
            )
            exit()

        new_height = int((num_of_slices * width * mask.height) / mask.width)
        mask = mask.resize(((num_of_slices) * width, new_height))

        if mask.height > height:
            print("num_of_slices is too high")
            exit()

        result = Image.new(mode="RGB", size=(width * num_of_columns, height), color=0)
        for i in range(num_of_columns):
            result.paste(pattern, (i * pattern.width, 0))

        for i in range(num_of_slices):
            apply_mask_slice(i, mask, result, width, height, num_of_columns)

        return result

    print("Generating image...")

    # Settings
    num_of_columns = settings["num_of_columns"]
    num_of_slices = settings["num_of_slices"]
    offset = settings["offset"]
    background_location = settings["background_location"]
    mask_location = settings["mask_location"]

    result_image = make_frame()
    print("Complete")

    print("Saving image as 'autostereogram_result.png'")
    result_image.save("autostereogram_result.png")

    result_image.show()

    print("DONE")
