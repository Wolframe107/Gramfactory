from PIL import Image

# Settings
col_num = 15  # Num of repeating columns
offset = 25  # Z-offset for slices
num_of_slices = 9  # Over how many columns does the mask sit

# Set up background
pattern = Image.open("Images/test_bak2.jpg")
width = pattern.width
height = pattern.height

# Set up mask and scale according to number of slices
mask = Image.open("Images/star.png")
new_height = int((num_of_slices * width * mask.height) / mask.width)
mask = mask.resize(((num_of_slices) * width, new_height))

if mask.height > height:
    print("num_of_slices is too high")
    exit()

def pasteMask(slice):
    # Create transparent mask in shape of background
    mask_size = (
        (mask.width * slice) / num_of_slices,
        0,
        (mask.width * (slice + 1)) / num_of_slices,
        mask.height,
    )

    mask_cropped = mask.crop(mask_size)
    result_mask = Image.new("RGBA", (width, mask.height), (255, 255, 255, 0))
    result_mask.paste(mask_cropped, (0, 0))

    # Crop background to fit mask
    left_slice = int(col_num / 2) - 1 + slice
    temp_background = result.crop(
        (
            left_slice * width - (offset * slice),
            int(height / 2 - result_mask.height / 2),
            (left_slice + 1) * width - (offset * slice),
            int(height / 2 + result_mask.height / 2),
        )
    )

    # Paste unto background
    for i in range(col_num - left_slice):
        result.paste(
            temp_background,
            (
                width * (i - 1 + left_slice + 1) - offset * (slice + 1),
                int(height / 2 - temp_background.height / 2),
            ),
            mask=result_mask,
        )


result = Image.new(mode="RGB", size=(width * col_num, height), color=0)
for i in range(col_num):
    result.paste(pattern, (i * pattern.width, 0))

# ändra sen
for i in range(num_of_slices):
    pasteMask(i)


result.show()
