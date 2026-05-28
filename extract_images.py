from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorOptions, AcceleratorDevice
import logging

# Disable logging
logging.basicConfig(level=logging.ERROR)


# Configure pipeline to generate images
pipeline_options = PdfPipelineOptions()
pipeline_options.accelerator_options = AcceleratorOptions(
    num_threads=4,
    device=AcceleratorDevice.CPU,
)
pipeline_options.generate_picture_images = True


source = "Docling_sample.pdf"
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
print("Converting document (this may take a moment as images are being generated)...")
result = converter.convert(source)
doc = result.document


image_count = 0

for item, level in doc.iterate_items():
    label = getattr(item, "label", None)

    if label == "picture":
        image_count += 1

        # Try to get image
        if hasattr(item, "get_image"):
            image = item.get_image(doc)

            if image:
                filename = f"figure_{image_count}.png"
                image.save(filename)
                print(f"Saved {filename}")
            else:
                print(f"Found picture item {image_count} but could not extract image data.")
        else:
            print(f"Found picture item {image_count} but it lacks get_image method.")

if image_count == 0:
    print("No images found in the document.")
