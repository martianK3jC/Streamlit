import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, time

# --- COLOR DEFINITIONS (Royal Blue & Gold Theme - Academic) ---
# Primary Backgrounds
DEEP_CHARCOAL = "#0D1117"   # Main app background (Deep Dark Blue/Gray)
DARK_GRAY = "#161B22"       # Main content areas, sidebar
SUBTLE_DARKER_GRAY = "#21262D" # Metrics, forms, expanders, success/info boxes

# Accent Colors
ROYAL_BLUE = "#4169E1"      # Primary Accent: H1, H2, Metric Values, Buttons, Profile Border/Glow
VIBRANT_GOLD = "#FFD700"    # Secondary Accent: H3, Chart Bars, Links, Secondary Progress
BUTTON_HOVER_BG = "#6495ED" # Tertiary Accent for button hover (Lighter Blue)

# Text & Neutral Colors
LIGHT_GRAY_TEXT = "#C9D1D9" # General text, labels (Light Gray)
MEDIUM_GRAY_NEUTRAL = "#6A6A6A" # Footer, less prominent borders/dividers


# --- DATA SETUP ---
initial_languages = {
    "Python": 90, "C++": 85, "Java": 75, "SQL": 80, 
    "C": 70, "JavaScript": 65, "C#": 50, "Kotlin": 40, "Assembly": 30
}
projects = {
    "Tamagotchi Teaches Programming": {
        "description": "An interactive, gamified learning tool where users nurture a digital pet by successfully completing programming challenges.",
        "status": {"Focus": "Full-Stack, Gamification", "Progress": 0.1, "Next Step": "Wireframing UI"},
        # Image URL uses Blue
        "image_url": f"https://placehold.co/400x200/{ROYAL_BLUE.strip('#')}/{DARK_GRAY.strip('#')}?text=WEB+DEV+PROJECT"
    },
    "Budgetables": {
        "description": "A localized guide to track the real-time or seasonal range of prices for fruits and vegetables in local markets to aid budgeting.",
        # --- FIXED: Changed Focus from Data Science to App Dev ---
        "status": {"Focus": "App Development, Data Collection, UX", "Progress": 0.05, "Next Step": "Market Research & Data Sourcing"},
        # Image URL uses Gold
        "image_url": f"https://placehold.co/400x200/{VIBRANT_GOLD.strip('#')}/{DARK_GRAY.strip('#')}?text=APP+DEV+PROJECT"
    }
}

# Initialize session state for language scores
if 'languages' not in st.session_state:
    st.session_state.languages = initial_languages


# Function to generate the fixed Dark CSS 
def get_custom_css():
    main_content_styles = """
        /* Limit the width of the main content container and center it */
        section.main {
            max-width: 1200px; /* Max width for large screens */
            padding: 2rem; 
            margin: 0 auto; /* Center the main content block */
        }
        /* Override Streamlit's default container padding for even more side space */
        .block-container {
            padding-left: 5rem; /* Large left padding */
            padding-right: 5rem; /* Large right padding */
            padding-top: 2rem; 
            padding-bottom: 2rem;
        }
        
        /* Add spacing for metrics */
        [data-testid="stMetric"] {
            padding: 1.5rem !important;
            margin: 1rem 0.5rem !important;
        }
        /* Add spacing for expanders */
        [data-testid="stExpander"] {
            margin: 1.5rem 0 !important;
            padding: 0.5rem !important;
        }
        /* Add spacing for forms */
        [data-testid="stForm"] {
            padding: 2rem !important;
            margin: 1.5rem 0 !important;
            border-radius: 10px !important;
        }
        /* Add spacing for dataframes */
        [data-testid="stDataFrame"] {
            margin: 1.5rem 0 !important;
        }
        /* Better spacing for columns */
        [data-testid="column"] {
            padding: 1rem !important;
        }
        /* Add breathing room to sections */
        .element-container {
            margin-bottom: 1rem;
        }
    """

    # Dark Theme (Royal Blue & Gold) - Now the only theme
    return f"""
    <style>
        {main_content_styles}
        .stApp {{ background-color: {DEEP_CHARCOAL}; color: {LIGHT_GRAY_TEXT}; }}
        .main, [data-testid="stSidebar"] {{ 
            background-color: {DARK_GRAY}; 
            border-radius: 10px; 
            padding: 2rem; 
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); 
        }}
        
        /* ROYAL BLUE Accents (Primary) */
        h1, h2 {{ color: {ROYAL_BLUE}; font-weight: 900; margin-top: 1.5rem; margin-bottom: 1rem; }}
        [data-testid="stMetricValue"] {{ color: {ROYAL_BLUE}; font-size: 1.8rem; font-weight: 700; }}
        .stButton>button {{ 
            background-color: {ROYAL_BLUE}; 
            color: {LIGHT_GRAY_TEXT}; 
            font-weight: 600;
            padding: 0.6rem 1.5rem;
            margin: 0.5rem 0;
            border: none;
            border-radius: 5px;
        }}
        .stButton>button:hover {{ background-color: {BUTTON_HOVER_BG}; color: {DEEP_CHARCOAL}; }}
        
        /* Styling for sidebar image border/glow */
        [data-testid="stSidebar"] img {{
            border: 4px solid {VIBRANT_GOLD}; /* Gold border */
            box-shadow: 0 0 25px {VIBRANT_GOLD}80; /* Gold glow */
            border-radius: 50%; /* Make image circular */
            display: block; 
            margin-bottom: 1rem;
        }}

        .stProgress > div > div > div > div {{ background-color: {VIBRANT_GOLD}; }} /* Main progress bars use Gold */
        
        /* VIBRANT GOLD Accents (Secondary) */
        h3 {{ color: {VIBRANT_GOLD}; margin-top: 1rem; margin-bottom: 0.8rem; }}
        [data-testid="stSidebar"] .stProgress > div > div > div > div {{ background-color: {VIBRANT_GOLD}; }} /* Motivation Level */
        a {{ color: {VIBRANT_GOLD} !important; text-decoration: none; }}
        a:hover {{ color: {ROYAL_BLUE} !important; text-decoration: underline; }}

        /* Accent Backgrounds (Forms, Metrics, Info boxes) */
        [data-testid="stMetric"], [data-testid="stForm"], [data-testid="stExpander"], 
        [data-testid="stSidebar"] [data-testid="stSuccess"], 
        [data-testid="stSidebar"] [data-testid="stInfo"] {{ 
            background-color: {SUBTLE_DARKER_GRAY}; 
            border: 1px solid {MEDIUM_GRAY_NEUTRAL}; 
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            border-radius: 8px;
            color: {LIGHT_GRAY_TEXT} !important; 
        }}
        
        /* General Input/Text fixes */
        [data-testid="stMetricLabel"] {{ color: {LIGHT_GRAY_TEXT}; font-size: 1rem; }}
        .stSelectbox label, .stNumberInput label {{ color: {LIGHT_GRAY_TEXT}; }}
        [data-testid="stDataFrame"] {{ color: {DEEP_CHARCOAL}; }} 
        .stApp > footer p {{ color: {MEDIUM_GRAY_NEUTRAL}; }}
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
            color: {ROYAL_BLUE}; 
        }}
    </style>
    """

# Set the page configuration early for a custom look
st.set_page_config(
    page_title="Kesha Jane Ceniza - CS Student Portfolio",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply the theme CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)


# Creating DataFrame for Skills Chart (reads from session state)
df_skills_chart = pd.DataFrame(
    list(st.session_state.languages.items()), columns=['Language', 'Experience Score (out of 100)']
).set_index('Language')


# Coordinates and data for the simulated walking path map
coords = {
    'lat': [10.3013, 10.3050, 10.3080], 'lon': [123.8906, 123.8890, 123.8870],
}
coords['lat'].extend(np.linspace(10.3080, 10.3120, 5))
coords['lon'].extend(np.linspace(123.8870, 123.8860, 5))
coords['lat'].extend(np.linspace(10.3120, 10.2933, 8))
coords['lon'].extend(np.linspace(123.8860, 123.9016, 8))
coords['lat'].extend(np.linspace(10.2933, 10.3013, 5))
coords['lon'].extend(np.linspace(123.9016, 123.8906, 5))
map_data = pd.DataFrame(coords)


# --- FUNCTION DEFINITIONS ---

# Function to update the score in session state (+5 points)
def update_score_add(language):
    # Ensure score doesn't exceed 100
    if st.session_state.languages[language] < 100:
        st.session_state.languages[language] = min(st.session_state.languages[language] + 5, 100)
        st.toast(f"+5 Points Added! {language} score is now {st.session_state.languages[language]}%.", icon="🚀")
    else:
        st.toast(f"Mastery reached! {language} is already at 100%. Great job!", icon="🎉")


# --- SIDEBAR (st.sidebar) ---
st.sidebar.title("About the Author 👤")

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------
# >>> PROFILE PICTURE SECTION (Sidebar) <<<
# This uses the local path 'img/CENIZA.jpg' to ensure the image loads when running locally.
# NOTE: Place your image file in the 'img' directory next to portfolio.py
PROFILE_PATH = "img/CENIZA.jpg"
SIDEBAR_IMG_SIZE = 150 

st.sidebar.image(PROFILE_PATH, width=SIDEBAR_IMG_SIZE)
# -----------------------------------------------------------

st.sidebar.caption("Connect with me!")

st.sidebar.markdown("<br>", unsafe_allow_html=True)

st.sidebar.metric(label="University", value="CIT-U")
st.sidebar.metric(label="Student Status", value="2nd Year CS")
st.sidebar.metric(label="Duolingo Streak (Days)", value="450", delta="Consistent Learning!")

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# New: Download Resume Button (Improved format)
resume_text = f"""
========================================
          PORTFOLIO RESUME
========================================

Name: [Your Name]
Title: CS Student & Project Analytics Officer
University: Cebu Institute of Technology - University
Year: 2nd Year Computer Science

========================================
          TECHNICAL SKILLS
========================================
{', '.join(initial_languages.keys())}

========================================
          PROJECT IDEAS
========================================
1. Tamagotchi Teaches Programming
    - Gamified learning tool for programming
    
2. Budgetables
    - Price tracking app for local market produce

========================================
          CONTACT
========================================
Email: keshajane24@gmail.com
GitHub: martianK3jC
LinkedIn: Kesha Jane L. Ceniza

========================================
"""

st.sidebar.download_button(
    label="📄 Download Resume (TXT)",
    data=resume_text,
    file_name='portfolio_resume.txt',
    mime='text/plain',
    help="Download a text version of the portfolio resume"
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

st.sidebar.header("Achievements")
# --- UPDATED TEXT HERE ---
st.sidebar.success("✅ Advanced Past Round 1: Ceb-i Hacks Cutoff")
# -------------------------
st.sidebar.info("📌 Project Analytics Officer: GDG CIT-U")

st.sidebar.markdown("<br>", unsafe_allow_html=True)

st.sidebar.header("Aspirations & Fun Facts")
st.sidebar.info(
    "**Aspiration:** Proficient Full-Stack Web Developer & Data Science dabbler. "
    "\n\n**Fun Facts:** Loves walking/hiking, watching funny reels, and competitive eating (I need to start!). Painting is a passion, even if I'm not great at it."
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

st.sidebar.progress(85, text="Motivation Level")


# --- MAIN CONTENT: SINGLE SCROLLABLE PAGE ---

st.markdown("<br>", unsafe_allow_html=True)

# 1. HOME / BIO SECTION
col1, col2 = st.columns([3, 1])

with col1:
    st.title("The CS Journey Portfolio")
    st.header("Confusion: It's a Feature, Not a Bug")
    # Text color is fixed to dark theme's light gray
    bio_color = LIGHT_GRAY_TEXT 
    st.markdown(
        f"""
        <p style='font-size: 1.2rem; color: {bio_color}; line-height: 1.8; margin-bottom: 1rem;'>
        Confusion isn't a bug, it's a <strong>feature</strong> of programming. If you're not confused, you're not learning—or you're just very good at pretending you're not confused during a late-night debugging session.
        </p>
        <p style='font-size: 1.2rem; color: {bio_color}; line-height: 1.8;'>
        As a <strong>Second-Year Computer Science Student at Cebu Institute of Technology - University (CIT-U)</strong>, I specialize in bridging technical problem-solving with organizational oversight, currently serving as a <strong>Project Analytics Officer</strong> for the Google Developer Group on campus.
        </p>
        """, 
        unsafe_allow_html=True
    )
with col2:
    st.markdown("<br><br>", unsafe_allow_html=True) 
    st.metric(label="Experience Focus", value="Analytics + Code", delta="Growing Daily!")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# 2. SKILLS SECTION
st.header("Technical Skillset 🛠️")
st.caption("A visualization of experience (based on a highly scientific self-assessment 😉)")

st.markdown("<br>", unsafe_allow_html=True)

# Interactive Bar Chart (Reads from session state)
st.subheader("Language Proficiency Comparison")
# Dynamic chart color uses VIBRANT_GOLD
chart_color = VIBRANT_GOLD 
st.bar_chart(df_skills_chart, use_container_width=True, color=chart_color)

st.markdown("<br>", unsafe_allow_html=True)

# Split skills into 3 columns for better layout on desktop
skill_cols = st.columns(3)

# Core Languages (Re-using progress bars for detailed view)
with skill_cols[0]:
    st.subheader("Core Languages")
    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(st.session_state.languages['Python'] / 100, text=f"Python ({st.session_state.languages['Python']}%)")
    st.progress(st.session_state.languages['SQL'] / 100, text=f"SQL ({st.session_state.languages['SQL']}%)")
    st.progress(st.session_state.languages['C++'] / 100, text=f"C++ ({st.session_state.languages['C++']}%)")
    st.progress(st.session_state.languages['Java'] / 100, text=f"Java ({st.session_state.languages['Java']}%)")

# Web/Foundational
with skill_cols[1]:
    st.subheader("Web & Foundations")
    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(st.session_state.languages['JavaScript'] / 100, text=f"JavaScript ({st.session_state.languages['JavaScript']}%)")
    st.progress(st.session_state.languages['C'] / 100, text=f"C ({st.session_state.languages['C']}%)")
    st.progress(st.session_state.languages['C#'] / 100, text=f"C# ({st.session_state.languages['C#']}%)")

# Specialized/Mobile
with skill_cols[2]:
    st.subheader("Specialty")
    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(st.session_state.languages['Kotlin'] / 100, text=f"Kotlin ({st.session_state.languages['Kotlin']}%)")
    st.progress(st.session_state.languages['Assembly'] / 100, text=f"Assembly ({st.session_state.languages['Assembly']}%)")

st.markdown("<br>", unsafe_allow_html=True)
    
# Use an expander to show the full list clearly
with st.expander("View Raw Skill Data"):
    st.dataframe(df_skills_chart, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# 3. ACADEMIC JOURNEY & TIMELINE
st.header("Academic Journey & Milestones 📈")
st.caption("A look at the path taken (and re-taken) to Computer Science.")

st.markdown("<br>", unsafe_allow_html=True)

# Data structure for the timeline events
timeline_data = [
    ("2005", "Born in Cebu, Philippines!"),
    ("2017", "Elementary School Graduation 🎓"),
    ("2021", "High School Graduation"),
    ("2023", "Senior High School Graduation"),
    # Refined wording applied here (FIXED: removed redundant **)
    ("2023-2024", "The Pivot: Initially failing Computer Engineering. This period was crucial, teaching me the true meaning of persistence and refining my career passion."),
    ("2024", "Persistence Pays: I took a risk, faced the Dean, and successfully advocated for my transfer into the Computer Science program. That decision made all the difference."),
    ("2024-Present", "Current Trajectory: I'm navigating the CS curriculum now, embracing the daily grind and pushing forward to build a rock-solid technical foundation.")
]

# Displaying the timeline using columns
year_color = ROYAL_BLUE 
event_color = VIBRANT_GOLD 

for year, event in timeline_data:
    tl_col1, tl_col2 = st.columns([1, 4])
    with tl_col1:
        st.markdown(f"### <span style='color: {year_color};'>{year}</span>", unsafe_allow_html=True)
    with tl_col2:
        # We use an f-string with <strong> tags to apply bolding inside the markdown output
        # Here we bold the key terms manually:
        if year == "2024":
            styled_event = event.replace("Computer Science", "<strong>Computer Science</strong>")
        elif year == "2024-Present":
            styled_event = event.replace("Current Trajectory", "<strong>Current Trajectory</strong>")
        else:
            styled_event = event
            
        st.markdown(f"<p style='color: {event_color}; font-size: 1.1rem; padding-top: 10px; line-height: 1.6;'>{styled_event}</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---") 
st.markdown("<br>", unsafe_allow_html=True)

# 4. PORTFOLIO IDEAS SECTION (INTERACTIVE)
st.header("Portfolio Ideas (Conceptual) 💡")
st.caption("Use the selector to view project details and current mock status.")

st.markdown("<br>", unsafe_allow_html=True)

# Project Selector and Display
project_key = st.selectbox(
    'Select a Project to View Details:',
    options=list(projects.keys()),
    key='project_selector'
)
selected_project = projects[project_key]

st.markdown("<br>", unsafe_allow_html=True)

# Dynamic Project Display
col_img, col_desc = st.columns([1, 2])
with col_img:
    st.image(selected_project["image_url"], caption=f"Mockup for {project_key}")
with col_desc:
    st.subheader(project_key)
    st.write(selected_project["description"])
    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(selected_project["status"]["Progress"], text=f"Mock Progress: {int(selected_project['status']['Progress'] * 100)}%")

st.markdown("<br>", unsafe_allow_html=True)

# Project Status Data (st.dataframe for detail)
st.markdown("##### Project Status Details (Data Demonstration):")
status_df = pd.DataFrame(
    list(selected_project["status"].items()), columns=['Attribute', 'Value']
).set_index('Attribute')
st.dataframe(status_df, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# 5. DATA VISUALIZATION SECTION
st.header("🚶 My Cebu Walking Paths (Data Feature) 🗺️")
st.caption("A simulated visualization of walks between CIT-U, Labangon, and the National Museum.")

st.markdown("<br>", unsafe_allow_html=True)

st.map(map_data, zoom=13, use_container_width=True)
st.caption("The path represents the route from CIT-U to Paseo Arcenas/Sta. Ana Labangon, then on to the National Museum of the Philippines - Cebu, and back towards CIT-U.")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# 6. INTERACTIVE DATA LOGGER
st.header("🗓️ Daily Focus Tracker (Data Logger) 📝")
st.caption("Log your mock study time for Python today. This demonstrates `st.time_input` and `st.form` usage.")

st.markdown("<br>", unsafe_allow_html=True)

if 'study_log' not in st.session_state:
    st.session_state.study_log = pd.DataFrame({
        'Date': [datetime.today().date()],
        'Language': ['Python'],
        'Duration (hours)': [1.5]
    })

with st.form("study_log_form", clear_on_submit=True):
    # Added padding div for better form appearance
    st.markdown("<div style='padding: 1rem;'>", unsafe_allow_html=True)
    col_lang, col_time = st.columns(2)
    with col_lang:
        log_language = st.selectbox(
            'Language Studied:',
            options=list(st.session_state.languages.keys()),
            key='log_lang'
        )
    with col_time:
        log_duration = st.number_input(
            'Study Duration (Hours):',
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.5,
            key='log_duration'
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    submit_log = st.form_submit_button("Log Study Session")
    st.markdown("</div>", unsafe_allow_html=True)

    if submit_log:
        new_entry = pd.DataFrame({
            'Date': [datetime.today().date()],
            'Language': [log_language],
            'Duration (hours)': [log_duration]
        })
        st.session_state.study_log = pd.concat([st.session_state.study_log, new_entry], ignore_index=True)
        st.success("Study session logged!")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("##### Recent Study Log:")
st.dataframe(st.session_state.study_log.tail(5), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# 7. SKILL BOOSTER (INTERACTIVE COMPONENT)
st.header("✨ Today I Learned: Skill Booster (Interactive Component) 🚀")
st.caption("Select a skill you focused on today and give yourself +5 points!")

st.markdown("<br>", unsafe_allow_html=True)

# Get list of languages for the selectbox
language_options = list(st.session_state.languages.keys())

# Interactive Widgets
col_sel, col_btn = st.columns([4, 1])

with col_sel:
    selected_language = st.selectbox(
        'Which language did you focus on today?',
        options=language_options,
        index=language_options.index("Python"),
        key='plus_point_selector'
    )

with col_btn:
    st.markdown("<br>", unsafe_allow_html=True) # Spacer for button alignment
    if st.button(f'+5 Boost to {selected_language}', use_container_width=True):
        update_score_add(selected_language)

st.markdown("<br>", unsafe_allow_html=True)
        
# Re-draw the skill chart immediately after the simulator for visual feedback
st.markdown("##### Updated Skill Level Visualization:")
df_updated_skills_chart = pd.DataFrame(
    list(st.session_state.languages.items()), columns=['Language', 'Experience Score (out of 100)']
).set_index('Language')

# Bar chart uses VIBRANT_GOLD
boost_color = VIBRANT_GOLD 
st.bar_chart(df_updated_skills_chart, use_container_width=True, color=boost_color) 

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# 8. CONTACT ME SECTION
st.header("Get In Touch 📧")
# Dynamic colors for contact section (fixed to dark theme's colors)
contact_color = LIGHT_GRAY_TEXT 
link_color = VIBRANT_GOLD 
accent_color = ROYAL_BLUE 

st.markdown(f"""
<div style='color: {contact_color}; margin-bottom: 2rem; line-height: 1.8;'>
You can reach out to discuss CS, Project Analytics, the hackathon, or competitive eating!
</div>
<div style='font-size: 1.1rem; line-height: 2;'>
<p style='color: {accent_color}; margin-bottom: 1rem;'>
    🔗 GitHub: <a href="https://github.com/martianK3jC" target="_blank" style="color: {link_color}; text-decoration: none;">martianK3jC</a>
</p>
<p style='color: {accent_color}; margin-bottom: 1rem;'>
    💼 LinkedIn: <a href="https://www.linkedin.com/in/kesha-jane-ceniza-88923b38b/" target="_blank" style="color: {link_color}; text-decoration: none;">Kesha Jane L. Ceniza</a>
</p>
<p style='color: {accent_color}; margin-bottom: 1rem;'>
    ✉️ Email: <a href="mailto:keshajane24@gmail.com" style="color: {link_color}; text-decoration: none;">keshajane24@gmail.com</a>
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# Fixed footer text
st.markdown(f"<p style='text-align: center; color: {MEDIUM_GRAY_NEUTRAL};'>Built with Streamlit 🎈</p>", unsafe_allow_html=True)