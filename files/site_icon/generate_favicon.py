#!/usr/bin/env python3
"""
Generate a custom favicon with initials and geometric design
"""

from PIL import Image, ImageDraw, ImageFont
import math

def create_favicon(size=512):
    """Create a favicon with geometric design and initials"""

    # Cool color scheme - deep purple/blue gradient with gold accents
    bg_color = (30, 20, 60)  # Deep purple/blue
    accent1 = (100, 60, 180)  # Purple
    accent2 = (60, 180, 200)  # Cyan
    accent3 = (255, 200, 80)  # Gold
    text_color = (255, 255, 255)  # White

    # Create image
    img = Image.new('RGB', (size, size), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw geometric background pattern - rotating squares
    center = size // 2
    num_squares = 6

    for i in range(num_squares):
        square_size = size - (i * size // (num_squares + 2))
        rotation = i * 15  # Rotate each square

        # Interpolate colors
        if i % 3 == 0:
            color = accent1
        elif i % 3 == 1:
            color = accent2
        else:
            color = accent3

        # Make inner squares more transparent by adjusting thickness
        thickness = max(2, 8 - i)

        # Draw rotated square
        half = square_size // 2
        points = [
            (-half, -half),
            (half, -half),
            (half, half),
            (-half, half)
        ]

        # Rotate points
        rad = math.radians(rotation)
        cos_r = math.cos(rad)
        sin_r = math.sin(rad)

        rotated = []
        for x, y in points:
            new_x = x * cos_r - y * sin_r + center
            new_y = x * sin_r + y * cos_r + center
            rotated.append((new_x, new_y))

        # Draw the square outline
        for j in range(4):
            draw.line(
                [rotated[j], rotated[(j + 1) % 4]],
                fill=color,
                width=thickness
            )

    # Add circular accent in the background
    circle_radius = size // 3
    draw.ellipse(
        [center - circle_radius, center - circle_radius,
         center + circle_radius, center + circle_radius],
        fill=None,
        outline=accent3,
        width=3
    )

    # Add text - initials "EGMC"
    # Try to use a nice font, fallback to default if not available
    try:
        # Try common system fonts
        font_size = size // 5
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size // 5)
        except:
            # Fallback to default
            font = ImageFont.load_default()

    # Draw text with shadow for depth
    text = "EGMC"

    # Get text bounding box for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2

    # Draw shadow
    shadow_offset = 3
    draw.text(
        (text_x + shadow_offset, text_y + shadow_offset),
        text,
        fill=(0, 0, 0, 128),
        font=font
    )

    # Draw main text
    draw.text(
        (text_x, text_y),
        text,
        fill=text_color,
        font=font
    )

    return img


if __name__ == "__main__":
    # Generate different sizes
    print("Generating favicon...")

    # High res version
    img_512 = create_favicon(512)
    img_512.save("favicon.png")
    print("✓ Created favicon.png (512x512)")

    # Standard favicon size
    img_32 = img_512.resize((32, 32), Image.Resampling.LANCZOS)
    img_32.save("favicon-32x32.png")
    print("✓ Created favicon-32x32.png")

    # Apple touch icon
    img_180 = img_512.resize((180, 180), Image.Resampling.LANCZOS)
    img_180.save("apple-touch-icon.png")
    print("✓ Created apple-touch-icon.png")

    # Also create ICO format
    try:
        img_512.save(
            "favicon.ico",
            format='ICO',
            sizes=[(16, 16), (32, 32), (48, 48), (64, 64)]
        )
        print("✓ Created favicon.ico (multi-size)")
    except Exception as e:
        print(f"Note: Could not create .ico file: {e}")

    print("\n✓ All done! Your favicon is ready.")
    print("  Main file: favicon.png")
    print("\nTo use it, add this to your _quarto.yml:")
    print('  favicon: favicon.png')
