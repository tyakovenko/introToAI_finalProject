import cv2
import numpy as np
from PIL import Image
import os
import csv


def processOneImg (file):
    'return final numpy array for each image'
    img = cv2.imread(file)
    #resize to standard
    img = cv2.resize(img, (224, 224)) #TODO: figure out if this sizing is good enough
    # add Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    # edge detection
    # canny_edges = cv2.Canny(blurred, 100, 200)


    # convert to numpy arrays
    img_array = np.array(blurred)
    # gray scale
    img_gray = np.array(Image.fromarray(img_array).convert("L"))
    # normalize
    img_norm = img_gray / 255.0
    # invert
    img_final = 1 - img_norm

    return np.array(img_final)



def process_folder(input_folder, output_csv, prefix, label):
    records = []

    # Allowed image extensions
    valid_exts = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(valid_exts):
            img_path = os.path.join(input_folder, filename)

            # Run your function
            result = processOneImg(img_path)

            fullName = prefix + filename
            # Include filename if needed
            if isinstance(result, dict):
                result["file"] = fullName
            elif isinstance(result, (list, tuple)):
                result = [fullName] + list(result)
            else:
                result = {"file": fullName, "result": result, "dimensions": result.shape, "label": label}

            records.append(result)

    # Write CSV
    if len(records) > 0:
        # If dicts → header from keys
        if isinstance(records[0], dict):
            fieldnames = list(records[0].keys())
            with open(output_csv, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(records)
        else:
            # If rows are lists → write directly
            with open(output_csv, "w", newline="") as f:
                writer = csv.writer(f)
                for row in records:
                    writer.writerow(row)

    print(f"Saved {len(records)} records to {output_csv}")


process_folder("/home/taya/PycharmProjects/introToAI_finalProject/rain", "rain1.csv", "r", 2)