# US-DATA Annotation Tools

Open-source data annotation and dataset conversion tools for computer vision, machine learning and AI dataset preparation.

Developed by US-DATA for image annotation workflows, object detection datasets, semantic segmentation pipelines and annotation format conversion.

---

## Supported Annotation Tasks

- Image Annotation
- Computer Vision Annotation
- Bounding Boxes
- Object Detection
- Polygon Annotation
- Semantic Segmentation
- Cuboid Annotation
- AI Dataset Preparation
- Dataset Conversion
- Machine Learning Annotation

---

# COCO JSON to CVAT XML Converter

A standalone Python converter for transforming COCO JSON datasets into CVAT XML annotation format.

The converter supports:

- Bounding Boxes
- Polygon Annotation
- Semantic Segmentation
- COCO datasets
- CVAT XML export
- AI image annotation workflows

---

## Features

- Pure Python core converter
- CLI support
- FastAPI server
- Production-ready conversion pipeline
- COCO JSON → CVAT XML conversion
- Supports bbox, polygon and mixed annotations
- Supports CVAT XML 1.1 and 2.0
- Lightweight standalone architecture
- Browser and API integration ready

---

## Repository Structure

```text
us-data-annotation-tools/
├── tools/
│   └── coco-to-cvat/
│       ├── coco_to_cvat.py
│       ├── cli.py
│       ├── api.py
│       └── requirements.txt
├── examples/
├── docs/
├── assets/
└── README.md
```

---

# Installation

## Clone repository

```bash
git clone https://github.com/us-data-annotation-tools/us-data-annotation-tools.git
cd us-data-annotation-tools
```

---

# CLI Usage

```bash
python3 cli.py instances.json -o annotations.xml --anno-type both
```

### Parameters

| Parameter | Values |
|---|---|
| anno-type | bbox, polygon, both |
| cvat-version | 1.1, 2.0 |

---

# FastAPI Server

Install dependencies:

```bash
pip install -r requirements.txt
```

Run server:

```bash
uvicorn api:app --port 8000
```

---

# API Example

```bash
curl -X POST http://localhost:8000/convert \
  -F "file=@instances.json" \
  -F "anno_type=bbox" \
  -F "cvat_version=1.1" \
  -o result.xml
```

---

# Python API Example

```python
import json
from coco_to_cvat import coco_to_cvat_xml

with open("instances.json", encoding="utf-8") as f:
    coco = json.load(f)

xml = coco_to_cvat_xml(
    coco,
    anno_type="both",
    cvat_version="1.1"
)

with open("annotations.xml", "w", encoding="utf-8") as f:
    f.write(xml)
```

---

# Supported Formats

Input:
- COCO JSON

Output:
- CVAT XML

Planned:
- YOLO TXT
- Pascal VOC XML
- COCO Validator
- CVAT to COCO Converter

---

# Use Cases

Useful for:

- Computer Vision datasets
- Object Detection projects
- AI image annotation workflows
- Semantic Segmentation pipelines
- Dataset preprocessing
- Annotation migration
- CVAT dataset conversion
- ML dataset preparation
- AI model training

---

# About US-DATA

US-DATA is a data annotation company focused on machine learning, computer vision, NLP and AI dataset preparation.

Services include:

- image annotation
- video annotation
- text annotation
- audio transcription
- semantic segmentation
- bounding boxes
- polygon annotation
- cuboid annotation
- keypoint labeling
- dataset preparation

Website:
https://usdataml.com/en/

Online Converter:
https://usdataml.com/en/pages/tools/coco-to-cvat.html

Tools:
https://usdataml.com/en/pages/tools.html

Contact:
https://usdataml.com/en/pages/contact.html

---

# Related Keywords

Data Annotation, Image Annotation, Computer Vision Annotation, COCO JSON, CVAT XML, Bounding Boxes, Semantic Segmentation, Polygon Annotation, Cuboid Annotation, Dataset Conversion, AI Dataset Preparation, Object Detection, Machine Learning Annotation Tools.

---

# License

MIT License
