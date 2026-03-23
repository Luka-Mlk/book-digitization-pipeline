from pathlib import Path
from collections import defaultdict

from processor.image_filter import ImageFilter
from processor.ocr_engine import OCREngine
from utils.config import IMAGES_DIR, PROC_DIR, TXT_DIR, OCR_OUTPUT_DIR


def main():
    # 1. Initialize our tools
    filt = ImageFilter(scale_factor=2)
    engine = OCREngine(languages="mkd+chu")

    # 2. Collect all images from the flat images directory
    image_paths = list(IMAGES_DIR.glob("*.png"))

    if not image_paths:
        print(f"No images found in {IMAGES_DIR}. Check your scraper output.")
        return

    print(f"Starting pipeline for {len(image_paths)} images...")

    # Track which books we've processed to merge them at the end
    processed_books = set()

    for img_path in sorted(image_paths):
        # Filename: bookname_page_NN.png
        try:
            book_name = img_path.stem.split("_page_")[0]
            processed_books.add(book_name)
        except IndexError:
            print(f"Skipping malformed filename: {img_path.name}")
            continue

        # Intermediate paths
        img_output_path = PROC_DIR / book_name / img_path.name
        txt_output_path = TXT_DIR / book_name / img_path.with_suffix(".txt").name

        # Ensure directories exist
        img_output_path.parent.mkdir(parents=True, exist_ok=True)
        txt_output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # --- Step A: Image Filtering ---
            processed_img = filt.process(img_path)
            filt.save(processed_img, img_output_path)

            # --- Step B: OCR Extraction ---
            text_content = engine.process_image(img_output_path)

            # --- Step C: Save Intermediate Result ---
            with open(txt_output_path, "w", encoding="utf-8") as f:
                f.write(text_content)

            print(f"✓ Success: {img_path.name}")

        except Exception as e:
            print(f"✗ Failed {img_path.name}: {e}")

    # --- Step D: Merge Results ---
    print("\nMerging individual page results...")
    OCR_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for book in processed_books:
        book_txt_dir = TXT_DIR / book
        # Sort numerically by extracting the number from bookpage_NN.txt
        txt_files = sorted(
            list(book_txt_dir.glob("*.txt")),
            key=lambda x: int(x.stem.split("_page_")[1])
        )
        
        combined_text = []
        for i, f_path in enumerate(txt_files):
            with open(f_path, "r", encoding="utf-8") as f:
                combined_text.append(f.read().strip())
            
            if i < len(txt_files) - 1:
                combined_text.append("\n\n---\n\n")
        
        output_file = OCR_OUTPUT_DIR / f"{book}_ocr_raw.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(combined_text)
        
        print(f"✓ Merged results for {book} into {output_file.name}")

    print(f"\nPipeline complete. Final results in {OCR_OUTPUT_DIR}")


if __name__ == "__main__":
    main()
