from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorOptions, AcceleratorDevice
import json


# Configure pipeline
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


# Export to markdown
markdown_content = result.document.export_to_markdown()

# Save to file
output_file = "output.md"
with open(output_file, "w") as f:
    f.write(markdown_content)

# Save to JSON
output_json_file = "Docling_structure.json"
with open(output_json_file, "w") as f:
    json.dump(result.document.export_to_dict(), f, indent=2)


print(f"Successfully converted {source} to {output_file}")
print(result.document.export_to_dict().keys())
print(f"Succesfully exported structure to {output_json_file}")
