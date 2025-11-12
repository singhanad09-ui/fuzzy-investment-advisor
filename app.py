# -----------------------------------------------------------------
# PROJECT: Fuzzy Investment Advisor - Remove Green Box
# FILE: app.py
# AUTHOR: (Your Name) / Gemini AI
# REQUIRES: pip install streamlit pandas plotly pillow
# -----------------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
from fuzzy_investment_engine import FuzzyInvestmentEngine, get_example_recommendations
from PIL import Image # Import Pillow for image handling

# --- กำหนดค่าเริ่มต้นและสไตล์ ---
st.set_page_config(
    page_title="FIA: Fuzzy Investment Advisor",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# โหลดโลโก้
try:
    logo = Image.open("fia_logo.png")
except FileNotFoundError:
    logo = None
    st.error("ไม่พบไฟล์ 'fia_logo.png' โปรดตรวจสอบไฟล์โลโก้ในโฟลเดอร์เดียวกับ app.py")

# Custom CSS (Green Theme - Adjusted for "light green" all over, compact layout, larger fonts, and prominent buttons)
st.markdown("""
<style>
    /* --- General Styling (Green Theme) --- */
    body, .stApp {
        background-color: #F0FDF4 !important; /* Lightest Green Background for ALL pages */
        color: #14532D !important; /* Dark Green Text */
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 1.05em; /* เพิ่มขนาดตัวอักษรพื้นฐาน */
    }
    .stApp > header {
        background-color: #14532D; /* Dark Green Header */
        color: white;
    }

    /* --- FIA Header for Input/Output Pages --- */
    .fia-header-container {
        display: flex;
        align-items: baseline; /* Align text baselines */
        width: 100%;
        padding-top: 0rem;
        padding-bottom: 0.5rem;
        margin-bottom: 15px; /* Add margin below header */
    }
    .fia-header-text {
        font-size: 2.7em; /* Larger FIA text */
        font-weight: bold;
        color: #22C55E; /* Medium Green (different color) */
        text-align: left;
        padding-left: 1rem;
        flex: 1; /* Take 1 part of space */
        line-height: 1.2; /* Adjust line height for alignment */
    }
    .fia-header-title {
        color: #14532D !important; /* Dark Green Title */
        font-size: 2.2em; /* Larger title font */
        font-weight: 600;
        text-align: center;
        flex: 2; /* Take 2 parts of space (center) */
        line-height: 1.2; /* Adjust line height for alignment */
    }
    .fia-header-spacer {
        flex: 1; /* Take 1 part of space (empty) */
    }

    /* --- Header Box (Used for home page only now) --- */
    .header-box {
        background-color: #14532D; /* Dark Green */
        color: white !important;
        padding: 18px; /* เพิ่ม padding */
        border-radius: 8px;
        text-align: center;
        font-size: 1.8em; /* เพิ่มขนาดตัวอักษร */
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .header-box * {
        color: white !important;
    }
    
    /* --- Home Page Logo Styling --- */
    .stImage {
        display: flex;
        justify-content: center; /* <<< (แก้ไข) ปรับให้กึ่งกลางเหมือนเดิม แต่จะแก้ที่ Column แทน */
        margin-top: 1rem;
        margin-bottom: 15px;
        width: 100%;
    }
    .stImage img {
        border-radius: 50% !important;
        object-fit: cover;
        width: 250px; /* <<< (แก้ไข) ขยายขนาดโลโก้หน้าแรกให้ใหญ่ขึ้นอีก */
        height: 250px;
        /* <<< (ลบ) border: 4px solid #22C55E; */ /* ลบขอบเขียวออก */
        /* <<< (ลบ) box-shadow: 0 6px 15px rgba(0,0,0,0.2); */ /* ลบเงาออก */
    }

    /* --- Titles and Headings --- */
    h1, h2, h3 {
        color: #14532D !important; /* Dark Green Titles */
        text-align: center;
        font-weight: 600;
    }
    h1 { font-size: 3.0em; padding-bottom: 15px; margin-top: 0; }
    h2 { font-size: 2.2em; margin-bottom: 15px; margin-top: 0; }
    h3 { 
        font-size: 1.6em; 
        margin-bottom: 0px; /* <<< (แก้ไข) ลดช่องว่างใต้ H3 */
        margin-top: 0; 
    }

    /* --- Text Alignment --- */
    .st-emotion-cache-16txtl3 { /* This is a common Streamlit container class */
        text-align: center;
    }
    .stRadio label, .stNumberInput label, .stSelectbox label, .stMarkdown p, [data-testid="stForm"] p {
        text-align: left !important;
        color: #14532D !important;
    }
    .disclaimer-box p {
        text-align: left !important;
    }

    /* --- Main Content Area - Reduced Padding --- */
    .reportview-container .main .block-container {
        padding-top: 0rem !important;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }

    /* --- Buttons --- */
    .stButton > button {
        background-color: #16A34A; /* Darker Green for more prominence */
        color: white !important;
        padding: 12px 28px; /* เพิ่ม padding ให้ปุ่มใหญ่ขึ้น */
        border: none;
        border-radius: 8px;
        text-align: center;
        font-size: 18px; /* เพิ่มขนาดตัวอักษรปุ่ม */
        margin: 8px 0; /* เพิ่ม margin */
        cursor: pointer;
        transition: 0.3s ease-in-out;
        box-shadow: 0 6px 15px rgba(0,0,0,0.15); /* เพิ่มเงาให้ปุ่มเด่นขึ้น */
        width: 100%;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #10B981; /* สีเขียวอ่อนลงเมื่อ hover */
        box-shadow: 0 8px 18px rgba(0,0,0,0.2); /* เงามากขึ้นเมื่อ hover */
    }

    /* --- Input Widgets --- */
    .stNumberInput > label, .stRadio > label, .stSelectbox > label, .stSlider > label {
        color: #14532D !important;
        font-weight: bold;
        margin-bottom: 5px;
        text-align: left !important;
        font-size: 1.1em;
    }
    /* --- (แก้ไข) เปลี่ยนพื้นหลัง Input Box --- */
    .stNumberInput input, .stSelectbox [data-testid="stSelectboxContainer"] div[role="button"] {
        background-color: #D1FAE5 !important; /* <<< (แก้ไข) เปลี่ยนจาก #FFFFFF เป็นสีเขียวอ่อน */
        border: 1px solid #A3E635 !important; /* Lime green border */
        border-radius: 5px !important;
        color: #14532D !important;
        padding: 8px 12px;
        font-size: 1.0em;
    }
    /* --- (สิ้นสุดส่วนที่แก้ไข) --- */
    
    .stRadio div[role="radiogroup"] {
        background-color: #D1FAE5; /* Light Green */
        border-radius: 5px;
        padding: 10px;
        margin-top: 5px;
        margin-bottom: 15px;
    }
    .stRadio div[role="radiogroup"] span {
        font-weight: bold;
        color: #14532D;
        font-size: 1.0em;
    }

    /* --- Output Box --- */
    .output-box {
        background-color: transparent !important; /* <<< (แก้ไข) ลบกล่องเขียวอ่อน */
        padding: 0px; /* <<< (แก้ไข) ลบ padding */
        margin-top: 0px; /* <<< (แก้ไข) ลบ margin */
        text-align: left;
        box-shadow: none; /* <<< (แก้ไข) ลบเงา */
        height: 100%;
    }
    .output-box h3 {
        text-align: left !important;
        font-size: 1.5em;
        margin-bottom: 5px; /* <<< (แก้ไข) ลดช่องว่างด้านล่าง */
    }
    .output-box p {
        font-size: 1.0em;
        line-height: 1.7;
        text-align: left !important;
        margin-bottom: 8px;
    }

    /* --- Columns Styling --- */
    [data-testid="stColumn"] {
        padding: 12px;
        border-radius: 10px;
        background-color: transparent !important;
        height: 100%;
        box-shadow: none !important;
    }
    [data-testid="stColumn"]:first-child {
        margin-right: 0px;
    }

    /* --- Disclaimer Box --- */
    .disclaimer-box {
        background-color: #FEFCE8; /* Light Yellow */
        border-left: 5px solid #FACC15; /* Yellow */
        padding: 15px;
        border-radius: 5px; 
        margin-top: 25px;
        margin-bottom: 15px;
        color: #856404;
        text-align: left !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .disclaimer-box p {
        font-size: 0.9em;
        margin-bottom: 3px;
        text-align: left !important;
    }
    .disclaimer-box p.bold-text {
        font-weight: bold; 
        margin-bottom: 5px;
        text-align: left !important;
    }

</style>
""", unsafe_allow_html=True)


# --- กำหนดสถานะของหน้า (เพื่อจำว่าอยู่หน้าไหน) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'portfolio_results' not in st.session_state:
    st.session_state.portfolio_results = None
if 'example_recommendations' not in st.session_state:
    st.session_state.example_recommendations = None
if 'risk_level_text' not in st.session_state:
    st.session_state.risk_level_text = ""
if 'user_age_input' not in st.session_state: st.session_state.user_age_input = 30
if 'user_income_input' not in st.session_state: st.session_state.user_income_input = 50000
if 'user_time_horizon_input' not in st.session_state: st.session_state.user_time_horizon_input = 10
if 'user_risk_tolerance_input' not in st.session_state: st.session_state.user_risk_tolerance_input = 6

# --- หน้า Home ---
def home_page():
    
    if logo:
        # --- (แก้ไข) ปรับอัตราส่วนคอลัมน์เพื่อขยับโลโก้ไปขวา ---
        # 2 ส่วนซ้าย (ว่าง), 2 ส่วนกลาง (โลโก้), 1 ส่วนขวา (ว่าง)
        col_logo_left, col_logo_center, col_logo_right = st.columns([2, 2, 1]) 
        with col_logo_center:
            st.image(logo)
    else:
        st.markdown("<h1 style='text-align: center;'>FIA: Fuzzy Investment Advisor</h1>", unsafe_allow_html=True)

    st.markdown('<div class="header-box">FIA: Fuzzy Investment Advisor</div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>ระบบผู้ช่วยประเมินและแนะนำการลงทุนอัจฉริยะด้วย AI (Fuzzy Logic)</h3>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="disclaimer-box">
            <p class="bold-text">ข้อควรทราบ:</p>
            <p>
            FIA เป็นเพียงเครื่องมือช่วยวิเคราะห์เบื้องต้นจากข้อมูลที่คุณให้ 
            ผลลัพธ์ที่ได้ไม่ใช่คำแนะนำการลงทุนที่สมบูรณ์แบบ 
            และไม่ควรถือเป็นการชี้นำในการตัดสินใจลงทุน 
            การลงทุนมีความเสี่ยง ผู้ลงทุนควรศึกษาข้อมูลให้เข้าใจก่อนตัดสินใจลงทุนทุกครั้ง 
            และปรึกษาผู้เชี่ยวชาญหากมีข้อสงสัย
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("เริ่มประเมินพอร์ต"):
            st.session_state.page = 'input'
            st.rerun()
            

# --- หน้า Input ---
def input_page():
    # --- ใช้ Header แบบใหม่ที่ปรับแล้ว ---
    st.markdown(f"""
        <div class="fia-header-container">
            <span class="fia-header-text">FIA</span>
            <h2 class="fia-header-title">ประเมินพอร์ตลงทุน</h2>
            <span class="fia-header-spacer">&nbsp;</span>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("investment_form"):
        age_options = list(range(7, 100))
        age = st.selectbox("อายุ", options=age_options, index=age_options.index(st.session_state.user_age_input))

        income = st.number_input("รายได้ต่อเดือน (บาท)", min_value=15000, max_value=500000, value=st.session_state.user_income_input, step=1000)
        time_horizon = st.number_input("ระยะเวลาการลงทุน (ปี)", min_value=1, max_value=30, value=st.session_state.user_time_horizon_input, step=1)
        
        st.write("ระดับความเสี่ยงที่ยอมรับได้")
        risk_map = {"ต่ำ": 3, "ปานกลาง": 6, "สูง": 8}
        
        current_risk_text = "ปานกลาง"
        if st.session_state.user_risk_tolerance_input == 3: current_risk_text = "ต่ำ"
        elif st.session_state.user_risk_tolerance_input == 8: current_risk_text = "สูง"

        selected_risk_text = st.radio("", ["ต่ำ", "ปานกลาง", "สูง"], index=["ต่ำ", "ปานกลาง", "สูง"].index(current_risk_text), horizontal=True)
        risk_tolerance = risk_map[selected_risk_text]

        submitted = st.form_submit_button("ประเมินคำแนะนำ")
        if submitted:
            st.session_state.user_age_input = age
            st.session_state.user_income_input = income
            st.session_state.user_time_horizon_input = time_horizon
            st.session_state.user_risk_tolerance_input = risk_tolerance

            engine = FuzzyInvestmentEngine()
            portfolio_results = engine.calculate_portfolio(age, income, time_horizon, risk_tolerance)
            
            if portfolio_results:
                example_recommendations = get_example_recommendations(
                    portfolio_results['equity'],
                    portfolio_results['bonds'],
                    portfolio_results['cash']
                )

                if portfolio_results['equity'] > 70:
                    risk_level_text = "สูง"
                elif portfolio_results['equity'] > 40:
                    risk_level_text = "ปานกลาง"
                else:
                    risk_level_text = "ต่ำ"

                st.session_state.portfolio_results = portfolio_results
                st.session_state.example_recommendations = example_recommendations
                st.session_state.risk_level_text = risk_level_text
                st.session_state.page = 'output'
                st.rerun()

# --- หน้า Output (Layout ใหม่) ---
def output_page():
    # --- ใช้ Header แบบใหม่ที่ปรับแล้ว ---
    st.markdown(f"""
        <div class="fia-header-container">
            <span class="fia-header-text">FIA</span>
            <h2 class="fia-header-title">ผลการประเมินและคำแนะนำพอร์ตลงทุน</h2>
            <span class="fia-header-spacer">&nbsp;</span>
        </div>
    """, unsafe_allow_html=True)
    
    if (st.session_state.portfolio_results is None or 
        st.session_state.example_recommendations is None or
        st.session_state.risk_level_text == ""):
        
        st.warning("กรุณากรอกข้อมูลในหน้า 'ประเมินพอร์ตลงทุน' และกดประเมินก่อนครับ")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("ไปหน้าประเมิน"):
                st.session_state.page = 'input'
                st.rerun()
        return

    portfolio = st.session_state.portfolio_results
    examples = st.session_state.example_recommendations
    risk_text = st.session_state.risk_level_text

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<h3>ระดับความเสี่ยงของคุณ: <span style='color:#16A34A;'>{risk_text}</span></h3>", unsafe_allow_html=True)

        df = pd.DataFrame({
            'Asset': ['หุ้น', 'พันธบัตร', 'เงินฝาก'],
            'Percentage': [portfolio['equity'], portfolio['bonds'], portfolio['cash']]
        })

        fig = px.pie(
            df, 
            values='Percentage', 
            names='Asset', 
            color_discrete_sequence=['#16A34A', '#6EE7B7', '#A7F3D0'], # Green Palette
            hole=0.5
        )
        fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=2)))
        fig.update_layout(
            showlegend=True, 
            height=350, 
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#14532D')
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<h3>คำแนะนำการลงทุน</h3>", unsafe_allow_html=True)
        
        st.markdown('<div class="output-box">', unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>เหมาะสำหรับพอร์ตการลงทุนแบบ: <span style='color:#16A34A;'>{examples['portfolio_type']}</span></h3>", unsafe_allow_html=True)
        st.write(f"**คำแนะนำสัดส่วน (จาก AI):**")
        st.write(f"- หุ้น (Equity): `{portfolio['equity']:.1f}%`")
        st.write(f"- พันธบัตร (Bonds): `{portfolio['bonds']:.1f}%`")
        st.write(f"- เงินฝาก (Cash): `{portfolio['cash']:.1f}%`")

        st.write(f"**ตัวอย่างสินทรัพย์:**")
        st.write(f"- **หุ้น:** {', '.join(examples['equity_examples'])}")
        st.write(f"- **พันธบัตร:** {', '.join(examples['bonds_examples'])}")
        st.write(f"- **เงินฝาก:** {', '.join(examples['cash_examples'])}")

        st.markdown('</div>', unsafe_allow_html=True)

    # --- (ลบ) st.write("") ออกแล้ว ---
    
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
    with col_btn2:
        if st.button("กลับหน้าหลัก"):
            st.session_state.page = 'home'
            st.rerun()
            
    st.markdown(
        """
        <div class="disclaimer-box">
            <p class="bold-text">ข้อควรทราบ:</p>
            <p>
            FIA เป็นเพียงเครื่องมือช่วยวิเคราะห์เบื้องต้นจากข้อมูลที่คุณให้ 
            ผลลัพธ์ที่ได้ไม่ใช่คำแนะนำการลงทุนที่สมบูรณ์แบบ 
            และไม่ควรถือเป็นการชี้นำในการตัดสินใจลงทุน 
            การลงทุนมีความเสี่ยง ผู้ลงทุนควรศึกษาข้อมูลให้เข้าใจก่อนตัดสินใจลงทุนทุกครั้ง 
            และปรึกษาผู้เชี่ยวชาญหากมีข้อสงสัย
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# --- Logic การแสดงหน้าเพจ ---
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'input':
    input_page()
elif st.session_state.page == 'output':
    output_page()