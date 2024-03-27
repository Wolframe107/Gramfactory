## gramfactory

Gramfactory is a Python script designed to generate autostereograms, commonly known as stereograms.

### How to Use

Configuration settings are adjusted within the `config.json` file. Simply select your desired background and mask, then execute `main.py`. Choose from the provided images in "Backgrounds" or "Masks," or craft your own. It's crucial to note that the mask must be in PNG format and utilize transparency for optimal results.

### Understanding Configuration Variables

- **num_of_columns**: Determines how many times the background slice repeats. Recommended values: 10-15
  
- **num_of_slices**: Specifies the number of slices over which the mask stretches, influencing its scale. Recommended values: 2-5
  
- **offset**: Reflects the depth of the mask, contributing to the 3D effect. However, excessively large values may compromise the illusion. Recommended values: 5-25

- **background_location**: Points to the desired background image slice for the stereogram.

- **mask_location**: Indicates the location of the mask image to be used, with PNG format being the only acceptable option.