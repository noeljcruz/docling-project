from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorOptions, AcceleratorDevice
from docling_core.types.doc.labels import DocItemLabel
import logging

# Disable logging
logging.basicConfig(level=logging.ERROR)


pipeline_options = PdfPipelineOptions()
pipeline_options.accelerator_options = AcceleratorOptions(
    num_threads=4,
    device=AcceleratorDevice.CPU,
)


source = "Docling_sample.pdf"
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
result = converter.convert(source)
doc = result.document


title_text = ""
headings = []
paragraphs = []


# Iterate over items to categorize them
# We assume the first section_header is the title
found_title = False

for item, level in doc.iterate_items():
    label = getattr(item, "label", None)
    text = getattr(item, "text", "").strip()

    if not text:
        continue
    
    if label == "section_header":
        # Try to get level from item, default to 1
        h_level = getattr(item, "level", 1)
        headings.append(f"{'#' * h_level} {text}")

        if not found_title:
            title_text = text
            found_title = True
    
    elif label == "text":
        paragraphs.append(text)


# If no title found from headers, use doc name
if not title_text:
    title_text = doc.name


# Write to files
with open("title.md", "w") as f:
    f.write(title_text + "\n")

with open("headings.md", "w") as f:
    f.write("\n\n".join(headings) + "\n")

with open("paragraphs.md", "w") as f:
    f.write("\n\n".join(paragraphs) + "\n")


print("Extraction complete.")
print(f"Title saved to title.md ({len(title_text)} chars)")
print(f"Headings saved to headings.md ({len(headings)} items)")
print(f"Paragraphs saved to paragraphs.md ({len(paragraphs)} items)")
