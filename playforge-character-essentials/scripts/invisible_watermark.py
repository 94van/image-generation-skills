#!/usr/bin/env python3
"""Embed and verify a traceable, non-visible marker in an original lossless PNG.

Requires Pillow. This is plaintext provenance data, not encryption, authentication,
or copyright certification. Cropping, screenshots, resizing, and lossy re-encoding
are not supported preservation paths. The source image is never overwritten.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import struct
import sys
import uuid
import zlib
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, PngImagePlugin

MAGIC = b"PFWMARK1"
HEADER = struct.Struct(">8sII")  # magic, UTF-8 payload length, payload CRC32
MAX_PAYLOAD_BYTES = 65536
METHOD = "blue-lsb-sequential-v1"
PAYLOAD_SCHEMA = "playforge.invisible-watermark/v1"
MANIFEST_SCHEMA = "playforge.invisible-watermark-manifest/v1"
META_PAYLOAD = "playforge.watermark"
META_METHOD = "playforge.watermark.method"


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def default_manifest(image_path: Path) -> Path:
    return image_path.with_name(image_path.name + ".watermark.json")


def read_png(path: Path) -> tuple[Image.Image, dict, bytes]:
    raw = path.read_bytes()
    with Image.open(io.BytesIO(raw)) as image:
        if image.format != "PNG":
            raise ValueError("Input must be a lossless PNG file.")
        if raw[24] > 8:
            raise ValueError("PNG bit depths above 8 are unsupported; provide an 8-bit PNG without reducing it here.")
        if getattr(image, "n_frames", 1) != 1:
            raise ValueError("Animated PNG is unsupported; provide one static image.")
        image.load()
        info = image.info.copy()
        # Palette/greyscale PNGs are converted without changing rendered colours.
        has_alpha = "A" in image.getbands() or "transparency" in info
        converted = image.convert("RGBA" if has_alpha else "RGB")
    return converted, info, raw


def color_chunks(raw: bytes) -> list[tuple[bytes, bytes]]:
    """Preserve display-affecting PNG chunks that Pillow does not save from info."""
    chunks = []
    offset = 8  # PNG signature
    while offset + 12 <= len(raw):
        length = struct.unpack_from(">I", raw, offset)[0]
        end = offset + 12 + length
        if end > len(raw):
            raise ValueError("Truncated PNG chunk.")
        chunk_type = raw[offset + 4:offset + 8]
        data = raw[offset + 8:offset + 8 + length]
        if chunk_type in (b"gAMA", b"sRGB", b"cHRM"):
            expected = struct.unpack_from(">I", raw, offset + 8 + length)[0]
            if (zlib.crc32(chunk_type + data) & 0xFFFFFFFF) != expected:
                raise ValueError("Invalid PNG colour-metadata checksum.")
            chunks.append((chunk_type, data))
        offset = end
        if chunk_type == b"IEND":
            break
    return chunks


def payload_errors(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return ["Watermark payload is not a JSON object."]
    errors = []
    if payload.get("schema") != PAYLOAD_SCHEMA:
        errors.append("Unsupported payload schema.")
    owner = payload.get("owner")
    if not isinstance(owner, str) or not owner.strip() or len(owner) > 256:
        errors.append("Invalid owner.")
    try:
        uuid.UUID(payload.get("artwork_id", ""))
    except (ValueError, TypeError, AttributeError):
        errors.append("Invalid artwork_id UUID.")
    stamp = payload.get("created_utc")
    try:
        if not isinstance(stamp, str) or not stamp.endswith("Z"):
            raise ValueError
        datetime.fromisoformat(stamp[:-1] + "+00:00")
    except (ValueError, TypeError):
        errors.append("Invalid UTC timestamp.")
    source_hash = payload.get("source_sha256")
    if not isinstance(source_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", source_hash):
        errors.append("Invalid source SHA256.")
    return errors


def packet_for(payload: dict) -> tuple[bytes, int, int]:
    encoded = canonical_json(payload).encode("utf-8")
    if len(encoded) > MAX_PAYLOAD_BYTES:
        raise ValueError("Watermark payload is too large.")
    checksum = zlib.crc32(encoded) & 0xFFFFFFFF
    return HEADER.pack(MAGIC, len(encoded), checksum) + encoded, len(encoded), checksum


def read_lsb_bytes(pixels: bytes | bytearray, channels: int, length: int) -> bytes:
    if length * 8 > len(pixels) // channels:
        raise ValueError("Watermark length exceeds the image capacity.")
    result = bytearray(length)
    for bit_index in range(length * 8):
        result[bit_index // 8] |= (pixels[bit_index * channels + 2] & 1) << (7 - bit_index % 8)
    return bytes(result)


def extract_lsb(image: Image.Image) -> dict:
    pixels = image.tobytes()
    channels = len(image.getbands())
    if image.width * image.height < HEADER.size * 8:
        return {"status": "absent", "errors": ["Image is too small for a watermark header."]}
    magic, length, expected_crc = HEADER.unpack(read_lsb_bytes(pixels, channels, HEADER.size))
    if magic != MAGIC:
        return {"status": "absent", "errors": ["No recognized pixel watermark magic."]}
    if length == 0 or length > MAX_PAYLOAD_BYTES or (HEADER.size + length) * 8 > image.width * image.height:
        return {"status": "corrupt", "errors": ["Invalid watermark payload length."]}
    encoded = read_lsb_bytes(pixels, channels, HEADER.size + length)[HEADER.size:]
    actual_crc = zlib.crc32(encoded) & 0xFFFFFFFF
    if actual_crc != expected_crc:
        return {"status": "corrupt", "errors": ["Pixel watermark CRC32 mismatch."]}
    try:
        payload = json.loads(encoded.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {"status": "corrupt", "errors": ["Pixel watermark is not valid UTF-8 JSON."]}
    errors = payload_errors(payload)
    return {
        "status": "corrupt" if errors else "valid",
        "payload": payload,
        "payload_bytes": length,
        "crc32": f"{expected_crc:08x}",
        "errors": errors,
    }


def embed(source: Path, output: Path, manifest_path: Path, owner: str) -> dict:
    if output.suffix.lower() != ".png":
        raise ValueError("Output filename must end in .png.")
    resolved = [path.resolve() for path in (source, output, manifest_path)]
    if len(set(resolved)) != 3:
        raise ValueError("Source, output, and manifest must be three different files.")
    for path in (output, manifest_path):
        if path.exists() or path.is_symlink():
            raise FileExistsError(f"Refusing to overwrite existing file: {path}")
        if not path.parent.is_dir():
            raise ValueError(f"Output directory does not exist: {path.parent}")
    image, info, source_raw = read_png(source)
    existing = extract_lsb(image)
    if existing["status"] == "valid" or META_PAYLOAD in info:
        raise ValueError("Source already contains a PlayForge watermark; use the unmarked source.")
    payload = {
        "schema": PAYLOAD_SCHEMA,
        "owner": owner,
        "artwork_id": str(uuid.uuid4()),
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z"),
        "source_sha256": sha256(source_raw),
    }
    errors = payload_errors(payload)
    if errors:
        raise ValueError(" ".join(errors))
    packet, length, checksum = packet_for(payload)
    if len(packet) * 8 > image.width * image.height:
        raise ValueError(f"Image is too small: needs at least {len(packet) * 8} pixels for this watermark.")
    pixels = bytearray(image.tobytes())
    channels = len(image.getbands())
    for bit_index in range(len(packet) * 8):
        offset = bit_index * channels + 2
        bit = (packet[bit_index // 8] >> (7 - bit_index % 8)) & 1
        pixels[offset] = (pixels[offset] & 0xFE) | bit
    marked = Image.frombytes(image.mode, image.size, bytes(pixels))
    pnginfo = PngImagePlugin.PngInfo()
    for chunk_type, chunk_data in color_chunks(source_raw):
        pnginfo.add(chunk_type, chunk_data)
    for key, value in info.items():
        if isinstance(value, str) and key not in (META_PAYLOAD, META_METHOD):
            pnginfo.add_text(key, value)
    pnginfo.add_text(META_PAYLOAD, canonical_json(payload))
    pnginfo.add_text(META_METHOD, METHOD)
    options = {key: info[key] for key in ("icc_profile", "dpi", "exif") if key in info}
    buffer = io.BytesIO()
    marked.save(buffer, format="PNG", pnginfo=pnginfo, **options)
    output_raw = buffer.getvalue()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "watermark": payload,
        "embedding": {"method": METHOD, "magic": MAGIC.decode("ascii"), "payload_bytes": length, "crc32": f"{checksum:08x}"},
        "input": {"file": source.name, "sha256": payload["source_sha256"]},
        "output": {"file": output.name, "sha256": sha256(output_raw), "mode": image.mode, "width": image.width, "height": image.height},
    }
    created = []
    try:
        # Exclusive creation also prevents accidental overwrite after the checks.
        with output.open("xb") as stream:
            created.append(output)
            stream.write(output_raw)
        with manifest_path.open("x", encoding="utf-8") as stream:
            created.append(manifest_path)
            json.dump(manifest, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    except Exception:
        for path in reversed(created):
            path.unlink(missing_ok=True)
        raise
    return {"status": "embedded", "output": str(output), "manifest": str(manifest_path), "watermark": payload, "output_sha256": sha256(output_raw)}


def inspect(image_path: Path, manifest_path: Path | None = None) -> tuple[dict, int]:
    image, info, image_raw = read_png(image_path)
    extracted = extract_lsb(image)
    errors = list(extracted.get("errors", []))
    payload = extracted.get("payload")
    checks = {"pixel_payload": extracted["status"] == "valid", "png_metadata": False, "manifest": None}
    metadata_present = META_PAYLOAD in info or META_METHOD in info
    if extracted["status"] == "valid":
        try:
            metadata = json.loads(info.get(META_PAYLOAD, ""))
            checks["png_metadata"] = metadata == payload and info.get(META_METHOD) == METHOD
        except (json.JSONDecodeError, TypeError):
            pass
        if not checks["png_metadata"]:
            errors.append("PNG text metadata is missing, invalid, or differs from the pixel watermark.")
    elif metadata_present:
        errors.append("PNG claims a watermark, but the pixel watermark is missing or corrupt.")

    explicit_manifest = manifest_path is not None
    candidate = manifest_path if explicit_manifest else default_manifest(image_path)
    manifest_used = None
    if candidate.exists():
        manifest_used = str(candidate)
        checks["manifest"] = False
        try:
            manifest = json.loads(candidate.read_text(encoding="utf-8"))
            expected_embedding = {"method": METHOD, "magic": MAGIC.decode("ascii"), "payload_bytes": extracted.get("payload_bytes"), "crc32": extracted.get("crc32")}
            expected_output = {"sha256": sha256(image_raw), "mode": image.mode, "width": image.width, "height": image.height}
            checks["manifest"] = (
                isinstance(manifest, dict)
                and extracted["status"] == "valid"
                and manifest.get("schema") == MANIFEST_SCHEMA
                and manifest.get("watermark") == payload
                and manifest.get("embedding") == expected_embedding
                and isinstance(manifest.get("input"), dict)
                and manifest["input"].get("sha256") == payload["source_sha256"]
                and isinstance(manifest.get("output"), dict)
                and all(manifest["output"].get(key) == value for key, value in expected_output.items())
            )
            if not checks["manifest"]:
                errors.append("Manifest payload, embedding details, dimensions, or file SHA256 do not match.")
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            errors.append("Manifest cannot be read as UTF-8 JSON.")
    elif explicit_manifest:
        checks["manifest"] = False
        errors.append("The requested manifest does not exist.")

    if checks["pixel_payload"] and checks["png_metadata"] and checks["manifest"] is not False:
        status, code = "valid", 0
    elif extracted["status"] == "absent" and not metadata_present and checks["manifest"] is None:
        status, code = "absent", 2
    else:
        status, code = "invalid", 3
    return {
        "status": status,
        "image": str(image_path),
        "output_sha256": sha256(image_raw),
        "watermark": payload,
        "checks": checks,
        "manifest": manifest_used,
        "errors": errors,
        "scope": "Original lossless PNG only; not encryption, authentication, or copyright certification.",
    }, code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    embed_parser = subparsers.add_parser("embed", help="Create a new PNG and provenance manifest; never overwrite files.")
    embed_parser.add_argument("source", type=Path)
    embed_parser.add_argument("output", type=Path)
    embed_parser.add_argument("--owner", default="@PLAyfORGE_")
    embed_parser.add_argument("--manifest", type=Path, help="Default: OUTPUT.png.watermark.json")
    inspect_parser = subparsers.add_parser("inspect", help="Verify pixel data, PNG metadata, and a present or specified manifest.")
    inspect_parser.add_argument("image", type=Path)
    inspect_parser.add_argument("--manifest", type=Path, help="Explicit manifest; otherwise use the adjacent default file if present.")
    args = parser.parse_args()
    try:
        if args.command == "embed":
            result = embed(args.source, args.output, args.manifest or default_manifest(args.output), args.owner)
            code = 0
        else:
            result, code = inspect(args.image, args.manifest)
    except (OSError, ValueError, Image.DecompressionBombError) as error:
        result, code = {"status": "error", "error": str(error)}, 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
