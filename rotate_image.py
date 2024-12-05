from PIL import Image, ExifTags

def correct_image_orientation(image_path):
    # Open the image
    with Image.open(image_path) as img:
        # Check for EXIF data
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            # Get the orientation from the EXIF metadata
            exif = img._getexif()
            if exif is not None and orientation in exif:
                orientation_value = exif[orientation]

                # Rotate the image if necessary
                if orientation_value == 3:
                    img = img.rotate(180, expand=True)
                elif orientation_value == 6:
                    img = img.rotate(270, expand=True)
                elif orientation_value == 8:
                    img = img.rotate(90, expand=True)

        except (AttributeError, KeyError, IndexError):
            # No EXIF data or Orientation tag not found
            pass

        # Save the corrected image (optional)
        corrected_image_path = "corrected_" + image_path
        img.save(corrected_image_path)
        return corrected_image_path

if __name__ == '__main__':
    image_path = "Evan/IMG_2708.JPG"
    corrected_image_path = correct_image_orientation(image_path)
    print(f"Corrected image saved to {corrected_image_path}")