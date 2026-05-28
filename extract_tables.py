from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorOptions, AcceleratorDevice
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


table_count = 0

for item, level in doc.iterate_items():
    label = getattr(item, "label", None)

    if label == "table":
        table_count += 1

        # Check if item has export_to_dataframe method
        if hasattr(item, "export_to_dataframe"):
            df = item.export_to_dataframe()
            filename = f"table_{table_count}.csv"
            df.to_csv(filename, index=False)
            print(f"Saved {filename}")
        else:
            print(f"Found table item but it lacks export_to_dataframe method: {type(item)}")

if table_count == 0:
    print("No tables found in the document.")
