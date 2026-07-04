import streamlit as st
from PIL import Image

from modules.vision_detection import detect_hazards
from modules.risk_engine import RiskEngine
from modules.control_generator import ControlGenerator
from modules.report_generator import ReportGenerator

st.set_page_config(page_title="EHS Smart Inspection", layout="wide")

st.title("🏭 AI-Powered EHS Smart Inspection System")
st.write("Industrial Safety Inspection Platform (ISO 45001 aligned)")

# 初始化类（关键！！！）
risk_engine = RiskEngine()
control_generator = ControlGenerator()
report_generator = ReportGenerator()

uploaded_file = st.file_uploader("Upload factory inspection image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Inspection Image", use_container_width=True)

    st.success("Running EHS analysis...")

    # 1. hazard detection
    hazards = detect_hazards(image)

    st.subheader("🚨 Detected Hazards")
    for h in hazards:
        st.write(f"- {h}")

    # 2. risk processing（关键修复）
    processed_hazards = risk_engine.process_hazards(hazards)

    st.subheader("📊 Risk Assessment")
    for r in processed_hazards:
        st.write(r)

    # 3. controls（关键修复）
    controls = control_generator.generate_all_controls(processed_hazards)

    st.subheader("🛠 Control Measures")
    for c in controls:
        st.write(c)

    # 4. summary（新增，推荐）
    risk_summary = risk_engine.get_risk_summary(processed_hazards)

    # 5. report（关键修复）
    report = report_generator.generate_report(
        risk_summary,
        processed_hazards,
        controls
    )

    st.subheader("📄 EHS Report")
    st.text(report)
