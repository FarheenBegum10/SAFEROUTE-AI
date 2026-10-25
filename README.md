# 🛡️ SafeRoute AI - Safe Route Navigation System

An AI-powered navigation web app that finds not just the fastest or shortest route, but the **safest route**.

🔗 **Live demo:** https://YOUR-APP-NAME.streamlit.app

## Features
- Safest-route analysis between two locations
- Interactive map (Folium)
- Around Me - nearby safety places (hospitals, police, etc.)
- Emergency SOS page
- Trusted contacts
- Multilingual support

## Tech Stack
Python, Streamlit, Folium, OpenStreetMap / Overpass API

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project structure
```
app.py            # main Streamlit app
app_pages/        # dashboard, routes, around_me, emergency, trusted_contacts, settings
components/       # map, cards
utils/            # helpers, translations
styles/           # CSS styles
```
