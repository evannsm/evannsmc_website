#!/usr/bin/env python3
"""
Generate a custom favicon with initials and Puerto Rican flag-inspired design
"""

from PIL import Image, ImageDraw, ImageFont
import math

def create_favicon(size=512):
    """Create a favicon with Puerto Rican flag colors and star-inspired design"""

    # Puerto Rican flag color scheme (light blue variant)
    pr_light_blue = (85, 169, 229)    # Sky/light blue
    pr_white = (255, 255, 255)         # White
    pr_red = (237, 28, 36)             # Red
    pr_black = (0, 0, 0)               # Black for text
    outline_color = (60, 140, 200)     # Darker blue for outlines

    # Create image with transparency
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    center = size // 2

    # First, draw horizontal stripes (5 stripes: red, white, red, white, red)
    stripe_height = size / 5
    for i in range(5):
        y_start = int(i * stripe_height)
        y_end = int((i + 1) * stripe_height)
        stripe_color = pr_red if i % 2 == 0 else pr_white
        draw.rectangle([0, y_start, size, y_end], fill=stripe_color)

    # Create a mask for the star shape
    star_mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(star_mask)

    # Draw a five-pointed star shape on the mask
    star_radius_outer = int(size * 0.48)
    star_radius_inner = int(size * 0.20)

    def get_star_points(cx, cy, radius_outer, radius_inner):
        """Get points for a five-pointed star"""
        points = []
        for i in range(10):
            angle = math.radians(i * 36 - 90)  # Start from top, -90 degrees
            if i % 2 == 0:
                # Outer point
                r = radius_outer
            else:
                # Inner point
                r = radius_inner
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.append((x, y))
        return points

    # Draw filled star on mask
    star_points = get_star_points(center, center, star_radius_outer, star_radius_inner)
    mask_draw.polygon(star_points, fill=255)

    # Apply the star mask to cut out the star shape from the stripes
    img.putalpha(star_mask)

    # Draw star outline
    draw.polygon(star_points, fill=None, outline=outline_color, width=6)

    # Add light blue circular center
    center_circle_radius = int(size * 0.22)
    draw.ellipse(
        [center - center_circle_radius, center - center_circle_radius,
         center + center_circle_radius, center + center_circle_radius],
        fill=pr_light_blue,
        outline=outline_color,
        width=4
    )

    # Add text - initials "EGMC" in black
    try:
        font_size = size // 6
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size // 6)
        except:
            font = ImageFont.load_default()

    text = "EGMC"

    # Get text bounding box for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2

    # Draw text in black
    draw.text(
        (text_x, text_y),
        text,
        fill=pr_black,
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
