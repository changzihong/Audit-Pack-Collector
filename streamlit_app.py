import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Audit Pack Collector", layout="wide")

# --- CUSTOM STYLES ---
st.markdown("""
    <style>
        /* Remove white margins and spacing */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            margin: 0 !important;
        }

        /* Navbar styling */
        .navbar {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #000080;
            padding: 1rem 0;
            width: 100%;
            position: sticky;
            top: 0;
            z-index: 999;
        }

        .nav-btn {
            background-color: transparent;
            border: none;
            color: #ADD8E6;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            margin: 0 1.5rem;
            transition: transform 0.2s ease;
        }

        .nav-btn:hover {
            transform: scale(1.05);
        }

        /* Title section */
        .title-section {
            text-align: center;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }

        .title-section h1 {
            color: #000080;
            font-size: 2.3rem;
            font-weight: 700;
        }

        /* Page container */
        .content {
            background-color: #F5F5F5;
            padding: 2rem 4rem;
            border-radius: 12px;
            margin: 1rem auto;
            width: 85%;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.05);
        }

        /* Auth (login/signup) card styling */
        .auth-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 70vh;
        }

        .auth-card {
            background-color: white;
            padding: 2.5rem 3rem;
            border-radius: 16px;
            box-shadow: 0px 6px 12px rgba(0,0,0,0.1);
            width: 400px;
            text-align: center;
        }

        .auth-card input {
            width: 100%;
            padding: 0.7rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            border: 1px solid #ccc;
        }

        .auth-btn {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 0.7rem 2rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.2s ease;
        }

        .auth-btn:hover {
            background-color: #45a049;
        }

        .switch-link {
            margin-top: 1rem;
            display: inline-block;
            color: #000080;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease;
        }

        .switch-link:hover {
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# --- NAVIGATION STATE ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

def set_page(page_name):
    st.session_state.page = page_name

# --- NAVBAR ---
st.markdown(f"""
<div class="navbar">
    <button class="nav-btn" onclick="window.location.href='/'">Home</button>
    <button class="nav-btn" onclick="window.location.href='/?page=Login'">Login</button>
    <button class="nav-btn" onclick="window.location.href='/?page=SignUp'">SignUp</button>
</div>
""", unsafe_allow_html=True)

# --- PAGE ROUTING ---
query_params = st.query_params
page = query_params.get("page", ["Home"])[0]

# --- PAGE CONTENTS ---
if page == "Home":
    st.markdown("<div class='title-section'><h1>Welcome to Audit Pack Collector</h1></div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="content">
            <h3>📂 About the System</h3>
            <p>This tool helps HR teams organize, track, and validate all required audit documents efficiently.</p>
            <ul>
                <li>Central repository for all audit files</li>
                <li>Built-in document checklist</li>
                <li>Role-based responsibility tracker</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

elif page == "Login":
    st.markdown("""
        <div class="auth-container">
            <div class="auth-card">
                <h3>🔐 Login</h3>
                <input type="text" placeholder="Email">
                <input type="password" placeholder="Password">
                <button class="auth-btn">Login</button>
                <div class="switch-link" onclick="window.location.href='/?page=SignUp'">Don't have an account? Sign Up</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif page == "SignUp":
    st.markdown("""
        <div class="auth-container">
            <div class="auth-card">
                <h3>📝 Sign Up</h3>
                <input type="text" placeholder="Full Name">
                <input type="text" placeholder="Email">
                <input type="password" placeholder="Password">
                <button class="auth-btn">Create Account</button>
                <div class="switch-link" onclick="window.location.href='/?page=Login'">Already have an account? Login</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
