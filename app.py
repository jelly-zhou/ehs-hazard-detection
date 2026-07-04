import streamlit as st
from PIL import Image

# ====== OOP模块 ======
from modules.vision_detection import HazardDetector
from modules.risk_engine import RiskEngine
from modules.control_generator import ControlGenerator
from modules.report_generator import ReportGenerator

# =========================
# 页面配置
# =========================
st.set_page_config(page_title="EHS Smart Inspection", layout="wide")

st.title("🏭 AI-Powered EHS Smart Inspection System")
st.write("Industrial Safety Inspection Platform (ISO 45001 Aligned)")

# =========================
# 初始化系统（只初始化一次更安全）
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

# =========================
# 主流程
# =========================
if uploaded_file:

    try:
        # 1. 读取图片（强制RGB防炸）
        image = Image.open(uploaded_file).convert("RGB")

        st.image(image, caption="Inspection Image")

        st.success("Running AI-EHS analysis...")

        # =========================
        # 2. Hazard Detection
        # =========================
        hazards = detector.detect_hazards(image)

        st.subheader("🚨 Detected Hazards")

        if hazards:
            for h in hazards:
                st.write(h)
        else:
            st.info("No hazards detected.")

        # =========================
        # 3. Risk Analysis
        # =========================
        processed_risks = risk_engine.process_hazards(hazards)

        st.subheader("📊 Risk Assessment")

        if processed_risks:
            for r in processed_risks:
                st.write(r)
        else:
            st.info("No risk data generated.")

        # =========================
        # 4. Control Measures
        # =========================
        controls = control_generator.generate_all_controls(processed_risks)

        st.subheader("🛠 Control Measures")

        if controls:
            for c in controls:
                st.write(c)
        else:
            st.info("No control measures generated.")

        # =========================
        # 5. Report Generation
        # =========================
        risk_summary = risk_engine.get_risk_summary(processed_risks)

        report = report_generator.generate_report(
            risk_summary,
            processed_risks,
            controls
        )

        st.subheader("📄 EHS Report")
        st.text(report)

    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
