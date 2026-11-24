import cv2
import numpy as np


def compare_images(reference_rgb, inspected_rgb, sensitivity=25, min_area=100):
    """
    Compare a test image with a known-good reference image.

    This is a classical computer-vision baseline, not a trained defect classifier.
    Images are resized to the same dimensions; consistent camera position and lighting
    are important for meaningful results.
    """
    if reference_rgb is None or inspected_rgb is None:
        raise ValueError("Both reference and inspected images are required.")

    height, width = reference_rgb.shape[:2]
    inspected = cv2.resize(inspected_rgb, (width, height), interpolation=cv2.INTER_AREA)

    reference_gray = cv2.cvtColor(reference_rgb, cv2.COLOR_RGB2GRAY)
    inspected_gray = cv2.cvtColor(inspected, cv2.COLOR_RGB2GRAY)

    # Reduce small sensor noise before comparing the images.
    reference_blur = cv2.GaussianBlur(reference_gray, (5, 5), 0)
    inspected_blur = cv2.GaussianBlur(inspected_gray, (5, 5), 0)

    difference = cv2.absdiff(reference_blur, inspected_blur)
    _, mask = cv2.threshold(difference, int(sensitivity), 255, cv2.THRESH_BINARY)

    # Remove isolated noise and join nearby pixels belonging to one region.
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    annotated = inspected.copy()
    regions = []
    total_area = 0

    for contour in contours:
        area = int(cv2.contourArea(contour))
        if area < int(min_area):
            continue

        x, y, w, h = cv2.boundingRect(contour)
        total_area += area
        regions.append({
            "x": int(x),
            "y": int(y),
            "width": int(w),
            "height": int(h),
            "area": area
        })
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (255, 0, 0), 2)

    difference_percent = (total_area / float(width * height)) * 100.0
    status = "REVIEW REQUIRED" if regions else "NO SIGNIFICANT DIFFERENCE"

    # Convert RGB annotated output to JPEG bytes for Streamlit download.
    bgr = cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR)
    success, encoded = cv2.imencode(".jpg", bgr)
    if not success:
        raise RuntimeError("Could not encode inspection image.")

    return {
        "status": status,
        "difference_percent": difference_percent,
        "region_count": len(regions),
        "regions": regions,
        "annotated": annotated,
        "annotated_bytes": encoded.tobytes()
    }
