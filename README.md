## Gramfactory

Gramfactory is a Python script designed to generate autostereograms, commonly known as stereograms.
![Example Image](example.png?raw=true "Example Image - Should show one or multiple stars")

### How to Use

You need the image library Pillow for this to work, install it easiest with pip:

```
pip install Pillow
```

Configuration settings are adjusted within the `config.json` file. Simply select your desired background and mask, then execute `main.py`. Choose from the provided images in "Backgrounds" and "Masks," or craft your own. It's crucial to note that the mask must be in PNG format and utilize transparency for optimal results.

### Understanding Configuration Variables

- **num_of_columns**: If anything other than a specified number, determines how many times the background pattern repeats. Else, tries to make final picture around 1920 pixels wide.
  
- **num_of_slices**: Specifies the number of slices over which the mask stretches, influencing its scale. Recommended values: 2-5
  
- **offset**: Reflects the depth of the mask, contributing to the 3D effect. However, excessively large values may compromise the illusion. Recommended values: 5-25

- **background_location**: Points to the desired background image slice for the stereogram.

- **mask_location**: Indicates the location of the mask image to be used, make sure it's PNG.

