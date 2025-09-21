import streamlit as st
import pandas as pd
import pickle
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="Fish Species Predictor",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for Styling ---
def load_css():
    """Loads custom CSS for styling the app."""
    st.markdown("""
        <style>
            /* --- General Styles --- */
            body {
                color: #333;
                background-color: #f0f2f6;
            }

            /* --- Main Content Area --- */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                padding-left: 5rem;
                padding-right: 5rem;
            }

            /* --- Sidebar Styles --- */
            .st-emotion-cache-16txtl3 {
                background-color: #ffffff;
                border-right: 1px solid #e6e6e6;
            }

            /* --- Header/Navbar --- */
            .header {
                padding: 10px 20px;
                background-color: #ffffff;
                color: #333;
                border-bottom: 1px solid #e6e6e6;
                text-align: center;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                z-index: 1000;
                box-shadow: 0 2px 4px 0 rgba(0,0,0,0.1);
            }
            .header h1 {
                margin: 0;
                font-size: 2.5rem;
                font-weight: 700;
            }

            /* --- Footer --- */
            .footer {
                padding: 10px 20px;
                background-color: #ffffff;
                color: #333;
                text-align: center;
                border-top: 1px solid #e6e6e6;
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                z-index: 1000;
                box-shadow: 0 -2px 4px 0 rgba(0,0,0,0.1);
            }

            /* --- Input Widgets --- */
            .st-emotion-cache-16txtl3 .stNumberInput, .st-emotion-cache-16txtl3 .stTextInput {
                margin-bottom: 1rem;
            }
            
            /* --- Buttons --- */
            .stButton>button {
                border-radius: 20px;
                border: 1px solid #4CAF50;
                background-color: #4CAF50;
                color: white;
                padding: 10px 24px;
                cursor: pointer;
                width: 100%;
                font-size: 1.1rem;
                font-weight: bold;
                transition: all 0.3s ease-in-out;
            }
            .stButton>button:hover {
                background-color: #45a049;
                border-color: #45a049;
            }
            
            /* --- Prediction Box --- */
            .prediction-box {
                background-color: #ffffff;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
                text-align: center;
                margin-top: 2rem;
            }
            .prediction-box h2 {
                color: #4CAF50;
                font-size: 2rem;
            }

        </style>
    """, unsafe_allow_html=True)

# --- Image to Base64 ---
def get_image_as_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# --- Load The Model ---
model = None
try:
    with open('Random Forest_best_model.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("❌ **Model file not found!**")
    st.info("Please make sure 'Random Forest_best_model.pkl' is in the same directory as 'app.py'.")
    st.stop()
except Exception as e:
    st.error("❌ **Error Loading Model**")
    st.error("This app cannot function because the machine learning model could not be loaded.")
    st.warning(
        """
        This issue is typically caused by a mismatch between the Python library versions used to create the model and the versions in this app's environment.
        
        **To fix this, please follow these steps in your terminal:**
        
        1.  Ensure you have activated your virtual environment.
        2.  Run the command below to install the exact required versions:
        """
    )
    st.code("pip install -r requirements.txt", language="bash")
    st.error(f"**Internal Error Details:** {e}")
    st.stop()


# --- Main Application ---
def main():
    load_css()
    
    # --- Header ---
    st.markdown('<div class="header"><h1>🐟 Fish Species Predictor</h1></div>', unsafe_allow_html=True)

    # --- Sidebar for Inputs ---
    with st.sidebar:
        st.header("Input Fish Features")
        
        # Input fields
        weight = st.number_input('Weight (in grams)', min_value=0.0, format="%.2f")
        length1 = st.number_input('Vertical Length (in cm)', min_value=0.0, format="%.2f")
        length2 = st.number_input('Diagonal Length (in cm)', min_value=0.0, format="%.2f")
        length3 = st.number_input('Cross Length (in cm)', min_value=0.0, format="%.2f")
        height = st.number_input('Height (in cm)', min_value=0.0, format="%.2f")
        width = st.number_input('Width (in cm)', min_value=0.0, format="%.2f")

        predict_button = st.button('Predict Species')

    # --- Main Panel for Output ---
    st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True) # Spacer for header
    
    if model:
        st.info("Enter the fish measurements in the sidebar and click 'Predict Species' to see the result.")

        if predict_button:
            # Create a DataFrame from the inputs
            input_data = pd.DataFrame({
                'Weight': [weight],
                'Length1': [length1],
                'Length2': [length2],
                'Length3': [length3],
                'Height': [height],
                'Width': [width]
            })
            
            # Make a prediction
            prediction = model.predict(input_data)[0]
            
            # Display the prediction
            st.markdown(f"""
                <div class="prediction-box">
                    <h2>Predicted Fish Species</h2>
                    <p style="font-size: 1.5rem; font-weight: bold;">{prediction}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # --- Footer ---
    st.markdown('<div class="footer"><p>Built with Streamlit by Gemini</p></div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()

