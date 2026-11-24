import streamlit as st
import cv2
import numpy as np
from PIL import Image
from detector import compare_images

st.set_page_config(page_title="Industrial Defect Inspection", page_icon="🔎", layout="wide")
st.title("Industrial Defect Detection & Quality-Control Assistant")
st.caption("PS5 prototype | Reference-image comparison baseline")

st.info(
    "Prototype note: This version compares an inspected product image with a known-good "
    "reference image. It highlights visual differences; it is not a trained industrial AI "
    "model and must be validated on real production data before operational use."
)

col1, col2 = st.columns(2)
with col1:
    reference_file = st.file_uploader("Upload a GOOD reference image", type=["png", "jpg", "jpeg"])
with col2:
    test_file = st.file_uploader("Upload the image to inspect", type=["png", "jpg", "jpeg"])

sensitivity = st.slider("Detection sensitivity", min_value=5, max_value=80, value=25, step=5)
min_area = st.slider("Minimum highlighted region (pixels)", min_value=10, max_value=1000, value=100, step=10)

if reference_file and test_file:
    reference = np.array(Image.open(reference_file).convert("RGB"))
    inspected = np.array(Image.open(test_file).convert("RGB"))

    result = compare_images(reference, inspected, sensitivity=sensitivity, min_area=min_area)

    st.subheader("Inspection result")
    a, b, c = st.columns(3)
    a.metric("Status", result["status"])
    b.metric("Difference area", f'{result["difference_percent"]:.2f}%')
    c.metric("Regions detected", result["region_count"])

    left, right = st.columns(2)
    with left:
        st.image(reference, caption="Good reference image", use_container_width=True)
    with right:
        st.image(inspected, caption="Inspected product image", use_container_width=True)

    st.image(result["annotated"], caption="Potential defect regions highlighted", use_container_width=True)

    if result["region_count"] > 0:
        st.warning("Visual differences were found. Review the highlighted areas manually.")
        for index, region in enumerate(result["regions"], start=1):
            st.write(
                f"Region {index}: x={region['x']}, y={region['y']}, "
                f"width={region['width']}, height={region['height']}, "
                f"area={region['area']} px"
            )
    else:
        st.success("No significant visual differences were detected at the selected sensitivity.")

    st.download_button(
        "Download annotated inspection image",
        data=result["annotated_bytes"],
        file_name="inspection_result.jpg",
        mime="image/jpeg"
    )
else:
    st.write("Upload both images to run an inspection.")
    st.write("Tip: use images of the same product, camera angle, lighting and scale.")
