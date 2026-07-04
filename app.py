import streamlit as st
from PIL import Image

# ====== OOP模块（关键修复点）======
from modules.vision_detection import HazardDetector
from modules.risk_engine import RiskEngine
from modules.control_generator import ControlGenerator
from modules.report_generator import ReportGenerator

st.set_page_config(page_title="EHS Smart Inspection", layout="wide")

st.title("🏭 AI-Powered EHS Smart Inspection System")
st.write("Industrial Safety Inspection Platform (ISO 45001 Aligned)")

# =========================
# 初始化系统（关键）
# =========================
detector = HazardDetector()
risk_engine = RiskEngine()
control_generator = ControlGenerator()
report_generator = ReportGenerator()

# =========================
# 上传图片
# =========================
uploaded_file = st.file_uploader(
    "Upload factory inspection image",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file:

    # 读取图片
    image = Image.open(uploaded_file)
    st.image(image, caption="Inspection Image", use_container_width=True)

    st.success("Running AI-EHS analysis...")

    # =========================
    # 1. Hazard Detection
    # =========================
    hazards = detector.detect_hazards(image)

    st.subheader("🚨 Detected Hazards")

    if not hazards:
        st.info("No hazards detected.")
    else:
        for h in hazards:
            st.write(h)

    # =========================
    # 2. Risk Analysis
    # =========================
    processed_risks = risk_engine.process_hazards(hazards)

    st.subheader("📊 Risk Assessment")

    if not processed_risks:
        st.info("No risk data generated.")
    else:
        for r in processed_risks:
            st.write(r)

    # =========================
    # 3. Control Measures
    # =========================
    controls = control_generator.generate_all_controls(processed_risks)

    st.subheader("🛠 Control Measures")

    if not controls:
        st.info("No control measures generated.")
    else:
        for c in controls:
            st.write(c)

    # =========================
    # 4. Report Generation
    # =========================
    risk_summary = risk_engine.get_risk_summary(processed_risks)

    report = report_generator.generate_report(
        risk_summary,
        processed_risks,
        controls
    )

    st.subheader("📄 EHS Report")
    st.text(report)
