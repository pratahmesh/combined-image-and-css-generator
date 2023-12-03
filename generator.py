from PIL import Image
import os
import math
import sys

# Move these declarations outside the function
css_sprite_path = None
combined_image_path = None
combined_image_2x_path = None

def create_combined_image(directory_path, base_name, produce_2x):
    global css_sprite_path, combined_image_path, combined_image_2x_path
    
    png_files = [f for f in os.listdir(directory_path) if f.endswith(".png")]

    if not png_files:
        print("No PNG files found in the directory.")
        return

    images = []
    min_dimension = float('inf')  # Initialize with a large value

    for png_file in png_files:
        file_path = os.path.join(directory_path, png_file)
        image = Image.open(file_path)
        images.append(image)
        
        # Update the minimum dimension
        min_dimension = min(min_dimension, min(image.width, image.height))

    total_images = len(images)
    rows = int(math.sqrt(total_images))
    columns = math.ceil(total_images / rows)

    # Calculate the dimensions of each cell in the grid
    cell_width = min_dimension
    cell_height = min_dimension

    # Create a new blank image with the calculated dimensions for the grid
    grid_width = columns * cell_width
    grid_height = rows * cell_height
    combined_image = Image.new("RGB", (grid_width, grid_height), (255, 255, 255))

    # Paste each image onto the combined image in a grid pattern
    current_x = 0
    current_y = 0
    for image in images:
        # Downscale the image if its dimension is greater than min_dimension
        if image.width > min_dimension or image.height > min_dimension:
            image = image.resize((min_dimension, min_dimension), Image.ANTIALIAS)
        combined_image.paste(image, (current_x, current_y))
        current_x += cell_width
        if current_x >= grid_width:
            current_x = 0
            current_y += cell_height

    # Save the combined image
    combined_image_path = os.path.join(directory_path, f"{base_name}.png")
    combined_image.save(combined_image_path)
    print(f"Combined grid image saved successfully at {combined_image_path}.")

    # Save the 2x image if requested
    if produce_2x:
        combined_image_2x_path = os.path.join(directory_path, f"{base_name}@2x.png")
        combined_image_2x = combined_image.resize(
            (cell_width * columns // 2, cell_height * rows // 2), Image.ANTIALIAS
        )
        combined_image_2x.save(combined_image_2x_path)
        print(f"2x Combined grid image saved successfully at {combined_image_2x_path}.")

    # CSS sprite file
    css_sprite_path = os.path.join(directory_path, f"{base_name}.css")
    with open(css_sprite_path, "w") as css_file:
        # Write common styles for all platforms
        css_file.write(f".sprite-game.{base_name} {{\n")
        css_file.write("    display: inline-block;\n")
        css_file.write(f'    background-image: url("{base_name}.png");\n')
        css_file.write(f'    background-size: {grid_width}px {grid_height}px;\n')
        css_file.write("}\n\n")

        # Create CSS sprite file with media queries and individual class names
        css_file.write(f'@media screen and (-webkit-min-device-pixel-ratio: 1), '
                       f'screen and (-o-min-device-pixel-ratio: 100/100), '
                       f'screen and (min-device-pixel-ratio: 1), '
                       f'screen and (-o-min-device-pixel-ratio: 1/1), '
                       f'screen and (min-resolution: 1dppx) {{\n')
        css_file.write(f'  .sprite-games.{base_name} {{\n')
        css_file.write(f'    background-image: url("{base_name}.png");\n')
        css_file.write(f'    background-size: {grid_width}px {grid_height}px;\n')
        css_file.write("  }\n}\n\n")

        # Write platform-specific styles for 2x resolution
        if produce_2x:
            css_file.write(
                "@media screen and (-webkit-min-device-pixel-ratio: 2),\n")
            css_file.write("  screen and (-o-min-device-pixel-ratio: 200/100),\n")
            css_file.write("  screen and (min-device-pixel-ratio: 2),\n")
            css_file.write("  screen and (-o-min-device-pixel-ratio: 2/1),\n")
            css_file.write("  screen and (min-resolution: 2dppx) {\n")
            css_file.write(f'  .sprite-games.{base_name} {{\n')
            css_file.write(f'    background-image: url("{base_name}@2x.png");\n')
            css_file.write(
                f'    background-size: {2 * grid_width}px {2 * grid_height}px;\n')
            css_file.write("  }\n")
            css_file.write("}\n\n")

        # Write platform-specific styles for other platforms
        css_file.write(
            "@media screen and (-webkit-min-device-pixel-ratio: /* platform ratio */),\n"
        )
        css_file.write(
            "  screen and (-o-min-device-pixel-ratio: /* platform ratio/100 */),\n"
        )
        css_file.write(
            "  screen and (min-device-pixel-ratio: /* platform ratio */),\n")
        css_file.write(
            "  screen and (-o-min-device-pixel-ratio: /* platform ratio/1 */),\n")
        css_file.write(
            "  screen and (min-resolution: /* platform resolution */dppx) {\n")
        css_file.write("  .sprite-game {\n")
        css_file.write(
            f"    background-image: url('../..//images/other-platform.png');\n")
        css_file.write("    /* Additional styles for other platforms */\n")
        css_file.write("  }\n")
        css_file.write("}\n\n")

        for image in images:
            file_name = os.path.splitext(os.path.basename(image.filename))[0]
            css_class = f".sprite-games.{base_name}.{file_name}{{\n"
            css_class += f"  width: {image.width}px;\n"
            css_class += f"  height: {image.height}px;\n"
            css_class += f"  background-position: {-current_x}px {-current_y}px;\n"
            css_class += "}\n\n"
            css_file.write(css_class)

    print(f"CSS sprite file saved successfully at {css_sprite_path}.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <directory_path> <base_name> <produce_2x>")
        sys.exit(1)

    directory_path = sys.argv[1]
    base_name = sys.argv[2]
    produce_2x = bool(int(sys.argv[3]))

    create_combined_image(directory_path, base_name, produce_2x)
