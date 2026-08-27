import streamlit as st
import requests

st.set_page_config(
    page_title="HealthyBite AI",
    page_icon="🥗",
    layout="wide"
)

# ==========================================================
# GRADIO API URL
# ==========================================================

GRADIO_URL ="https://872d88b9aacff067fa.gradio.live"


# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

.stApp {
    background:
    linear-gradient(
        135deg,
        #fffdf3,
        #f0fff4
    );
}

.title {
    text-align:center;
    font-size:48px;
    font-weight:800;
    padding:20px;
}

.subtitle {
    text-align:center;
    color:#666;
    font-size:18px;
    margin-bottom:30px;
}

.card {
    background:white;
    padding:25px;
    border-radius:22px;
    margin-bottom:20px;
    border:1px solid #eeeeee;
    box-shadow:0 8px 25px rgba(0,0,0,0.06);
}

.bmi {
    padding:25px;
    border-radius:20px;
    text-align:center;
    background:#eaf8ed;
}

.bmi-number {
    font-size:55px;
    font-weight:800;
}

.ai-result {
    background:white;
    padding:30px;
    border-radius:22px;
    border:1px solid #eeeeee;
    line-height:1.8;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    '<div class="title">🥗 HealthyBite AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Personalized Health & Diet Planner'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================================
# INPUT
# ==========================================================

st.markdown(
    '<div class="card">',
    unsafe_allow_html=True
)

st.subheader("👤 Personal Information")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Name",
        placeholder="Enter your name"
    )

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=18
    )

    height = st.number_input(
        "Height (cm)",
        min_value=50.0,
        max_value=250.0,
        value=165.0
    )

with col2:

    weight = st.number_input(
        "Weight (kg)",
        min_value=10.0,
        max_value=300.0,
        value=60.0
    )

    months = st.selectbox(
        "Diet Plan Duration",
        [
            "1 Month",
            "2 Months",
            "3 Months",
            "4 Months",
            "5 Months"
        ]
    )

    health = st.text_area(
        "Health Update",
        placeholder="Enter your health information"
    )

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ==========================================================
# BMI
# ==========================================================

height_m = height / 100

bmi = weight / (height_m * height_m)

if bmi < 18.5:
    category = "Underweight"
elif bmi < 25:
    category = "Healthy Range"
elif bmi < 30:
    category = "Overweight Range"
else:
    category = "Higher BMI Range"


# ==========================================================
# BUTTON
# ==========================================================

if st.button(
    "🤖 ANALYSE WITH HEALTHYBITE AI",
    type="primary",
    use_container_width=True
):

    if not name:

        st.error("Please enter your name.")

    else:

        # ==================================================
        # BMI RESULT
        # ==================================================

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader("🧮 BMI Analysis")

        st.markdown(
            f"""
            <div class="bmi">

                <div>BMI</div>

                <div class="bmi-number">
                    {bmi:.1f}
                </div>

                <strong>
                    {category}
                </strong>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


        # ==================================================
        # SEND TO GRADIO
        # ==================================================

        with st.spinner(
            "🤖 Connecting to HealthyBite AI..."
        ):

            try:

                response = requests.post(

                    f"{GRADIO_URL}/api/predict",

                    json={
                        "name": name,
                        "age": age,
                        "height": height,
                        "weight": weight,
                        "health": health,
                        "months": months,
                        "bmi": bmi,
                        "category": category
                    },

                    timeout=60
                )


                # ==========================================
                # SUCCESS
                # ==========================================

                if response.status_code == 200:

                    data = response.json()

                    result = data.get(
                        "result",
                        "No result returned."
                    )

                    st.markdown(
                        '<div class="card">',
                        unsafe_allow_html=True
                    )

                    st.subheader(
                        "🤖 AI Personalized Plan"
                    )

                    st.markdown(
                        f"""
                        <div class="ai-result">

                        {result}

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

                else:

                    st.error(
                        f"Gradio returned HTTP "
                        f"{response.status_code}"
                    )


            except requests.exceptions.RequestException as e:

                st.error(
                    "Could not connect to the Gradio server."
                )

                st.code(str(e))


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("""
<div style="
text-align:center;
padding:30px;
color:#777;
">

🥗 HealthyBite AI

<br>

Python • Streamlit • Gradio • Hugging Face

<br><br>

Educational Student Project

</div>
""", unsafe_allow_html=True)
