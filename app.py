# 2. Enhanced CSS to force sidebar visibility and show toggle sign
st.markdown("""
    <style>
        /* 1. Force the sidebar to stay visible regardless of state */
        [data-testid="stSidebar"] {
            transform: none !important;
            visibility: visible !important;
            min-width: 300px !important;
            max-width: 300px !important;
            border-right: 2px solid rgba(255, 75, 173, 0.2);
        }

        /* 2. Force the toggle button (the > or < sign) to always show */
        [data-testid="collapsedControl"] {
            display: flex !important;
            visibility: visible !important;
            left: 0 !important;
            color: #ff4bad !important;
            background-color: white !important;
            border-radius: 0 50% 50% 0 !important;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1) !important;
            z-index: 999999 !important;
        }

        /* 3. Adjust the main content margin so it doesn't overlap on wide screens */
        [data-testid="stMainViewContainer"] {
            margin-left: 0px;
        }

        /* 4. Hide the specific 'X' close button inside the sidebar to prevent accidental closing */
        [data-testid="stSidebar"] button[kind="header"] {
            display: none !important;
        }
        
        /* Secret message comment for the code:
           SemSemty AI 🌸 — A cute pink radiology assistant made with love for Sama 💗🐾
           Made with endless love by Mohamed ✨
        */
    </style>
""", unsafe_allow_html=True)
