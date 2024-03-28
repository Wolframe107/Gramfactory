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
    video_mode = config.get("video_mode")
    save_image = config.get("save_image")

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

    def make_frame(frame_num, video_mode):
        # Set up background
        pattern = Image.open(background_location)
        width = pattern.width
        height = pattern.height

        # Set up mask and scale according to number of slices
        if video_mode:
            mask = Image.open("Masks/Used_mask/video_frame_" + str(frame_num) + ".png")
        else:
            mask = Image.open(mask_location)

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

        if video_mode:
            result.save("Output/output_frame_" + str(frame_num) + ".jpg")
        else:
            result.show()
            if save_image:
                result.save("Stereogram.jpg")

    def generate_masks():
        mask_gif = Image.open(mask_location)
        if mask_gif.is_animated:
            for i in range(mask_gif.n_frames):
                mask_gif.seek(i)
                current_frame = mask_gif.copy()
                current_frame.save("Masks/Used_mask/video_frame_" + str(i) + ".png")
        return mask_gif.n_frames

    def generate_gif(num_of_frames):
        frames = []

        for i in range(num_of_frames):
            frame = Image.open("Output/output_frame_" + str(i) + ".jpg")
            frames.append(frame)

        frames[0].save(
            "Output/Stereogram.gif",
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0,
        )

    if video_mode:
        print("Generating masks from GIF")
        num_of_frames = generate_masks()
    else:
        num_of_frames = 1

    for i in range(num_of_frames):
        make_frame(i, video_mode)

    if video_mode:
        generate_gif(num_of_frames)
        print("Process completed\nGIF has been created")
    else:
        print("Process completed\nStereogram has been created")


if __name__ == "__main__":
    main()
