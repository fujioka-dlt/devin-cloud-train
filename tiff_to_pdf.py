#!/usr/bin/env python3
"""Recursively convert TIFF drawings to same-folder PDFs."""

from __future__ import annotations

import argparse
import csv
import logging
import os
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image, ImageOps, ImageSequence
except ImportError as exc:  # pragma: no cover - exercised only without deps
    raise SystemExit(
        "Pillow is required. Install dependencies with: pip install -r requirements.txt"
    ) from exc

try:
    from pypdf import PdfReader
except ImportError as exc:  # pragma: no cover - exercised only without deps
    raise SystemExit(
        "pypdf is required. Install dependencies with: pip install -r requirements.txt"
    ) from exc


TIFF_SUFFIXES = {".tif", ".tiff"}
PDF_SAFE_MODES = {"1", "L", "RGB", "CMYK"}
DEFAULT_CSV_NAME = "tiff_to_pdf_results.csv"


@dataclass
class ConversionResult:
    status: str
    source_tiff: Path
    pdf_path: Path
    message: str
    processed_at: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="指定フォルダ配下の TIFF (.tif/.tiff) を同じフォルダに PDF へ変換します。",
    )
    parser.add_argument("source_folder", type=Path, help="検索対象の親フォルダ")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(DEFAULT_CSV_NAME),
        help=f"結果 CSV の出力先 (既定: {DEFAULT_CSV_NAME})",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        help="任意のログファイル出力先。省略時はコンソールのみ。",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="変換せず、対象と既存 PDF の有無だけを CSV に出力します。",
    )
    return parser.parse_args()


def configure_logging(log_file: Path | None) -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=handlers,
        force=True,
    )


def iter_tiff_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in TIFF_SUFFIXES:
            yield path


def pdf_path_for(tiff_path: Path) -> Path:
    return tiff_path.with_suffix(".pdf")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def resolve_dpi(*info_objects: dict) -> tuple[int, int]:
    for info in info_objects:
        dpi = info.get("dpi")
        if not isinstance(dpi, (tuple, list)) or len(dpi) < 2:
            continue
        try:
            x_dpi = float(dpi[0])
            y_dpi = float(dpi[1])
        except (TypeError, ValueError):
            continue
        if 1 <= x_dpi <= 2400 and 1 <= y_dpi <= 2400:
            return int(round(x_dpi)), int(round(y_dpi))
    return 300, 300


def prepare_frame(frame: Image.Image) -> Image.Image:
    image = ImageOps.exif_transpose(frame)

    if "A" in image.getbands():
        rgba = image.convert("RGBA")
        background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        background.alpha_composite(rgba)
        image = background.convert("RGB")
    elif image.mode == "P":
        image = image.convert("RGB")
    elif image.mode not in PDF_SAFE_MODES:
        image = image.convert("RGB")

    return image.copy()


def load_pdf_frames(tiff_path: Path) -> tuple[list[Image.Image], tuple[int, int]]:
    frames: list[Image.Image] = []
    first_info: dict = {}

    with Image.open(tiff_path) as image:
        first_info = dict(image.info)
        for frame in ImageSequence.Iterator(image):
            frames.append(prepare_frame(frame))

    if not frames:
        raise ValueError("TIFF に画像フレームがありません")

    dpi = resolve_dpi(first_info, frames[0].info)
    return frames, dpi


def verify_pdf(pdf_path: Path) -> None:
    with PdfReader(str(pdf_path)) as reader:
        if reader.is_encrypted:
            raise ValueError("PDF が暗号化されています")
        if len(reader.pages) == 0:
            raise ValueError("PDF にページがありません")
        _ = reader.pages[0].mediabox


def convert_tiff_to_pdf(tiff_path: Path, pdf_path: Path) -> None:
    frames, dpi = load_pdf_frames(tiff_path)

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{pdf_path.name}.", suffix=".tmp", dir=pdf_path.parent
    )
    os.close(fd)
    temp_path = Path(temp_name)

    try:
        frames[0].save(
            temp_path,
            "PDF",
            resolution=dpi,
            save_all=True,
            append_images=frames[1:],
        )
        verify_pdf(temp_path)
        temp_path.replace(pdf_path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def process_tiff(tiff_path: Path, dry_run: bool) -> ConversionResult:
    pdf_path = pdf_path_for(tiff_path)
    processed_at = utc_now()

    if pdf_path.exists():
        return ConversionResult(
            status="skipped",
            source_tiff=tiff_path,
            pdf_path=pdf_path,
            message="同名 PDF が既に存在します",
            processed_at=processed_at,
        )

    if dry_run:
        return ConversionResult(
            status="would_convert",
            source_tiff=tiff_path,
            pdf_path=pdf_path,
            message="dry-run のため変換していません",
            processed_at=processed_at,
        )

    try:
        convert_tiff_to_pdf(tiff_path, pdf_path)
    except Exception as exc:
        logging.exception("変換に失敗しました: %s", tiff_path)
        return ConversionResult(
            status="failed",
            source_tiff=tiff_path,
            pdf_path=pdf_path,
            message=str(exc),
            processed_at=processed_at,
        )

    return ConversionResult(
        status="converted",
        source_tiff=tiff_path,
        pdf_path=pdf_path,
        message="PDF を作成し、正常に開けることを確認しました",
        processed_at=processed_at,
    )


def write_results_csv(csv_path: Path, results: list[ConversionResult]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "status",
                "source_tiff",
                "pdf_path",
                "message",
                "processed_at",
            ],
        )
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    "status": result.status,
                    "source_tiff": str(result.source_tiff),
                    "pdf_path": str(result.pdf_path),
                    "message": result.message,
                    "processed_at": result.processed_at,
                }
            )


def main() -> int:
    args = parse_args()
    root = args.source_folder.expanduser().resolve()

    if not root.exists():
        print(f"エラー: フォルダが見つかりません: {root}", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"エラー: フォルダを指定してください: {root}", file=sys.stderr)
        return 2

    configure_logging(args.log_file)
    logger = logging.getLogger(__name__)

    results: list[ConversionResult] = []
    tiff_files = list(iter_tiff_files(root))

    if not tiff_files:
        logger.info("対象の TIFF ファイルは見つかりませんでした: %s", root)

    for index, tiff_path in enumerate(tiff_files, start=1):
        logger.info("[%d/%d] 処理中: %s", index, len(tiff_files), tiff_path)
        result = process_tiff(tiff_path, dry_run=args.dry_run)
        results.append(result)
        logger.info("結果: %s - %s", result.status, tiff_path)

    write_results_csv(args.csv, results)

    counts = {
        status: sum(1 for result in results if result.status == status)
        for status in {result.status for result in results}
    }
    logger.info("完了: %s", ", ".join(f"{key}={value}" for key, value in sorted(counts.items())) or "対象なし")
    logger.info("結果 CSV: %s", args.csv.resolve())

    return 1 if any(result.status == "failed" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
