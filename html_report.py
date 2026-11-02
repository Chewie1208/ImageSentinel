#from pathlib import Path

def generate_html_report(
    html_path,
    detections,
    stats
):

    cards = []

    for detection in detections:

        image_uri = (
            detection.file_path
            .resolve()
            .as_uri()
        )

        file_name = detection.file_path.name

        cards.append(
            f"""
            <div class="card {detection.severity.lower()}">

                <a href="{image_uri}" target="_blank">

                    <img
                        src="{image_uri}"
                        loading="lazy"
                        alt="{file_name}">

                </a>

                <div class="details">

                    <div class="severity">
                        {detection.severity}
                    </div>

                    <div class="classification">
                        {detection.detection_class}
                    </div>

                    <div class="score">
                        Score: {detection.score:.2f}
                    </div>

                    <div class="dimensions">
                        {detection.width:,} × {detection.height:,}
                    </div>

                    <div class="filename">
                        {file_name}
                    </div>

                    <div class="filepath">
                        {detection.file_path}
                    </div>

                </div>

                <div class="actions">

                    <a
                        href="{image_uri}"
                        target="_blank"
                        class="button">

                        Open Original

                    </a>

                    <label>

                        <input
                            type="checkbox"
                            class="delete-marker"
                            data-path="{detection.file_path}">

                        Mark for deletion

                    </label>

                </div>

            </div>
            """
        )

    html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<title>
Image Sentinel Review
</title>

<style>

body {{

    margin: 0;

    background: #f5f6f8;

    font-family: Segoe UI, Arial, sans-serif;
}}

.header {{

    background: #1f2937;

    color: white;

    padding: 20px 30px;
}}

.stats {{

    display: flex;

    gap: 30px;

    margin-top: 10px;
}}

.stat {{

    font-size: 15px;
}}

.toolbar {{

    background: white;

    padding: 15px 20px;

    border-bottom: 1px solid #ddd;
}}

.gallery {{

    display: grid;

    grid-template-columns:
        repeat(
            auto-fill,
            minmax(350px, 1fr)
        );

    gap: 20px;

    padding: 20px;
}}

.card {{

    background: white;

    border-radius: 8px;

    overflow: hidden;

    box-shadow:
        0 2px 8px rgba(0,0,0,0.12);
}}

.card img {{

    width: 100%;

    height: 260px;

    object-fit: cover;

    display: block;
}}

.details {{

    padding: 15px;
}}

.severity {{

    font-weight: bold;

    font-size: 16px;

    margin-bottom: 5px;
}}

.classification {{

    font-size: 14px;

    margin-bottom: 5px;
}}

.score {{

    margin-bottom: 5px;
}}

.dimensions {{

    margin-bottom: 5px;

    color: #666;
}}

.filename {{

    font-weight: bold;

    margin-bottom: 5px;
}}

.filepath {{

    font-size: 11px;

    color: #777;

    word-break: break-word;
}}

.actions {{

    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 15px;

    border-top: 1px solid #eee;
}}

.button {{

    background: #0078d4;

    color: white;

    text-decoration: none;

    padding: 8px 12px;

    border-radius: 4px;
}}

.very_high {{
    border-top: 8px solid #8b0000;
}}

.high {{
    border-top: 8px solid #d13438;
}}

.medium {{
    border-top: 8px solid #ff8c00;
}}

.low {{
    border-top: 8px solid #2e8b57;
}}

</style>

</head>

<body>

<div class="header">

    <h1>
        Image Sentinel Review
    </h1>

    <div class="stats">

        <div class="stat">
            Scanned:
            {stats['scanned']:,}
        </div>

        <div class="stat">
            Flagged:
            {stats['flagged']:,}
        </div>

        <div class="stat">
            Threshold:
            {stats['threshold']}
        </div>

    </div>

</div>

<div class="gallery">

{''.join(cards)}

</div>

</body>

</html>
"""

    with open(
        html_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)