from PIL import Image
import os
import math
import sys

def create_combined_image(directory_path, base_name, produce_1x):
    # Get a list of all PNG files in the directory
    png_files = [f for f in os.listdir(directory_path) if f.endswith(".png")]
    if not png_files:
        print("No PNG files found in the directory.")
        return

    # Create a list to store Image objects
    images = []
    
    # Open each PNG file and append it to the list
    for png_file in png_files:
        file_path = os.path.join(directory_path, png_file)
        image = Image.open(file_path)
        images.append(image)

    total_images = len(images)
    rows = int(math.sqrt(total_images))
    columns = math.ceil(total_images / rows)

    # Calculate the dimensions of each cell in the grid
    cell_width = max(image.width for image in images)
    cell_height = max(image.height for image in images)

    # Create a new blank image with the calculated dimensions for the grid
    grid_width = columns * cell_width
    grid_height = rows * cell_height
    combined_image = Image.new("RGB", (grid_width, grid_height), (255, 255, 255))

    # Paste each original image onto the combined image in a grid pattern
    current_x = 0
    current_y = 0
    for image in images:
        combined_image.paste(image, (current_x, current_y))
        current_x += cell_width
        if current_x >= grid_width:
            current_x = 0
            current_y += cell_height

    # Save the 2x combined image
    combined_image_path = os.path.join(directory_path, f"{base_name}.png")
    combined_image.save(combined_image_path)
    print(f"2x Combined grid image saved successfully at {combined_image_path}.")

    # Save the 1x image if requested
    if produce_1x:
        downscaled_images = [image.resize((image.width // 2, image.height // 2), Image.ANTIALIAS) for image in images]
        grid_width_1x = columns * (cell_width // 2)
        grid_height_1x = rows * (cell_height // 2)
        combined_image_1x = Image.new("RGB", (grid_width_1x, grid_height_1x), (255, 255, 255))

        # Paste each downscaled image onto the combined image in a grid pattern
        current_x = 0
        current_y = 0
        for downscaled_image in downscaled_images:
            combined_image_1x.paste(downscaled_image, (current_x, current_y))
            current_x += cell_width // 2
            if current_x >= grid_width_1x:
                current_x = 0
                current_y += cell_height // 2

        # Save the 1x combined image
        combined_image_1x_path = os.path.join(directory_path, f"{base_name}@1x.png")
        combined_image_1x.save(combined_image_1x_path)
        print(f"1x Combined grid image saved successfully at {combined_image_1x_path}.")



    css_sprite_path = os.path.join(directory_path, f"{base_name}.css")
    with open(css_sprite_path, "w") as css_file:
      # Write common styles for all platforms
      css_file.write(f".sprite-game.{base_name} {{\n")
      css_file.write("  display: inline-block;\n")
      css_file.write(f'  background-image: url("{base_name}.png");\n')
      css_file.write(f'  background-size: {grid_width}px {grid_height}px;\n')
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

      # Write platform-specific styles for 1x resolution
      if produce_1x:
        css_file.write(
            "@media screen and (-webkit-min-device-pixel-ratio: 2),\n")
        css_file.write("  screen and (-o-min-device-pixel-ratio: 200/100),\n")
        css_file.write("  screen and (min-device-pixel-ratio: 2),\n")
        css_file.write("  screen and (-o-min-device-pixel-ratio: 2/1),\n")
        css_file.write("  screen and (min-resolution: 2dppx) {\n")
        css_file.write(f'  .sprite-games.{base_name} {{\n')
        css_file.write(f'    background-image: url("{base_name}@1x.png");\n')
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
        print("Usage: python script.py <directory_path> <base_name> <produce_1x>")
        sys.exit(1)

    directory_path = sys.argv[1]
    base_name = sys.argv[2]
    produce_1x = bool(int(sys.argv[3]))

    create_combined_image(directory_path, base_name, produce_1x)
