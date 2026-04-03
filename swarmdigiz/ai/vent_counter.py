import numpy as np
from PIL import Image
from scipy.ndimage import label

def detect_vent_count(uploaded_file):
    """
    Basic vent detection based on dark rectangular regions.
    This is a lightweight heuristic approach.
    """

    image = Image.open(uploaded_file).convert("L")
    img = np.array(image)

    # threshold to isolate darker vent areas
    threshold = img < 80

    labeled, count = label(threshold)

    # basic filtering to avoid noise
    vent_estimate = max(1, min(count // 500, 20))

    return {
        "vent_count": int(vent_estimate),
        "confidence": "experimental"
    }