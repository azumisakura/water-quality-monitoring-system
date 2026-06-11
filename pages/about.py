import streamlit as st
import base64
import os
from components.navbar import show_navbar

show_navbar()

def get_base64_img(image_path):
    """Safely converts local image to base64 string."""
    # Fallback placeholder if the file is completely missing
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
img_base64 = get_base64_img("static/water-bg.jpg")
if img_base64:
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.6)), url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
else:
    st.error(
        "Error: Could not find 'water-bg.jpg'. Place it next to your python script."
    )

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

with open("styles/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# --- FULL WIDTH TOP HERO ---
st.html(
    f"""
    <div style="
        background-color: #2563eb; color: white !important; width: 100%; border-radius: 8px; padding: 12px 20px; 
        font-size: 22px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; box-sizing: border-box;
        margin-bottom: 1rem
    ">
        ℹ️ About the System
    </div>
    """
)

st.markdown(
    f"""
    <div style="text-align:center; margin-bottom: 2.5rem; color: inherit;">
        <p style="font-size:17px; margin-bottom: 12px;">
            <b>Water Quality Monitoring, Classification, and Visualization System</b>
        </p>
        <p style="font-size:15px; color: inherit; line-height: 1.6; max-width: 800px; margin: 0 auto;">
            This web-based system was developed to analyze and visualize the Imus Ambient Water Quality Dataset 
            collected from monitoring stations along the Imus River.
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)


# --- TWO COLUMN CONTENT SPLIT ---
col1, col2 = st.columns(2, gap="large")

with col1:
    # 2. Project Title Section
    st.html(
        f"""
        <div style="
            background-color: #2563eb; color: white !important; width: 100%; border-radius: 8px; padding: 12px 20px; 
            font-size: 18px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; box-sizing: border-box;
            margin-bottom: 1rem
        ">
            📖 Project Title
        </div>
        """
    )
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 2.5rem; color: inherit;">
            <p style="font-size:15px; line-height: 1.6;">
                Design and Development of a Data Mining and Visualization System for Environmental Impact Analysis using Imus' Ambient Water Quality Data
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # 4. Water Quality Parameters Section
    st.html(
        f"""
        <div style="
            background-color: #2563eb; color: white !important; width: 100%; border-radius: 8px; padding: 12px 20px; 
            font-size: 18px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; box-sizing: border-box;
            margin-bottom: 1rem
        ">
            🧪 Water Quality Parameters
        </div>
        """
    )
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 2.5rem; color: inherit;">
            <p style="font-size:15px; line-height: 1.9;">
                pH<br>
                Dissolved Oxygen (DO)<br>
                Biochemical Oxygen Demand (BOD)<br>
                Temperature<br>
                Total Suspended Solids (TSS)<br>
                Fecal Coliform<br>
                Nitrate (NO₃-N)<br>
                Phosphate (PO₄-P)
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # 6. Technologies Used Section
    st.html(
        f"""
        <div style="
            background-color: #2563eb; color: white !important; width: 100%; border-radius: 8px; padding: 12px 20px; 
            font-size: 18px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; box-sizing: border-box;
            margin-bottom: 1rem
        ">
            🛠 Technologies Used
        </div>
        """
    )
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 2.5rem; color: inherit;">
            <p style="font-size:15px; line-height: 1.9;">
                Python<br>
                Streamlit<br>
                Pandas<br>
                NumPy<br>
                Scikit-learn<br>
                Plotly<br>
                Supabase
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # 7. Dataset Source Section
    st.html(
        f"""
        <div style="
            background-color: #2563eb; color: white !important; width: 100%; border-radius: 8px; padding: 12px 20px; 
            font-size: 18px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; box-sizing: border-box;
            margin-bottom: 1rem
        ">
            📚 Dataset Source
        </div>
        """
    )
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 2.5rem; color: inherit;">
            <p style="font-size:15px; line-height: 1.6;">
                Imus Ambient Water Quality Dataset
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )


with col2:
    # 3. Objectives Section
    st.html(
        f"""
        <div style="
            background-color: #2563eb; color: white !important; width: 100%; border-radius: 8px; padding: 12px 20px; 
            font-size: 18px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; box-sizing: border-box;
            margin-bottom: 1rem
        ">
            🎯 Objectives
        </div>
        """
    )
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 2.5rem; color: inherit;">
            <p style="font-size:15px; line-height: 1.9;">
                • Process and organize water quality records.<br>
                • Classify water samples using machine learning.<br>
                • Visualize historical trends and patterns.<br>
                • Support environmental monitoring and decision-making.
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # 5. Machine Learning Algorithms Section
    st.html(
        f"""
        <div style="
            background-color: #2563eb; color: white !important; width: 100%; border-radius: 8px; padding: 12px 20px; 
            font-size: 18px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; box-sizing: border-box;
            margin-bottom: 1rem;
        ">
            🤖 Machine Learning Algorithms
        </div>
        """
    )
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 2.5rem; color: inherit;">
            <p style="font-size:15px; line-height: 1.9;">
                Logistic Regression<br>
                Decision Tree<br>
                Random Forest
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # 8. Researchers & Institution Section
    st.html(
        f"""
        <div style="
            background-color: #2563eb; color: white !important; width: 100%; border-radius: 8px; padding: 12px 20px; 
            font-size: 18px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; box-sizing: border-box;
            margin-bottom: 1rem
        ">
            👨‍💻 Researchers
        </div>
        """
    )
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 1.5rem; color: inherit;">
            <p style="font-size:15px; line-height: 1.9;">
                Theresa Julliana B. Dela Peña<br>
                Leivinze P. Lustico<br>
                Jeyleene Faith R. Palomares<br>
                Kirt Angelo D. Ramboyong<br>
                Chedrick L. Torres
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 2.5rem; color: inherit;">
            <p style="font-size:15px; line-height: 1.6;">
                <b>BS Computer Engineering</b><br>
                College of Engineering and Information Technology<br>
                Cavite State University – Main Campus<br>
                Academic Year 2025–2026
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
