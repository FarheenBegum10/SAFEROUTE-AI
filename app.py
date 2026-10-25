import streamlit as st
import streamlit.components.v1 as components
import folium
from streamlit_folium import st_folium
import requests
from app_pages.dashboard import show_dashboard
from app_pages.routes import show_routes
from utils.helpers import analyze_route
from app_pages.around_me import show_around_me
from app_pages.emergency import show_emergency
from app_pages.trusted_contacts import show_trusted_contacts


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="SafeRoute AI",
    page_icon="🛡️",
    layout="wide"
)


# =====================================================
# SESSION STATE
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

if "latitude" not in st.session_state:
    st.session_state.latitude = None

if "longitude" not in st.session_state:
    st.session_state.longitude = None

if "nearby_places" not in st.session_state:
    st.session_state.nearby_places = [] 
if "trusted_contacts" not in st.session_state:
    st.session_state.trusted_contacts = []
if "offline_mode" not in st.session_state:
    st.session_state.offline_mode = False
if "language" not in st.session_state:
    st.session_state.language = "English"


# =====================================================
# MULTI-LANGUAGE TRANSLATIONS
# =====================================================

translations = {

    "English": {

        "dashboard": "Dashboard",
        "safe_routes": "Safe Routes",
        "safe_around_me": "Safe Around Me",
        "emergency_sos": "Emergency SOS",
        "settings": "SETTINGS",
        "overview": "OVERVIEW",
        "language": "Language",
        "logout": "Logout",

        "where_going": "Where are you going today?",
        "find_safest_way": "Find the safest way to reach your destination.",
        "search_destination": "Search destination",
        "destination_placeholder": "Where do you want to go?",
        "use_location": "📍 Use my live location",
        "find_route": "✦ Find My Safest Route",

        "current_location": "📍 Current Location Detected",
        "live_safety_map": "Live safety map",
        "location_instruction":
            "Click 'Use my live location' to display your location on the map.",

        "safety_companion": "Your safety companion",
        "more_features": "More safety features",

        "safe_routes_card": "🛡️ Safe Routes",
        "safe_routes_desc":
            "Compare possible routes and choose the one with the highest safety score.",

        "safe_around_card": "📍 Safe Around Me",
        "safe_around_desc":
            "Discover nearby police stations, hospitals and safe public places.",

        "sos_card": "🚨 Emergency SOS",
        "sos_desc":
            "Quickly access emergency assistance and trusted contacts.",

        "multi_language": "🌐 Multi-language Support",
        "multi_language_desc":
            "Access safety information and alerts in your preferred language.",

        "offline_support": "📡 Offline Support",
        "offline_support_desc":
            "Access essential safety information even with limited connectivity.",

        "trusted_contacts": "👥 Trusted Contacts",
        "trusted_contacts_desc":
            "Keep your emergency contacts ready whenever you need them.",

        "choose_safer": "Choose the safer way.",
        "fastest_not_safest":
            "The fastest route is not always the safest route.",
        "starting_point": "Starting point",
        "starting_placeholder": "Where are you starting from?",
        "destination": "Destination",
        "analyze_route": "✦ Analyze Safest Route",
        "route_analysis": "✦ Route Safety Analysis",
        "recommended": "Recommended",
        "safety_score": "Safety Score",
        "distance": "Distance",
        "risk_level": "Risk Level",

        "safe_around_title": "Safe Around Me",
        "safe_around_desc":
            "Discover nearby places that can help keep you safe.",
        "use_saved_location": "📍 Using your saved live location.",
        "find_places": "🔍 Find Safety Places Near Me",
        "searching": "Searching nearby safety places...",
        "nearby_resources": "Nearby Safety Resources",
        "search_instruction":
            "Click 'Find Safety Places Near Me' to search.",

        "emergency_title": "Emergency Assistance",
        "emergency_desc": "Get quick access to emergency support.",
        "need_help": "🚨 Need immediate help?",
        "emergency_action":
            "Use the emergency action below to activate your safety response.",
        "activate_sos": "🚨 ACTIVATE EMERGENCY SOS"

    },


    "తెలుగు": {

        "dashboard": "డాష్‌బోర్డ్",
        "safe_routes": "సురక్షిత మార్గాలు",
        "safe_around_me": "నా చుట్టూ సురక్షిత ప్రదేశాలు",
        "emergency_sos": "అత్యవసర SOS",
        "settings": "సెట్టింగ్స్",
        "overview": "అవలోకనం",
        "language": "భాష",
        "logout": "లాగ్ అవుట్",

        "where_going": "ఈరోజు మీరు ఎక్కడికి వెళ్తున్నారు?",
        "find_safest_way":
            "మీ గమ్యస్థానానికి చేరుకోవడానికి సురక్షితమైన మార్గాన్ని కనుగొనండి.",
        "search_destination": "గమ్యస్థానాన్ని వెతకండి",
        "destination_placeholder": "మీరు ఎక్కడికి వెళ్లాలనుకుంటున్నారు?",
        "use_location": "📍 నా ప్రస్తుత స్థానాన్ని ఉపయోగించండి",
        "find_route": "✦ నా సురక్షిత మార్గాన్ని కనుగొనండి",

        "current_location": "📍 ప్రస్తుత స్థానం గుర్తించబడింది",
        "live_safety_map": "లైవ్ సేఫ్టీ మ్యాప్",
        "location_instruction":
            "మీ స్థానాన్ని మ్యాప్‌లో చూపించడానికి 'నా ప్రస్తుత స్థానాన్ని ఉపయోగించండి' క్లిక్ చేయండి.",

        "safety_companion": "మీ సేఫ్టీ కంపానియన్",
        "more_features": "మరిన్ని సేఫ్టీ ఫీచర్లు",

        "safe_routes_card": "🛡️ సురక్షిత మార్గాలు",
        "safe_routes_desc":
            "వివిధ మార్గాలను పోల్చి అత్యధిక సేఫ్టీ స్కోర్ ఉన్న మార్గాన్ని ఎంచుకోండి.",

        "safe_around_card": "📍 నా చుట్టూ సురక్షిత ప్రదేశాలు",
        "safe_around_desc":
            "సమీపంలోని పోలీస్ స్టేషన్లు, ఆసుపత్రులు మరియు సురక్షిత ప్రదేశాలను కనుగొనండి.",

        "sos_card": "🚨 అత్యవసర SOS",
        "sos_desc":
            "అత్యవసర సహాయం మరియు నమ్మకమైన పరిచయాలను త్వరగా యాక్సెస్ చేయండి.",

        "multi_language": "🌐 బహుభాషా మద్దతు",
        "multi_language_desc":
            "మీకు ఇష్టమైన భాషలో సేఫ్టీ సమాచారం మరియు అలర్ట్‌లను పొందండి.",

        "offline_support": "📡 ఆఫ్‌లైన్ మద్దతు",
        "offline_support_desc":
            "పరిమిత ఇంటర్నెట్ ఉన్నప్పటికీ అవసరమైన సేఫ్టీ సమాచారాన్ని పొందండి.",

        "trusted_contacts": "👥 నమ్మకమైన పరిచయాలు",
        "trusted_contacts_desc":
            "అత్యవసర సమయంలో మీ నమ్మకమైన పరిచయాలను సిద్ధంగా ఉంచుకోండి.",

        "choose_safer": "సురక్షితమైన మార్గాన్ని ఎంచుకోండి.",
        "fastest_not_safest":
            "వేగవంతమైన మార్గం ఎల్లప్పుడూ సురక్షితమైనది కాదు.",
        "starting_point": "ప్రారంభ స్థానం",
        "starting_placeholder": "మీరు ఎక్కడి నుండి ప్రారంభిస్తున్నారు?",
        "destination": "గమ్యస్థానం",
        "analyze_route": "✦ సురక్షితమైన మార్గాన్ని విశ్లేషించండి",
        "route_analysis": "✦ మార్గ సేఫ్టీ విశ్లేషణ",
        "recommended": "సిఫార్సు చేయబడింది",
        "safety_score": "సేఫ్టీ స్కోర్",
        "distance": "దూరం",
        "risk_level": "ప్రమాద స్థాయి",

        "safe_around_title": "నా చుట్టూ సురక్షిత ప్రదేశాలు",
        "safe_around_desc":
            "మీకు సురక్షితంగా ఉండటానికి సహాయపడే సమీప ప్రదేశాలను కనుగొనండి.",
        "use_saved_location": "📍 మీ సేవ్ చేసిన లైవ్ లొకేషన్ ఉపయోగించబడుతోంది.",
        "find_places": "🔍 నా సమీపంలోని సేఫ్టీ ప్రదేశాలను కనుగొనండి",
        "searching": "సమీపంలోని సేఫ్టీ ప్రదేశాలను వెతుకుతోంది...",
        "nearby_resources": "సమీపంలోని సేఫ్టీ వనరులు",
        "search_instruction":
            "వెతకడానికి 'నా సమీపంలోని సేఫ్టీ ప్రదేశాలను కనుగొనండి' క్లిక్ చేయండి.",

        "emergency_title": "అత్యవసర సహాయం",
        "emergency_desc": "అత్యవసర సహాయాన్ని త్వరగా పొందండి.",
        "need_help": "🚨 మీకు తక్షణ సహాయం కావాలా?",
        "emergency_action":
            "మీ సేఫ్టీ రెస్పాన్స్‌ను ప్రారంభించడానికి క్రింది ఎమర్జెన్సీ యాక్షన్‌ను ఉపయోగించండి.",
        "activate_sos": "🚨 అత్యవసర SOS యాక్టివేట్ చేయండి"

    },


    "हिन्दी": {

        "dashboard": "डैशबोर्ड",
        "safe_routes": "सुरक्षित मार्ग",
        "safe_around_me": "मेरे आसपास सुरक्षित स्थान",
        "emergency_sos": "आपातकालीन SOS",
        "settings": "सेटिंग्स",
        "overview": "अवलोकन",
        "language": "भाषा",
        "logout": "लॉग आउट",

        "where_going": "आज आप कहाँ जा रहे हैं?",
        "find_safest_way":
            "अपने गंतव्य तक पहुँचने का सबसे सुरक्षित मार्ग खोजें।",
        "search_destination": "गंतव्य खोजें",
        "destination_placeholder": "आप कहाँ जाना चाहते हैं?",
        "use_location": "📍 मेरी वर्तमान लोकेशन का उपयोग करें",
        "find_route": "✦ मेरा सबसे सुरक्षित मार्ग खोजें",

        "current_location": "📍 वर्तमान लोकेशन का पता चला",
        "live_safety_map": "लाइव सुरक्षा मानचित्र",
        "location_instruction":
            "मानचित्र पर अपना स्थान दिखाने के लिए 'मेरी वर्तमान लोकेशन का उपयोग करें' पर क्लिक करें।",

        "safety_companion": "आपका सुरक्षा साथी",
        "more_features": "अधिक सुरक्षा सुविधाएँ",

        "safe_routes_card": "🛡️ सुरक्षित मार्ग",
        "safe_routes_desc":
            "संभावित मार्गों की तुलना करें और सबसे अधिक सुरक्षा स्कोर वाला मार्ग चुनें।",

        "safe_around_card": "📍 मेरे आसपास सुरक्षित स्थान",
        "safe_around_desc":
            "पास के पुलिस स्टेशन, अस्पताल और सुरक्षित सार्वजनिक स्थान खोजें।",

        "sos_card": "🚨 आपातकालीन SOS",
        "sos_desc":
            "आपातकालीन सहायता और विश्वसनीय संपर्कों तक जल्दी पहुँचें।",

        "multi_language": "🌐 बहुभाषी सहायता",
        "multi_language_desc":
            "अपनी पसंदीदा भाषा में सुरक्षा जानकारी और अलर्ट प्राप्त करें।",

        "offline_support": "📡 ऑफलाइन सहायता",
        "offline_support_desc":
            "सीमित इंटरनेट कनेक्शन में भी आवश्यक सुरक्षा जानकारी प्राप्त करें।",

        "trusted_contacts": "👥 विश्वसनीय संपर्क",
        "trusted_contacts_desc":
            "आपातकालीन स्थिति में अपने विश्वसनीय संपर्क तैयार रखें।",

        "choose_safer": "सुरक्षित रास्ता चुनें।",
        "fastest_not_safest":
            "सबसे तेज़ रास्ता हमेशा सबसे सुरक्षित नहीं होता।",
        "starting_point": "प्रारंभिक स्थान",
        "starting_placeholder": "आप कहाँ से शुरू कर रहे हैं?",
        "destination": "गंतव्य",
        "analyze_route": "✦ सबसे सुरक्षित मार्ग का विश्लेषण करें",
        "route_analysis": "✦ मार्ग सुरक्षा विश्लेषण",
        "recommended": "अनुशंसित",
        "safety_score": "सुरक्षा स्कोर",
        "distance": "दूरी",
        "risk_level": "जोखिम स्तर",

        "safe_around_title": "मेरे आसपास सुरक्षित स्थान",
        "safe_around_desc":
            "अपने आसपास ऐसे स्थान खोजें जो आपको सुरक्षित रहने में मदद कर सकें।",
        "use_saved_location": "📍 आपकी सेव की गई लोकेशन का उपयोग किया जा रहा है।",
        "find_places": "🔍 मेरे पास सुरक्षित स्थान खोजें",
        "searching": "पास के सुरक्षित स्थान खोजे जा रहे हैं...",
        "nearby_resources": "पास के सुरक्षा संसाधन",
        "search_instruction":
            "खोजने के लिए 'मेरे पास सुरक्षित स्थान खोजें' पर क्लिक करें।",

        "emergency_title": "आपातकालीन सहायता",
        "emergency_desc": "आपातकालीन सहायता तक जल्दी पहुँचें।",
        "need_help": "🚨 क्या आपको तुरंत सहायता चाहिए?",
        "emergency_action":
            "अपनी सुरक्षा प्रतिक्रिया शुरू करने के लिए नीचे दिए गए आपातकालीन विकल्प का उपयोग करें।",
        "activate_sos": "🚨 आपातकालीन SOS सक्रिय करें"

    }

}


# =====================================================
# CURRENT LANGUAGE
# =====================================================

language = st.session_state.language
t = translations[language]


# =====================================================
# CUSTOM DESIGN
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Manrope:wght@400;500;600;700&display=swap');

* {
    font-family: 'Manrope', sans-serif;
}

.stApp {
    background: #F7F1EB;
}

.main {
    padding: 2rem 5rem;
}

.brand {
    font-size: 20px;
    font-weight: 700;
    color: #000000;
    letter-spacing: 1px;
}

.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 58px;
    line-height: 1.1;
    color: #000000;
}

.section-heading {
    color: #000000;
    font-size: 26px;
    font-weight: 700;
}

.hero-text {
    font-size: 17px;
    color: #000000;
    line-height: 1.7;
}

.stTextInput > div > div > input {
    background: #FFFDFC !important;
    color: #000000 !important;
    border: 1px solid #E1D3DC;
    border-radius: 12px;
    padding: 12px;
}

.stTextInput > div > div > input::placeholder {
    color: #777777 !important;
    opacity: 1 !important;
}

.stTextInput label {
    color: #000000 !important;
    font-weight: 600;
}

.stTabs [data-baseweb="tab"] {
    color: #000000 !important;
}

.stTabs [data-baseweb="tab"] p {
    color: #000000 !important;
}

.stTabs [data-baseweb="tab"] span {
    color: #000000 !important;
}

.stAlert {
    color: #000000 !important;
}

.stAlert p {
    color: #000000 !important;
}

.stButton > button {
    background: #9B7E9F;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 28px;
    font-size: 16px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #806583;
}

.dashboard-card {
    background: #FFFDFC;
    padding: 25px;
    border-radius: 22px;
    border: 1px solid #E9DDE5;
    min-height: 150px;
}

.card-title {
    color: #000000;
    font-size: 19px;
    font-weight: 700;
}

.card-text {
    color: #000000;
    font-size: 14px;
    line-height: 1.6;
}

.sos-card {
    background: #F3DADA;
    padding: 25px;
    border-radius: 22px;
    border: 1px solid #E5BDBD;
    min-height: 150px;
}

.route-card {
    background: #FFFDFC;
    padding: 25px;
    border-radius: 22px;
    border: 1px solid #E9DDE5;
    margin-top: 20px;
}

.route-title {
    color: #000000;
    font-size: 22px;
    font-weight: 700;
}

.route-score {
    color: #806583;
    font-size: 42px;
    font-weight: 700;
}

.route-info {
    color: #000000;
    font-size: 16px;
}

.location-card {
    background: #E8E1EC;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #D5C9DC;
    color: #000000;
}

[data-testid="stSidebar"] {
    background: #FFFDFC;
}

[data-testid="stSidebar"] * {
    color: #000000;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# FIND NEARBY SAFETY PLACES
# =====================================================

def get_nearby_places(latitude, longitude):

    query = f"""
    [out:json][timeout:25];

    (
        node["amenity"="police"](around:5000,{latitude},{longitude});
        way["amenity"="police"](around:5000,{latitude},{longitude});

        node["amenity"="hospital"](around:5000,{latitude},{longitude});
        way["amenity"="hospital"](around:5000,{latitude},{longitude});

        node["amenity"="fire_station"](around:5000,{latitude},{longitude});
        way["amenity"="fire_station"](around:5000,{latitude},{longitude});
    );

    out center;
    """

    url = "https://overpass.kumi.systems/api/interpreter"

    try:

        response = requests.post(
            url,
            data={
                "data": query
            },
            headers={
                "User-Agent": "SafeRouteAI/1.0"
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data.get("elements", [])

    except requests.exceptions.RequestException as error:

        st.error(
            f"Unable to load nearby places: {error}"
        )

        return []

    except Exception as error:

        st.error(
            f"Unexpected error while loading nearby places: {error}"
        )

        return []
    # =====================================================
# OFFLINE SAFETY INFORMATION
# =====================================================

def show_offline_safety():

    st.markdown(
        """
        <div class="hero-title">
            Offline Safety Support
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-text">
            Essential safety information remains available even with limited connectivity.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.info(
        "📡 Offline Safety Mode is active. "
        "Your essential safety information is still available."
    )

    st.write("")

    # Last known location
    st.markdown(
        '<div class="section-heading">📍 Last Known Location</div>',
        unsafe_allow_html=True
    )

    st.write("")

    if (
        st.session_state.latitude is not None
        and st.session_state.longitude is not None
    ):

        st.success(
            f"Latitude: {st.session_state.latitude} | "
            f"Longitude: {st.session_state.longitude}"
        )

    else:

        st.warning(
            "No location has been saved yet."
        )

    st.write("")
    st.write("")

    # Emergency numbers
    st.markdown(
        '<div class="section-heading">🚨 Emergency Numbers</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="dashboard-card">
                <div class="card-title">🚓 Police</div>
                <div class="card-text">
                    Emergency Number: <b>112</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="dashboard-card">
                <div class="card-title">🚑 Ambulance</div>
                <div class="card-text">
                    Emergency Number: <b>108</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="dashboard-card">
                <div class="card-title">🔥 Fire Services</div>
                <div class="card-text">
                    Emergency Number: <b>101</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.write("")

    # Trusted contacts
    st.markdown(
        '<div class="section-heading">👥 Trusted Contacts</div>',
        unsafe_allow_html=True
    )

    st.write("")

    if st.session_state.trusted_contacts:

        for contact in st.session_state.trusted_contacts:

            st.html(
                f"""
                <div class="dashboard-card">

                    <div class="card-title">
                        👥 {contact["name"]}
                    </div>

                    <div class="card-text">
                        📞 {contact["phone"]}<br>
                        ❤️ {contact["relationship"]}
                    </div>

                </div>
                """
            )

            st.write("")

    else:

        st.info(
            "No trusted contacts saved yet."
        )


# =====================================================
# LOGIN / SIGNUP PAGE
# =====================================================

if not st.session_state.logged_in:

    st.markdown(
        '<div class="brand">✦ SAFEROUTE AI</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:

        st.markdown(
            """
            <div class="hero-title">
                Your destination matters.<br>
                Your journey should be safe too.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="hero-text">
                AI-powered route intelligence that helps you choose
                the safest way to reach your destination — not just the shortest.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")
        st.write("")

        login_tab, signup_tab = st.tabs(
            ["Login", "Create Account"]
        )

        with login_tab:

            email = st.text_input(
                "Email or phone number",
                key="login_email"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            st.write("")

            if st.button(
                "Login to SafeRoute",
                use_container_width=True
            ):

                if email and password:

                    st.session_state.logged_in = True
                    st.session_state.page = "dashboard"

                    st.rerun()

                else:

                    st.warning(
                        "Please enter your email and password."
                    )

        with signup_tab:

            name = st.text_input(
                "Full name",
                key="signup_name"
            )

            email = st.text_input(
                "Email or phone number",
                key="signup_email"
            )

            password = st.text_input(
                "Create password",
                type="password",
                key="signup_password"
            )

            st.write("")

            if st.button(
                "Create SafeRoute Account",
                use_container_width=True
            ):

                if name and email and password:

                    st.session_state.logged_in = True
                    st.session_state.page = "dashboard"

                    st.rerun()

                else:

                    st.warning(
                        "Please complete all fields."
                    )


# =====================================================
# MAIN APPLICATION
# =====================================================

else:

    # =================================================
    # SIDEBAR
    # =================================================

    with st.sidebar:

        st.markdown(
            '<div class="brand">✦ SAFEROUTE AI</div>',
            unsafe_allow_html=True
        )

        st.write("")
        st.write("")

        st.markdown(f"### {t['overview']}")

        if st.button(
            f"⌂  {t['dashboard']}",
            use_container_width=True
        ):

            st.session_state.page = "dashboard"
            st.rerun()

        if st.button(
            f"🛡  {t['safe_routes']}",
            use_container_width=True
        ):

            st.session_state.page = "routes"
            st.rerun()

        if st.button(
            f"⌖  {t['safe_around_me']}",
            use_container_width=True
        ):

            st.session_state.page = "around_me"
            st.rerun()

        if st.button(
            f"🚨  {t['emergency_sos']}",
            use_container_width=True
        ):

            st.session_state.page = "sos"
            st.rerun()
        if st.button(
            "👥  Trusted Contacts",
            use_container_width=True
            ):
            st.session_state.page = "contacts"
            st.rerun()
        if st.button(
    "📡  Offline Support",
    use_container_width=True
):

           st.session_state.page = "offline"
           st.rerun()    

        st.write("")

        st.markdown(f"### {t['settings']}")

        selected_language = st.selectbox(
            f"🌐 {t['language']}",
            [
                "English",
                "తెలుగు",
                "हिन्दी",
                "தமிழ்",
                "ಕನ್ನಡ"
            ],
            index=[
                "English",
                "తెలుగు",
                "हिन्दी",
                "தமிழ்",
                "ಕನ್ನಡ"
            ].index(st.session_state.language)
        )

        if selected_language != st.session_state.language:

            st.session_state.language = selected_language

            st.rerun()

        st.write("")

        if st.button(
            t["logout"],
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.rerun()


    # =================================================
    # DASHBOARD
    # =================================================
# =================================================
# DASHBOARD
# =================================================


if st.session_state.page == "dashboard":

    show_dashboard(t)

elif st.session_state.page == "routes":
    show_routes(
        t,
        analyze_route
    )
    
    # =====================================================
    # SAFE ROUTES
    # =====================================================



    # =====================================================
    # SAFE AROUND ME
    # =====================================================

elif st.session_state.page == "around_me":

        st.markdown(
            '<div class="brand">✦ SAFEROUTE AI</div>',
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown(
            f"""
            <div class="hero-title">
                {t["safe_around_title"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="hero-text">
                {t["safe_around_desc"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if (
            st.session_state.latitude is None
            or st.session_state.longitude is None
        ):

            st.warning(
                "Please go to the Dashboard and click "
                "'Use my live location' first."
            )

        else:

            latitude = st.session_state.latitude
            longitude = st.session_state.longitude

            st.success(
                t["use_saved_location"]
            )

            if st.button(
                t["find_places"],
                use_container_width=True
            ):

                with st.spinner(
                    t["searching"]
                ):

                    places = get_nearby_places(
                        latitude,
                        longitude
                    )

                    st.session_state.nearby_places = places

            places = st.session_state.nearby_places

            if places:

                st.success(
                    f"Found {len(places)} nearby safety places."
                )

                around_map = folium.Map(
                    location=[
                        latitude,
                        longitude
                    ],
                    zoom_start=14
                )

                folium.Marker(
                    [
                        latitude,
                        longitude
                    ],
                    popup="📍 Your Current Location",
                    tooltip="You are here",
                    icon=folium.Icon(
                        color="red",
                        icon="user"
                    )
                ).add_to(around_map)

                for place in places:

                    tags = place.get(
                        "tags",
                        {}
                    )

                    name = tags.get(
                        "name",
                        "Unnamed Safety Place"
                    )

                    amenity = tags.get(
                        "amenity",
                        "Safety Place"
                    )

                    if "lat" in place:

                        place_latitude = place["lat"]
                        place_longitude = place["lon"]

                    else:

                        place_latitude = place["center"]["lat"]
                        place_longitude = place["center"]["lon"]

                    if amenity == "police":

                        icon_color = "blue"
                        icon_name = "shield"

                    elif amenity == "hospital":

                        icon_color = "green"
                        icon_name = "plus"

                    else:

                        icon_color = "orange"
                        icon_name = "fire"

                    folium.Marker(
                        [
                            place_latitude,
                            place_longitude
                        ],
                        popup=f"""
                        <b>{name}</b><br>
                        Type: {amenity}
                        """,
                        tooltip=name,
                        icon=folium.Icon(
                            color=icon_color,
                            icon=icon_name
                        )
                    ).add_to(around_map)

                st_folium(
                    around_map,
                    width=1200,
                    height=600
                )

                st.write("")

                st.markdown(
                    f'<div class="section-heading">{t["nearby_resources"]}</div>',
                    unsafe_allow_html=True
                )

                st.write("")

                for place in places:

                    tags = place.get(
                        "tags",
                        {}
                    )

                    name = tags.get(
                        "name",
                        "Unnamed Safety Place"
                    )

                    amenity = tags.get(
                        "amenity",
                        "Safety Place"
                    )

                    if amenity == "police":

                        st.info(
                            f"👮 {name} — Police Station"
                        )

                    elif amenity == "hospital":

                        st.success(
                            f"🏥 {name} — Hospital"
                        )

                    elif amenity == "fire_station":

                        st.warning(
                            f"🚒 {name} — Fire Station"
                        )

            else:

                st.info(
                    t["search_instruction"]
                )


    # =====================================================
    # EMERGENCY SOS
    # =====================================================

    # =====================================================
    # EMERGENCY SOS
    # =====================================================

elif st.session_state.page == "sos":
    show_emergency(t)
                   # =====================================================
    # TRUSTED CONTACTS
    # =====================================================

elif st.session_state.page == "trusted_contacts":

    show_trusted_contacts(t)
    # =====================================================
    # OFFLINE SUPPORT
    # =====================================================

elif st.session_state.page == "offline":

        show_offline_safety()