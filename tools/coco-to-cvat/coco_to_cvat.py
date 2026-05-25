"""
COCO JSON → CVAT XML converter (stdlib only).
"""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union
from xml.dom import minidom


def coco_to_cvat_xml(
    coco: dict,
    anno_type: str = "bbox",
    cvat_version: str = "1.1",
) -> str:
    """Convert a parsed COCO dict to CVAT XML string."""

    images_by_id = {img["id"]: img for img in coco.get("images", [])}
    cats_by_id = {cat["id"]: cat["name"] for cat in coco.get("categories", [])}

    annots_by_image: dict[int, list] = {}
    for ann in coco.get("annotations", []):
        annots_by_image.setdefault(ann["image_id"], []).append(ann)

    root = ET.Element("annotations")

    ver = ET.SubElement(root, "version")
    ver.text = cvat_version

    meta = ET.SubElement(root, "meta")
    task = ET.SubElement(meta, "task")
    labels_el = ET.SubElement(task, "labels")
    for cat_name in cats_by_id.values():
        lbl = ET.SubElement(labels_el, "label")
        lbl_name = ET.SubElement(lbl, "name")
        lbl_name.text = cat_name
        ET.SubElement(lbl, "color").text = ""
        ET.SubElement(lbl, "attributes")

    for img_id, img_info in images_by_id.items():
        img_el = ET.SubElement(root, "image")
        img_el.set("id", str(img_info["id"]))
        img_el.set("name", img_info.get("file_name", ""))
        img_el.set("width", str(img_info.get("width", 0)))
        img_el.set("height", str(img_info.get("height", 0)))

        for ann in annots_by_image.get(img_id, []):
            label = cats_by_id.get(ann.get("category_id", 0), "unknown")

            if anno_type in ("bbox", "both") and ann.get("bbox"):
                x, y, w, h = ann["bbox"]
                box_el = ET.SubElement(img_el, "box")
                box_el.set("label", label)
                box_el.set("occluded", "0")
                box_el.set("xtl", f"{x:.2f}")
                box_el.set("ytl", f"{y:.2f}")
                box_el.set("xbr", f"{x + w:.2f}")
                box_el.set("ybr", f"{y + h:.2f}")
                box_el.set("z_order", "0")

            if anno_type in ("polygon", "both") and ann.get("segmentation"):
                for seg in ann["segmentation"]:
                    if len(seg) < 6:
                        continue
                    points = " ".join(
                        f"{seg[i]:.2f},{seg[i + 1]:.2f}"
                        for i in range(0, len(seg) - 1, 2)
                    )
                    poly_el = ET.SubElement(img_el, "polygon")
                    poly_el.set("label", label)
                    poly_el.set("occluded", "0")
                    poly_el.set("points", points)
                    poly_el.set("z_order", "0")

    raw = ET.tostring(root, encoding="unicode")
    pretty = minidom.parseString(raw).toprettyxml(indent="  ")
    lines = pretty.split("\n")
    if lines and lines[0].startswith("<?xml"):
        lines = lines[1:]
    return '<?xml version="1.0" encoding="utf-8"?>\n' + "\n".join(lines)


def convert_file(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    anno_type: str = "bbox",
    cvat_version: str = "1.1",
) -> None:
    """Read COCO JSON from disk and write CVAT XML."""
    input_path = Path(input_path)
    output_path = Path(output_path)
    with input_path.open(encoding="utf-8") as f:
        coco = json.load(f)
    xml = coco_to_cvat_xml(coco, anno_type=anno_type, cvat_version=cvat_version)
    output_path.write_text(xml, encoding="utf-8")
