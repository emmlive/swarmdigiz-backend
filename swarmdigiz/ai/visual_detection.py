import numpy as np
from PIL import Image

def analyze_image_condition(uploaded_file):
    """
    Simple AI-style image analysis for cleaning severity.
    """

    image = Image.open(uploaded_file).convert("L")
    img_array = np.array(image)

    brightness = np.mean(img_array)
    texture = np.std(img_array)

    severity_score = 0

    if brightness < 90:
        severity_score += 40

    if texture > 40:
        severity_score += 30

    severity_score = min(100, severity_score)

    if severity_score < 30:
        condition = "clean"
    elif severity_score < 60:
        condition = "moderate"
    else:
        condition = "heavy"

    return {
        "severity_score": int(severity_score),
        "condition": condition
    }