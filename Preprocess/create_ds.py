import os
import shutil
import numpy
from PIL import Image

def convert_to_jpeg(image_path):
    img =  numpy.array(Image.open(image_path))
    # img.mode = 'I'
    # img.point(lambda i:i*(1./256)).convert('P') 
    img = img / numpy.amax(img) * 255
    img = img.astype(numpy.uint8)
    img = Image.fromarray(img)
    return img

def create_folder_structure(source_dir, destination_dir):
    for root, dirs, files in os.walk(source_dir):
        for dirname in dirs:
            patient_dir = os.path.join(destination_dir, dirname)
            os.makedirs(patient_dir, exist_ok=True)

        for filename in files:
            if filename.endswith('.tiff'):
                patient_slice_dir = os.path.join(destination_dir, os.path.basename(os.path.dirname(root)))
                os.makedirs(patient_slice_dir, exist_ok=True)
                patient_slice_subdir = os.path.join(patient_slice_dir, os.path.basename(root))
                os.makedirs(patient_slice_subdir, exist_ok=True)
                source_image_path = os.path.join(root, filename)
                print(source_image_path)
                dest_image_path = os.path.join(patient_slice_subdir, filename)
                shutil.copy(source_image_path, dest_image_path)

                # Convert to JPEG
                image = convert_to_jpeg(dest_image_path)
                dest_jpeg_path = os.path.splitext(dest_image_path)[0] + '.jpg'
                image.save(dest_jpeg_path)


def main():
    source_dir = '/home/prosjekt/PerfusionCT/StrokeSUS/ORIGINAL/IMAGE_REGISTERED/'
    destination_dir = '/home/prosjekt/PerfusionCT/StrokeSUS/GAN_project_2023/ORIGINAL_JPEG/'

    create_folder_structure(source_dir, destination_dir)

if __name__ == "__main__":
    main()