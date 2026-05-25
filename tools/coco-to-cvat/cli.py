#!/usr/bin/env python3
"""CLI: COCO JSON → CVAT XML."""
import argparse
import sys

from coco_to_cvat import convert_file


def main() -> int:
    p = argparse.ArgumentParser(description="Convert COCO JSON to CVAT XML")
    p.add_argument("input", help="Path to COCO JSON file")
    p.add_argument("-o", "--output", required=True, help="Output XML path")
    p.add_argument(
        "--anno-type",
        choices=("bbox", "polygon", "both"),
        default="bbox",
        help="Annotation types to export",
    )
    p.add_argument(
        "--cvat-version",
        choices=("1.1", "2.0"),
        default="1.1",
        help="CVAT version in XML metadata",
    )
    args = p.parse_args()
    try:
        convert_file(
            args.input,
            args.output,
            anno_type=args.anno_type,
            cvat_version=args.cvat_version,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    print(f"Written: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
