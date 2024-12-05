from PIL import Image
import os

def convert_to_png(image_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists
    for image_file in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_file)
        try:
            # Open the image using PIL
            with Image.open(image_path) as img:
                # Save the image as PNG
                output_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + ".png")
                img.save(output_path, format="PNG")
                print(f"Converted {image_file} to {output_path}")
        except Exception as e:
            print(f"Error processing image {image_file}: {e}")

if __name__ == "__main__":
    convert_to_png("Evan", "Evan_png")