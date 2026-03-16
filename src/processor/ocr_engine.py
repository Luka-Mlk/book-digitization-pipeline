from pathlib import Path

import pytesseract


class OCREngine:
    def __init__(self, languages="mkd+chu+bel"):
        """
        languages: 'mkd' (Macedonian), 'chu' (Church Slavonic for old characters),
                   'bel' (Belarusian - often shares old Cyrillic glyph patterns).
        """
        self.lang_config = languages
        # Page Segmentation Mode 3: Fully automatic page segmentation, but no OSD.
        # This is usually best for standard book pages.
        self.custom_config = f"--oem 3 --psm 3"

    def process_image(self, image_path):
        """
        Takes a path to a processed image and returns the recognized text.
        """
        try:
            # We don't need to re-open with OpenCV because Tesseract
            # can handle the file path directly or via PIL/Pillow.
            text = pytesseract.image_to_string(
                str(image_path), lang=self.lang_config, config=self.custom_config
            )
            return text
        except Exception as e:
            print(f"OCR Error on {image_path.name}: {e}")
            return ""
