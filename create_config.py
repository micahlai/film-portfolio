import os
import json
from pathlib import Path

ROOT = Path(".")
WORK_DIR = ROOT / "work"

CONFIG = {
    "profileImage": "profile.webp",
    "work": {},
    "photography": [],
    "graphic": [],
    "crew": []
}


def natural_sort_key(path):
    """Sort files numerically when possible."""
    stem = path.stem
    try:
        return int(stem)
    except ValueError:
        return stem


def get_webp_files(directory):
    if not directory.exists():
        return []

    files = sorted(
        [f for f in directory.iterdir() if f.suffix.lower() == ".webp"],
        key=natural_sort_key
    )

    return [str(f.as_posix()) for f in files]


# -----------------------------
# Photography
# -----------------------------
CONFIG["photography"] = get_webp_files(ROOT / "photography")

# -----------------------------
# Graphic Design
# -----------------------------
CONFIG["graphic"] = get_webp_files(ROOT / "graphic-design")

# -----------------------------
# Crew
# -----------------------------
CONFIG["crew"] = get_webp_files(ROOT / "crew")

# -----------------------------
# Work
# -----------------------------
if WORK_DIR.exists():
    work_folders = sorted(
        [d for d in WORK_DIR.iterdir() if d.is_dir()],
        key=lambda x: int(x.name)
    )

    for folder in work_folders:
        work_id = folder.name

        info_path = folder / "info.txt"

        title = ""
        year = ""
        work_type = ""
        role = ""
        info = ""
        link = ""

        if info_path.exists():
            with open(info_path, "r", encoding="utf-8") as f:
                lines = [line.rstrip("\n") for line in f.readlines()]

            # Ensure at least 6 lines
            while len(lines) < 6:
                lines.append("")

            title = lines[0]
            year = lines[1]
            work_type = lines[2]
            role = lines[3]
            info = lines[4]
            link = lines[5]

        stills = get_webp_files(folder / "stills")
        bts = get_webp_files(folder / "bts")

        CONFIG["work"][work_id] = {
            "title": title,
            "year": year,
            "type": work_type,
            "role": role,
            "info": info,
            "link": link,
            "thumbnail": f"work/{work_id}/thumbnail.webp",
            "stills": stills,
            "bts": bts
        }


# -----------------------------
# Write config.js
# -----------------------------
json_text = json.dumps(CONFIG, indent=2, ensure_ascii=False)

output = f"const portfolioConfig = {json_text};\n"

with open("config.js", "w", encoding="utf-8") as f:
    f.write(output)

print("Generated config.js")