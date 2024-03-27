
# FÖR ATT SKAPA EN MASK OCH DET
foreground = Image.open("star.png").convert("RGBA")  # Convert to grayscale
background = Image.open("test_bak.jpg").convert("RGBA")
# Resize the foreground image to match the background image size
result = Image.new("RGBA", (1000,1000), (255, 255, 255, 255))
# Paste the background onto the result image using the foreground as a mask
foreground = foreground.resize((background.width, foreground.height), Image.ANTIALIAS)
background = background.crop((0, int(background.height/2 - foreground.height / 2), background.width, int(background.height/2 + foreground.height / 2)))
# Create a new image with the same size as the background and fill it with white
result.paste(background, (0, 0), mask=foreground)
# Save the resulting image
result.show()

""" 
#background.show()
# Mask 1
# Gör ny mask
mask = Image.open("star.png")
mask_cropped = mask.crop((0, 0, mask.width/4, mask.height))
result_mask = Image.new("RGBA", (width,mask.height), (255, 255, 255, 0))
result_mask.paste(mask_cropped, (width-mask_cropped.width, 0))

# Croppa rätt parti
temp_background = background.crop((6 * width, int(height/2 - result_mask.height/2), 7 * width, int(height/2 + result_mask.height/2)))
# Sätt ihop
result = Image.new("RGBA", (result_mask.size), (255, 255, 255, 0))
result.paste(temp_background, (0, 0), mask=result_mask)

#test_background = Image.new("RGBA", (background.size), (255,255,255,100))
for i in range(9):
    #test_background.paste(temp_background, (width  * (i+7) - 15, int(height/2 - temp_background.height/2)), mask=result_mask)
    background.paste(temp_background, (width  * (i+7) - 5, int(height/2 - temp_background.height/2)), mask=result_mask)
#test_background.show()

# Mask 2!
mask = Image.open("star.png")
mask_cropped = mask.crop((mask.width/4, 0, (3*mask.width)/4, mask.height))
result_mask = Image.new("RGBA", (width,mask.height), (255, 255, 255, 0))
result_mask.paste(mask_cropped, (0, 0))

# Croppa rätt parti
temp_background = background.crop((7 * width - 5, int(height/2 - result_mask.height/2), 8 * width - 5, int(height/2 + result_mask.height/2)))
# Sätt ihop
result = Image.new("RGBA", (result_mask.size), (255, 255, 255, 0))
result.paste(temp_background, (0, 0), mask=result_mask)

test_background = Image.new("RGBA", (background.size), (255,255,255,100))
for i in range(8):
    test_background.paste(temp_background, (width  * (i+8) - 10, int(height/2 - temp_background.height/2)), mask=result_mask)
    background.paste(temp_background, (width  * (i+8) - 10, int(height/2 - temp_background.height/2)), mask=result_mask)
#test_background.show()

# Mask 3!

mask_cropped = mask.crop(((3*mask.width)/4, 0, mask.width, mask.height))
result_mask = Image.new("RGBA", (width,mask.height), (255, 255, 255, 100))
result_mask.paste(mask_cropped, (0, 0))
#result_mask.show()

# Croppa rätt parti
temp_background = background.crop((8 * width - 10, int(height/2 - result_mask.height/2), 9 * width - 10, int(height/2 + result_mask.height/2)))
# Sätt ihop
result = Image.new("RGBA", (result_mask.size), (255, 255, 255, 10))
result.paste(temp_background, (0, 0), mask=result_mask)
#result.show()

test_background = Image.new("RGBA", (background.size), (255,255,255,100))
for i in range(7):
    test_background.paste(temp_background, (width  * (i+9) - 15, int(height/2 - temp_background.height/2)), mask=result_mask)
    width  * (i + left_column + 1) - 5 - 5 * num
    
    width * (i+7) - 5
    width * (i+8) - 10
    width * (i+9) - 15
    background.paste(temp_background, (width  * (i+9) - 15, int(height/2 - temp_background.height/2)), mask=result_mask)
background.show() """