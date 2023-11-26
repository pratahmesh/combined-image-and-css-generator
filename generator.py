from PIL import Image
import os
import math
# Replace "/codes/py/test/" with the actual path
directory_path = "codes/py/testok/"
# Get a list of all PNG files in the directory
png_files = [f for f in os.listdir(directory_path) if f.endswith(".png")]
if not png_files:
    print("No PNG files found in the directory.")
else:
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
# Paste each image onto the combined image in a grid pattern
    current_x = 0
    current_y = 0
    for image in images:
        combined_image.paste(image, (current_x, current_y))
        current_x += cell_width
        if current_x >= grid_width:
            current_x = 0
            current_y += cell_height
    # Save the combined image
    combined_image.save(os.path.join(directory_path, "combined_grid_image.png"))
    print("Combined grid image saved successfully.")

#CSS sprite file
css_sprite_path = os.path.join(directory_path, "sprite.css")
with open(css_sprite_path, "w") as css_file:
    # Write common styles for all platforms
    css_file.write(".sprite-game {\n")
    css_file.write("  display: inline-block;\n")
    css_file.write(f'  background-image: url("combined_grid_image.png");\n')
    css_file.write("  background-size: 416px 384px;\n")
    css_file.write("}\n\n")

    # Create CSS sprite file with media queries and individual class names
    css_file.write(f'@media screen and (-webkit-min-device-pixel-ratio: 1), '
                       f'screen and (-o-min-device-pixel-ratio: 100/100), '
                       f'screen and (min-device-pixel-ratio: 1), '
                       f'screen and (-o-min-device-pixel-ratio: 1/1), '
                       f'screen and (min-resolution: 1dppx) {{\n')
    css_file.write(f'  .sprite-games {{\n')
    css_file.write(f'    background-image: url("combined_grid_image.png");\n')
    css_file.write(f'    background-size: {grid_width}px {grid_height}px;\n')
    css_file.write("  }\n}\n\n")

    # Write platform-specific styles for 2x resolution
    css_file.write("@media screen and (-webkit-min-device-pixel-ratio: 2),\n")
    css_file.write("  screen and (-o-min-device-pixel-ratio: 200/100),\n")
    css_file.write("  screen and (min-device-pixel-ratio: 2),\n")
    css_file.write("  screen and (-o-min-device-pixel-ratio: 2/1),\n")
    css_file.write("  screen and (min-resolution: 2dppx) {\n")
    css_file.write("  .sprite-game {\n")
    css_file.write(f'    background-image: url("combined_grid_image.png");\n')
    css_file.write("  }\n")
    css_file.write("}\n\n")

    # Write platform-specific styles for other platforms
    css_file.write("@media screen and (-webkit-min-device-pixel-ratio: /* platform ratio */),\n")
    css_file.write("  screen and (-o-min-device-pixel-ratio: /* platform ratio/100 */),\n")
    css_file.write("  screen and (min-device-pixel-ratio: /* platform ratio */),\n")
    css_file.write("  screen and (-o-min-device-pixel-ratio: /* platform ratio/1 */),\n")
    css_file.write("  screen and (min-resolution: /* platform resolution */dppx) {\n")
    css_file.write("  .sprite-game {\n")
    css_file.write(f"    background-image: url('../..//images/other-platform.png');\n")
    css_file.write("    /* Additional styles for other platforms */\n")
    css_file.write("  }\n")
    css_file.write("}\n\n")


    for image in images:
        file_name = os.path.splitext(os.path.basename(image.filename))[0]
        css_class = f".sprite-game.{file_name}{{\n"
        css_class += f"  width: {image.width}px;\n"
        css_class += f"  height: {image.height}px;\n"
        css_class += f"  background-position: {-current_x}px {-current_y}px;\n"
        css_class += "}\n\n"
        css_file.write(css_class)

print("CSS sprite file saved successfully.")
