from PIL import Image


def run(settings):
    def apply_mask_slice(slice, mask, result, bg_width, bg_height):
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

    def make_frame(mask):
        # Set up background
        pattern = Image.open(background_location)
        width = pattern.width
        height = pattern.height

        # Scale mask according to number of slices
        new_height = int((num_of_slices * width * mask.height) / mask.width)
        mask = mask.resize(((num_of_slices) * width, new_height))

        if mask.height > height:
            print("num_of_slices is too high")
            exit()

        result = Image.new(mode="RGB", size=(width * num_of_columns, height), color=0)
        for i in range(num_of_columns):
            result.paste(pattern, (i * pattern.width, 0))

        for i in range(num_of_slices):
            apply_mask_slice(i, mask, result, width, height)

        return result

    def generate_masks():
        masks = []

        mask_gif = Image.open(mask_location)
        if mask_gif.is_animated:
            for i in range(mask_gif.n_frames):
                mask_gif.seek(i)
                masks.append(mask_gif.copy())
        else:
            print("ERROR: Mask is not gif, try turning off gif_mode")
            exit()

        return masks

    def generate_gif(frames):
        print("Saving gif as 'autostereogram_result.gif'\nmight take a while...")
        frames[0].save(
            "autostereogram_result.gif",
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0,
        )

    print("Generating gif...")

    # Settings
    num_of_columns = settings["num_of_columns"]
    num_of_slices = settings["num_of_slices"]
    offset = settings["offset"]
    background_location = settings["background_location"]
    mask_location = settings["mask_location"]

    # Create individual masks
    masks = generate_masks()

    # Create individual stereograms
    frames = []
    for mask in masks:
        frames.append(make_frame(mask))

    # Combine frames
    generate_gif(frames)

    print("DONE")
