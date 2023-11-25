# Combined Image and CSS Sprite Generator

This Python script is designed to generate a combined image from multiple images and create corresponding CSS sprite classes. It's a handy tool for optimizing web development workflows when dealing with image assets.


## Description
The script performs the following steps:

**Image Combination:**
- Reads all PNG files in the specified directory.
- Calculates the dimensions for the combined grid image.
- Pastes each image onto the combined image in a grid pattern.

**CSS Sprite Generation:**
- Writes common styles for all platforms.
- Creates CSS sprite file with media queries and individual class names.
- Writes platform-specific styles for 2x resolution.
- Writes platform-specific styles for other platforms.
- The CSS sprite file is saved with the name sprite.css.


## Usage

1. **Requirements:**
   - Python 3.x
   - PIL (Python Imaging Library)

2. **Installation:**
   ```bash
   pip install pillow

3. Important note

Just Replace the value of `directory_path` with the actual path of your directory containing Images 
   ```python
   directory_path = "codes/py/testok/"
```
It supports .jpg , .png , .jpeg files for now


