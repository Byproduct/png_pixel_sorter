from PIL import Image
import colorsys

# Thresholds
LIGHT_THRESHOLD = 0.99
DARK_THRESHOLD = 0.01
GRAY_THRESHOLD = 0.30
SATURATION_EXCLUDE = 0.30  # Used to exclude colorful pixels from light/dark

input_image = Image.open("paintover.png").convert("RGB")
width, height = input_image.size
pixels = list(input_image.getdata())

light_pixels = []
gray_pixels = []
dark_pixels = []
color_pixels = []

# Classify pixels
for pixel in pixels:
    r, g, b = [x / 255.0 for x in pixel]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    if v > LIGHT_THRESHOLD and s < SATURATION_EXCLUDE:
        light_pixels.append((pixel, v))
    elif v < DARK_THRESHOLD and s < SATURATION_EXCLUDE:
        dark_pixels.append((pixel, v))
    elif s < GRAY_THRESHOLD:
        gray_pixels.append((pixel, v))
    else:
        color_pixels.append((pixel, h, v))

# Sort each group
light_pixels.sort(key=lambda x: -x[1])        # Brightest first
gray_pixels.sort(key=lambda x: -x[1])         # Light to dark
dark_pixels.sort(key=lambda x: x[1])          # Darkest first
color_pixels.sort(key=lambda x: (x[1], x[2])) # Hue, then brightness

sorted_pixels = [p[0] for p in light_pixels + gray_pixels + dark_pixels + color_pixels]
output_image = Image.new("RGB", (width, height))
output_image.putdata(sorted_pixels)
output_image.save("output.png")
