import re
import os


def file_upload(req, folder):
    image_list = req.files.getlist("filename")
    full_file_paths = []
    for image in image_list:
        file_name = image.filename
        full_file_path = os.path.join(folder, file_name)
        image.save(full_file_path)
        full_file_paths.append(full_file_path)

    return full_file_paths


def delete_images(full_file_paths):
    for image in full_file_paths:
        os.remove(image)