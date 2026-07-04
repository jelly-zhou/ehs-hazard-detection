import streamlit as st
from PIL import Image

from modules.vision_detection import detect_hazards
from modules.risk_engine import calculate_risk
from modules.control_generator import generate_controls
from modules.report_generator import generate_report

st.set_page_config(page_title="EHS Smart Inspection", layout="wide")

st.title("🏭 AI-Powered EHS Smart Inspection System")
st.write("Industrial Safety Inspection Platform (ISO 45001 aligned)")

# 上传图片
uploaded_file = st.file_uploader("Upload factory inspection image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Inspection Image", use_container_width=True)

    st.success("Running EHS analysis...")

    # =========================
    # 1. hazard detection
    # =========================
    hazards = detect_hazards(image)

    st.subheader("🚨 Detected Hazards")
    for h in hazards:
        st.write(f"- {h}")

    # =========================
    # 2. risk engine
    # =========================
    risks = calculate_risk(hazards)

    st.subheader("📊 Risk Assessment")

    for r in risks:
        st.write(r)

    # =========================
    # 3. control measures
    # =========================
    controls = generate_controls(hazards)

    st.subheader("🛠 Control Measures")

    for c in controls:
        st.write(c)

    # =========================
    # 4. report
    # =========================
    report = generate_report(hazards, risks, controls)

    st.subheader("📄 EHS Report")
    st.text(report)
