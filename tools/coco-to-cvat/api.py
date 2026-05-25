"""
Standalone FastAPI endpoint (same logic as US-DATA production API).
"""
import json

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from coco_to_cvat import coco_to_cvat_xml

app = FastAPI(title="COCO → CVAT Converter", version="1.0.0")

MAX_BYTES = 50 * 1024 * 1024


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/convert")
async def convert(
    file: UploadFile = File(...),
    anno_type: str = Form("bbox"),
    cvat_version: str = Form("1.1"),
):
    if not (file.filename or "").endswith(".json"):
        raise HTTPException(status_code=400, detail="Upload a .json file")

    content = await file.read()
    if len(content) > MAX_BYTES:
        raise HTTPException(status_code=400, detail="File exceeds 50 MB")

    try:
        coco = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    if "images" not in coco or "annotations" not in coco:
        raise HTTPException(
            status_code=400,
            detail="Not a COCO file (missing images / annotations)",
        )

    if anno_type not in ("bbox", "polygon", "both"):
        anno_type = "bbox"
    if cvat_version not in ("1.1", "2.0"):
        cvat_version = "1.1"

    xml_content = coco_to_cvat_xml(coco, anno_type, cvat_version)
    out_name = (file.filename or "coco.json").replace(".json", "_cvat.xml")

    return Response(
        content=xml_content.encode("utf-8"),
        media_type="application/xml",
        headers={"Content-Disposition": f'attachment; filename="{out_name}"'},
    )


# US-DATA-compatible path
@app.post("/api/tools/coco-to-cvat")
async def convert_legacy(
    file: UploadFile = File(...),
    anno_type: str = Form("bbox"),
    cvat_version: str = Form("1.1"),
):
    return await convert(file=file, anno_type=anno_type, cvat_version=cvat_version)
