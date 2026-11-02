from pathlib import Path
from nudenet import NudeDetector
from scan_triage import discover_images
from scan_triage import build_candidates
from scan_models import Detection
from html_report import generate_html_report

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
        "sdk,"
        "sdks",
        "android",
        ".android"
    }


def run_scan(
    source_folder,
    results_folder,
    threshold,
    copy_very_high,
    copy_high,
    copy_medium,
    copy_low,
    callback,
    update_scan_count,
    update_flagged_count,
    update_total_images,
    update_progress,
    stop_requested
):

    callback("Scanner Engine Started")
    callback(
        f"Threshold set to {threshold}"
    )
    source_path = Path(source_folder)
    results_path = Path(results_folder)

    results_path.mkdir(
        parents=True,
        exist_ok=True
    )

    # Full list of NudeNet returns

    # ANUS_EXPOSED - High
    # FEMALE_GENITALIA_EXPOSED - High
    # MALE_GENITALIA_EXPOSED - High

    # FEMALE_BREAST_EXPOSED - Medium
    # BUTTOCKS_EXPOSED - Medium

    # BUTTOCKS_COVERED - Low
    # FEMALE_BREAST_COVERED - Low
    # FEMALE_GENITALIA_COVERED - Low
    # MALE_BREAST_EXPOSED - Low

    # ARMPITS_EXPOSED - Ignore
    # BELLY_COVERED - Ignore
    # BELLY_EXPOSED - Ignore
    # FACE_FEMALE - Ignore
    # FACE_MALE - Ignore
    # FEET_COVERED - Ignore
    # FEET_EXPOSED - Ignore

    IGNORE_CLASSES = {
        "ARMPITS_EXPOSED",
        "BELLY_COVERED",
        "BELLY_EXPOSED",
        "FACE_FEMALE",
        "FACE_MALE",
        "FEET_COVERED",
        "FEET_EXPOSED"
    }
    LOW_CLASSES = {
        "BUTTOCKS_COVERED", 
        "FEMALE_BREAST_COVERED",
        "FEMALE_GENITALIA_COVERED"
    }
    MEDIUM_CLASSES = {
        "BUTTOCKS_EXPOSED",
        "FEMALE_BREAST_EXPOSED"
    }
    HIGH_CLASSES = {
        "FEMALE_GENITALIA_EXPOSED",
        "MALE_GENITALIA_EXPOSED"
    }
    VERY_HIGH_CLASSES = {
        "ANUS_EXPOSED"
     }

    count = 0
    flagged_count = 0
    detections_found = 0
    highest_scores = {}

    total_images = 0

    callback(
        "Discovering images..."
    )

    image_files = discover_images(
        source_path,
        results_path,
        callback
    )

    total_images = len(image_files)

    callback(
        "Filtering images..."
    )

    candidates = build_candidates(
        image_files,
        callback
    )


    callback(
        f"Finished. Filtered to {len(candidates):,} images to be scanned"
    )

    update_total_images(
        len(candidates)
    )

    detector = NudeDetector()

    html_path = results_path / "review.html"
    html_rows = []
    detections = []

    callback(
        f"NSFW Scanning underway..."
    )
    for candidate in candidates:
        if stop_requested():
            callback(
                "__SCAN_STOPPED__"
            )

            return
        count += 1

        if not candidate.path.exists():

            callback(
                f"Missing file: {candidate.path}"
            )

            continue
        file = candidate.path

        try:

            results = detector.detect(
                str(candidate.path)
            )

        except Exception as ex:

            callback(
                f"Detection failed: {candidate.path}"
            )

            callback(
                str(ex)
            )

            continue

        if results:

            highest_scores = {}

            # Keep highest score per class
            for result in results:

                cls = result["class"]
                score = result["score"]

                if (
                    cls not in highest_scores
                    or score > highest_scores[cls]
                ):
                    highest_scores[cls] = score

            best_class = None
            best_score = 0
            best_severity = None

            for cls, score in highest_scores.items():
                if score < threshold:
                    continue


                if cls in IGNORE_CLASSES:
                    continue

                severity = None

                if cls in VERY_HIGH_CLASSES:
                    severity = "VERY_HIGH"

                if cls in HIGH_CLASSES:
                    severity = "HIGH"

                elif cls in MEDIUM_CLASSES:
                    severity = "MEDIUM"

                elif cls in LOW_CLASSES:
                    severity = "LOW"

                if severity is None:
                    continue

                if best_class is None:
                    best_class = cls
                    best_score = score
                    best_severity = severity
                    continue

                severity_rank = {
                    "LOW": 1,
                    "MEDIUM": 2,
                    "HIGH": 3,
                    "VERY_HIGH": 4
                }

                if (
                    severity_rank[severity]
                    > severity_rank[best_severity]
                ):

                    best_class = cls
                    best_score = score
                    best_severity = severity

                elif (
                    severity == best_severity
                    and score > best_score
                ):

                    best_class = cls
                    best_score = score
                    best_severity = severity

            if best_class:

                detections_found += 1

                update_flagged_count(
                    detections_found
                )

            should_report = False

            if (
                best_severity == "VERY_HIGH"
                and copy_very_high
            ):
                should_report = True

            elif (
                best_severity == "HIGH"
                and copy_high           
            ):
                should_report = True
            elif (
                best_severity == "MEDIUM"
                and copy_medium           
            ):
                should_report = True

            elif (
                best_severity == "LOW"
                and copy_low
            ):
                should_report = True

            if should_report:

                image_uri = file.resolve().as_uri()

                detections.append(
                    Detection(
                        file_path=file,
                        severity=best_severity,
                        detection_class=best_class,
                        score=best_score,
                        file_name=file.name,
                        width=candidate.width,
                        height=candidate.height
                    )
                )
                flagged_count += 1

                update_flagged_count(flagged_count)
                
        update_scan_count(
            count
        )
        update_progress(
            count,
            len(candidates)
        )   

    stats = {
        "scanned": count,
        "flagged": detections_found,
        "threshold": threshold
    }

    generate_html_report(
        html_path,
        detections,
        stats
    )

    callback(
        f"NSFW Scanning finished"
    )

    callback(
        "__SCAN_COMPLETE__"
    )

def prune_dirs(root, dirs):

    dirs[:] = [
        d for d in dirs
        if d.lower() not in EXCLUDED_FOLDERS
    ]
