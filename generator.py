from PIL import Image
import os
import math
import sys


def create_combined_image(directory_path, base_name, produce_2x):
    # Get a list of all PNG files in the directory
    png_files = [f for f in os.listdir(directory_path) if f.endswith(".png")]
    if not png_files:
        print("No PNG files found in the directory.")
        return

    # Create a list to store Image objects
    images_1x = []
    images_2x = []

    # Open each PNG file, downscale a little for 1x, and append it to the list
    for png_file in png_files:
        file_path = os.path.join(directory_path, png_file)
        image = Image.open(file_path)

        # Downscale each image a little for 1x
        downscale_factor_1x = 0.6  # Adjust as needed
        target_size_1x = (
            int(image.width * downscale_factor_1x),
            int(image.height * downscale_factor_1x),
        )
        image_1x = image.resize(target_size_1x, Image.ANTIALIAS)
        images_1x.append(image_1x)

        if produce_2x:
            # Downscale even more for 2x
            downscale_factor_2x = 0.3  # Adjust as needed
            target_size_2x = (
                max(1, int(image.width * downscale_factor_2x)),
                max(1, int(image.height * downscale_factor_2x)),
            )
            image_2x = image.resize(target_size_2x, Image.ANTIALIAS)
            images_2x.append(image_2x)

    # Resize all 2x images to have the same dimensions
    if produce_2x:
        max_width_2x = max(image.width for image in images_2x)
        max_height_2x = max(image.height for image in images_2x)

        images_2x_resized = [
            image.resize((max_width_2x, max_height_2x), Image.ANTIALIAS)
            for image in images_2x
        ]

    total_images = len(images_1x)
    rows = int(math.sqrt(total_images))
    columns = math.ceil(total_images / rows)

    # Calculate the dimensions of each cell in the grid for 1x
    cell_width_1x = max(image.width for image in images_1x)
    cell_height_1x = max(image.height for image in images_1x)

    # Create a new blank image with the calculated dimensions for the 1x grid
    grid_width_1x = columns * cell_width_1x
    grid_height_1x = rows * cell_height_1x
    combined_image_1x = Image.new("RGB", (grid_width_1x, grid_height_1x), (255, 255, 255))

    # Paste each downscale 1x image onto the combined 1x image in a grid pattern
    current_x = 0
    current_y = 0
    for image_1x in images_1x:
        combined_image_1x.paste(image_1x, (current_x, current_y))
        current_x += cell_width_1x
        if current_x >= grid_width_1x:
            current_x = 0
            current_y += cell_height_1x

    # Save the combined 1x image
    combined_image_1x_path = os.path.join(directory_path, f"{base_name}.png")
    combined_image_1x.save(combined_image_1x_path)
    print(f"Combined grid image saved successfully at {combined_image_1x_path}.")

    # Save the 2x image if requested
    if produce_2x:
        # Calculate the dimensions of each cell in the grid for 2x
        cell_width_2x = max_width_2x
        cell_height_2x = max_height_2x

        # Create a new blank image with the calculated dimensions for the 2x grid
        grid_width_2x = columns * cell_width_2x
        grid_height_2x = rows * cell_height_2x
        combined_image_2x = Image.new("RGB", (grid_width_2x, grid_height_2x), (255, 255, 255))

        # Paste each resized 2x image onto the combined 2x image in a grid pattern
        current_x = 0
        current_y = 0
        for image_2x in images_2x_resized:
            combined_image_2x.paste(image_2x, (current_x, current_y))
            current_x += cell_width_2x
            if current_x >= grid_width_2x:
                current_x = 0
                current_y += cell_height_2x

        # Save the 2x combined image
        combined_image_2x_path = os.path.join(directory_path, f"{base_name}@2x.png")
        combined_image_2x.save(combined_image_2x_path)
        print(f"2x Combined grid image saved successfully at {combined_image_2x_path}.")

    # CSS sprite file
    css_sprite_path = os.path.join(directory_path, f"{base_name}.css")
    with open(css_sprite_path, "w") as css_file:
        # Write common styles for all platforms
        css_file.write(f".sprite-game.{base_name} {{\n")
        css_file.write("    display: inline-block;\n")
        css_file.write(f'    background-image: url("{base_name}.png");\n')
        css_file.write(f'    background-size: {grid_width_1x}px {grid_height_1x}px;\n')
        css_file.write("}\n\n")

        # Create CSS sprite file with media queries and individual class names
        css_file.write(f'@media screen and (-webkit-min-device-pixel-ratio: 1), '
                      f'screen and (-o-min-device-pixel-ratio: 100/100), '
                      f'screen and (min-device-pixel-ratio: 1), '
                      f'screen and (-o-min-device-pixel-ratio: 1/1), '
                      f'screen and (min-resolution: 1dppx) {{\n')
        css_file.write(f'  .sprite-games.{base_name} {{\n')
        css_file.write(f'    background-image: url("{base_name}.png");\n')
        css_file.write(f'    background-size: {grid_width_1x}px {grid_height_1x}px;\n')
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
                f'    background-size: {2 * grid_width_1x}px {2 * grid_height_1x}px;\n')
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

        for image_1x in images_1x:
            file_name = os.path.splitext(os.path.basename(png_files[images_1x.index(image_1x)]))[0]
            css_class = f".sprite-games.{base_name}.{file_name}{{\n"
            css_class += f"  width: {image_1x.width}px;\n"
            css_class += f"  height: {image_1x.height}px;\n"
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
