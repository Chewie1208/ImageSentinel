import os
from pathlib import Path
from scan_models import CandidateImage
from PIL import Image

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}
EXCLUDED_FOLDERS = {
        "windows",
        "program files",
        "program files (x86)",
        "programdata",
#        "$recycle.bin",
        "system volume information",
        "recovery",
        "msocache",
        "intel",
        "amd",
        "nvidia",
        "perflogs",
        "inetpub",
        ".gradle",
        ".m2",
        ".nuget",
        "node_modules",
        ".git",
        ".svn",
        ".hg",
        "__pycache__",
        ".vscode",
        "sdk",
        "sdks",
        "android",
        ".android",
        "placeholdertilelogofolder",
        "windowsapps",
        "microsoft",
        "packages"
    }

def discover_images(
    source_path,
    results_path,
    callback
):

    image_files = []

    for root, dirs, files in os.walk(source_path):

        prune_dirs(dirs)

        for filename in files:

            file = Path(root) / filename
            if str(file).startswith(
                str(results_path)
            ):
                continue

            if file.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            image_files.append(file)

    callback(
        f"Discovered {len(image_files):,} images"
    )

    return image_files



def build_candidates(
    image_files,
    callback
):

    candidates = []
    count = 0

    for file in image_files:
        count +=1
        try:

            size_bytes = file.stat().st_size

            with Image.open(file) as img:
                width, height = img.size

            # If width of height are less than 200 px, exclude
            if width < 200:
                continue
            if height < 200:
                continue

            # If image has more than 50mp, exclude
            if width * height > 50_000_000:
                continue

            # If image size is less 50kb, exclude
            if size_bytes < 50 * 1024:
                continue
            
            # Otherwise create 'candidate' and add to array
            candidate = CandidateImage(
                path=file,
                size_bytes=size_bytes,
                width=width,
                height=height,
                requires_resize=False
            )

            candidates.append(candidate)

        except Exception as ex:

            continue

    return candidates

def prune_dirs(dirs):

    dirs[:] = [
        d for d in dirs
        if d.lower() not in EXCLUDED_FOLDERS
    ]