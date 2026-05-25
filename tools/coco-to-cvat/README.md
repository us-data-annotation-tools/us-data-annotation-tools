# COCO JSON → CVAT XML Converter

Convert [COCO](https://cocodataset.org/#format-data) instance annotation JSON files to [CVAT](https://github.com/cvat-ai/cvat) XML for task import.

Used on [US-DATA](https://usdataml.com) (RU / EN web UI).

## Features

- Bounding boxes (`bbox`)
- Polygons from COCO `segmentation`
- Combined mode: `bbox + polygons`
- CVAT export version `1.1` or `2.0` (metadata)
- No third-party dependencies for conversion logic (stdlib only)

## Quick start (CLI)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # only needed for HTTP API

python cli.py instances.json -o annotations.xml
python cli.py instances.json -o out.xml --anno-type both --cvat-version 2.0
```

## HTTP API (optional)

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

```bash
curl -X POST http://localhost:8000/convert \
  -F "file=@instances.json" \
  -F "anno_type=bbox" \
  -F "cvat_version=1.1" \
  -o result.xml
```

## Python API

```python
import json
from coco_to_cvat import coco_to_cvat_xml

with open("instances.json", encoding="utf-8") as f:
    coco = json.load(f)

xml = coco_to_cvat_xml(coco, anno_type="both", cvat_version="1.1")
with open("annotations.xml", "w", encoding="utf-8") as f:
    f.write(xml)
```

## Parameters

| Parameter       | Values              | Default |
|----------------|---------------------|---------|
| `anno_type`    | `bbox`, `polygon`, `both` | `bbox` |
| `cvat_version` | `1.1`, `2.0`        | `1.1`   |

## COCO input

Expects a standard COCO instances file with at least:

- `images` — list of image records (`id`, `file_name`, `width`, `height`)
- `annotations` — list with `image_id`, `category_id`, optional `bbox` and `segmentation`
- `categories` — list with `id` and `name`

## License

Proprietary / US-DATA — adjust before publishing if you open-source it.
