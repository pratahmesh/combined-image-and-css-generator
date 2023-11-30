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

3. **Command Line Usage:**
   ```bash
   python script.py <directory_path> <base_name> <produce_2x>
`
  - <directory_path>: Path to the directory containing images.
  - <base_name>: Base name for the output files.
  - <produce_2x>: 0 for normal image, 1 for 2x image.
 

**Example** 
```bash
python script.py "root/py/test" "output" 1
```
Output:
Combined grid image: output.png
2x Combined grid image: output@2x.png
CSS sprite file: output.css

**It supports .jpg , .png , .jpeg files for now**
