from pathlib import Path

from processor.image_filter import ImageFilter
from processor.ocr_engine import OCREngine  # New Import
from utils.config import PROC_DIR, RAW_DIR, TXT_DIR  # Added TXT_DIR


def main():
    # 1. Initialize our tools
    filt = ImageFilter(scale_factor=2)
    # Using mkd+chu to handle both modern and archaic Cyrillic
    engine = OCREngine(languages="mkd+chu")

    # 2. Collect all images
    image_paths = list(RAW_DIR.rglob("*.png"))

    if not image_paths:
        print(f"No images found in {RAW_DIR}. Check your scraper output.")
        return

    print(f"Starting pipeline for {len(image_paths)} images...")

    for img_path in image_paths:
        # Create mirrored paths for both processed images and text results
        relative_path = img_path.relative_to(RAW_DIR)

        # Image output path (e.g., data/processed_screenshots/book/page.png)
        img_output_path = PROC_DIR / relative_path

        # Text output path (e.g., data/text_output/book/page.txt)
        txt_output_path = TXT_DIR / relative_path.with_suffix(".txt")

        # Ensure directories exist
        img_output_path.parent.mkdir(parents=True, exist_ok=True)
        txt_output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # --- Step A: Image Filtering ---
            # This prepares the 'visual' for the OCR
            processed_img = filt.process(img_path)
            filt.save(processed_img, img_output_path)

            # --- Step B: OCR Extraction ---
            # We run the engine on the ALREADY processed image
            text_content = engine.process_image(img_output_path)

            # --- Step C: Save Results ---
            with open(txt_output_path, "w", encoding="utf-8") as f:
                f.write(text_content)

            print(f"✓ Success: {relative_path}")

        except Exception as e:
            print(f"✗ Failed {relative_path}: {e}")

    print(f"\nPipeline complete. Results available in {TXT_DIR}")


if __name__ == "__main__":
    main()
