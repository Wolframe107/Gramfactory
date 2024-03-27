from PIL import Image

pattern = Image.open("ny_bak.jpg")
width = pattern.width
height = pattern.height
col_num = 13
offset = 10
num_of_slices = 3

# Scale mask to fit accordding to number of slices
mask = Image.open("star.png")
new_height = int(float(mask.size[1]) * (width / float(mask.size[0])))
mask = mask.resize(((num_of_slices - 1) * width, (num_of_slices - 1) * new_height))

def pasteMask(slice):
    # Create transparent mask in shape of background
    if slice == 0:    
        mask_size = (0, 0, mask.width/4, mask.height)
    elif slice == 1:
        mask_size = (mask.width/4, 0, (3*mask.width)/4, mask.height)
    elif slice == 2:
        mask_size = ((3*mask.width)/4, 0, mask.width, mask.height)
    
    mask_cropped = mask.crop(mask_size)
    result_mask = Image.new("RGBA", (width, mask.height), (255, 255, 255, 0))

    if(slice == 0):
        result_mask.paste(mask_cropped, (width-mask_cropped.width, 0))
    else:
        result_mask.paste(mask_cropped, (0, 0))
    
    # Crop background to fit mask
    left_column = int(col_num/2) - 1 + slice
    temp_background = result.crop((left_column * width - (offset * slice), int(height/2 - result_mask.height/2), (left_column + 1) * width - (offset * slice), int(height/2 + result_mask.height/2)))

    # Paste unto background
    debug_background = Image.new("RGBA", (result.size), (255,255,255,100))
    for i in range(col_num - left_column):
        #debug_background.paste(temp_background, (width  * (i - 1 + left_column + 1) - offset * (num + 1), int(height/2 - temp_background.height/2)), mask=result_mask)
        result.paste(temp_background, (width  * (i - 1 + left_column + 1) - offset * (slice + 1), int(height/2 - temp_background.height/2)), mask=result_mask)
    #debug_background.show()

result = Image.new(mode="RGB", size=(width*col_num, height), color=0)
for i in range(col_num):
    result.paste(pattern, (i*pattern.width, 0))

for i in range(3):
    pasteMask(i)


result.show()