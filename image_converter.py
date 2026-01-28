import os
from PIL import Image

def convert_images_to_webp(root_dir, quality=80):
    valid_exts = {".png", ".jpg", ".jpeg"}

    for root, _, files in os.walk(root_dir):
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext in valid_exts:
                input_path = os.path.join(root, filename)
                output_path = os.path.splitext(input_path)[0] + ".webp"

                print(input_path)

                try:
                    with Image.open(input_path) as img:
                        # Convert to RGB if needed (e.g., PNG with alpha)
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")

                        img.save(output_path, "WEBP", quality=quality)
                except Exception as e:
                    print(f"  ❌ Failed to convert: {e}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python imager_converter.py <directory>")
        sys.exit(1)

    convert_images_to_webp(sys.argv[1])
