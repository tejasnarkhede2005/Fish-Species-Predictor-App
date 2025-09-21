import streamlit as st
import pandas as pd
import pickle

# --- Page Configuration ---
st.set_page_config(
    page_title="Fish Weight Predictor",
    page_icon="🐟",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Styling ---
def load_css():
    """Loads custom CSS for a modern, clean look."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
            
            html, body, [class*="st-"] {
                font-family: 'Poppins', sans-serif;
            }

            /* Main container styling */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                padding-left: 2rem;
                padding-right: 2rem;
                background-color: #f9f9f9;
            }

            /* Sidebar styling */
            .st-emotion-cache-16txtl3 {
                background-color: #FFFFFF;
                border-right: 1px solid #e0e0e0;
            }
            
            h1 {
                color: #0068c9;
                text-align: center;
            }

            h2, h3 {
                color: #333;
            }

            /* Input widgets styling */
            .stNumberInput, .stButton {
                margin-bottom: 0.75rem;
            }

            /* Custom button styling */
            .stButton>button {
                border: 2px solid #0068c9;
                border-radius: 10px;
                color: #FFFFFF;
                background-color: #0068c9;
                padding: 10px 24px;
                cursor: pointer;
                width: 100%;
                font-size: 1.1rem;
                font-weight: 600;
                transition: all 0.3s ease-in-out;
            }
            .stButton>button:hover {
                background-color: #FFFFFF;
                color: #0068c9;
                border-color: #0068c9;
            }
            
            /* Prediction result card */
            .prediction-card {
                background-color: #ffffff;
                border-radius: 15px;
                padding: 25px;
                margin-top: 2rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                text-align: center;
                border: 1px solid #e0e0e0;
            }
            .prediction-card h2 {
                color: #0068c9;
                margin-bottom: 10px;
                font-size: 1.8rem;
            }
            .prediction-value {
                font-size: 2.2rem;
                font-weight: 600;
                color: #2a9d8f;
            }
            
            /* Footer styling */
            footer {
                text-align: center;
                padding: 1rem;
                color: #888;
            }
        </style>
    """, unsafe_allow_html=True)

# --- Model Loading ---
@st.cache_resource
def load_model():
    """Loads the trained machine learning model from the pickle file."""
    try:
        with open('Random Forest_best_model.pkl', 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        st.error("Model file 'Random Forest_best_model.pkl' not found.")
        st.info("Please ensure the model file is in the same directory as the app.py script.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the model: {e}")
        st.warning("This is often due to a library version mismatch. Please run 'pip install -r requirements.txt' in your terminal.")
        return None

# --- Main Application ---
def main():
    load_css()
    model = load_model()

    if model is None:
        st.stop()

    # --- Sidebar for User Inputs ---
    with st.sidebar:
        st.header("Input Fish Features")
        
        # Create input fields for the fish features
        weight = st.number_input('Weight (in grams)', min_value=0.0, value=242.0, format="%.2f")
        length1 = st.number_input('Vertical Length (cm)', min_value=0.0, value=23.2, format="%.2f")
        length2 = st.number_input('Diagonal Length (cm)', min_value=0.0, value=25.4, format="%.2f")
        length3 = st.number_input('Cross Length (cm)', min_value=0.0, value=30.0, format="%.2f")
        height = st.number_input('Height (cm)', min_value=0.0, value=11.52, format="%.2f")
        width = st.number_input('Diagonal Width (cm)', min_value=0.0, value=4.02, format="%.2f")
        
        predict_button = st.button('Predict Weight')

    # --- Main Panel Display ---
    st.title("🐟 Fish Weight Predictor")
    st.markdown("Enter the measurements of a fish in the sidebar to predict its weight.")

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
        
        # Make a prediction using the loaded model
        prediction = model.predict(input_data)[0]
        
        # Display the prediction in a styled card
        st.markdown(f"""
            <div class="prediction-card">
                <h2>Predicted Fish Weight</h2>
                <p class="prediction-value">{prediction:.2f} grams</p>
            </div>
        """, unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("---")
    st.markdown("<footer>Built with Streamlit and Gemini</footer>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()

