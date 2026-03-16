import cv2
import numpy as np


class ImageFilter:
    def __init__(self, scale_factor=2):
        self.scale_factor = scale_factor

    def process(self, image_path):
        # Load image as grayscale
        img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)

        if img is None:
            raise FileNotFoundError(f"Could not open image: {image_path}")

        # Fix: Ensure dimensions are explicitly integers and dsize is passed correctly
        h, w = img.shape[:2]
        new_size = (int(w * self.scale_factor), int(h * self.scale_factor))

        # Explicitly naming the dsize argument to satisfy the overload
        img = cv2.resize(src=img, dsize=new_size, interpolation=cv2.INTER_CUBIC)

        # Thresholding
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Morphological thinning to separate touching characters
        kernel = np.ones((1, 2), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)

        return img

    def save(self, img_array, output_path):
        cv2.imwrite(str(output_path), img_array)
