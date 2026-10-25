import streamlit as st
import folium
from streamlit_folium import st_folium


def show_dashboard(t):

    st.markdown(
        '<div class="brand">✦ SAFEROUTE AI</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown(
        f"""
        <div class="hero-title">
            {t["where_going"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="hero-text">
            {t["find_safest_way"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    destination = st.text_input(
        t["search_destination"],
        placeholder=t["destination_placeholder"],
        key="dashboard_destination"
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            t["use_location"],
            use_container_width=True,
            key="dashboard_use_location"
        ):

            st.session_state.latitude = 17.56170212169957
            st.session_state.longitude = 78.45000734903626

            st.success(
                "📍 Live location detected successfully!"
            )

            st.rerun()

    with col2:

        if st.button(
            t["find_route"],
            use_container_width=True,
            key="dashboard_find_route"
        ):

            if destination:

                st.session_state.page = "routes"
                st.rerun()

            else:

                st.warning(
                    "Please enter a destination first."
                )

    st.write("")
    st.write("")

    # LOCATION CARD

    if (
        st.session_state.latitude is not None
        and st.session_state.longitude is not None
    ):

        st.success(
            f"📍 Current Location Detected\n\n"
            f"Latitude: {st.session_state.latitude}\n\n"
            f"Longitude: {st.session_state.longitude}"
        )

    st.write("")

    # LIVE SAFETY MAP

    st.markdown(
        f"""
        <div class="section-heading">
            {t["live_safety_map"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if (
        st.session_state.latitude is not None
        and st.session_state.longitude is not None
    ):

        latitude = st.session_state.latitude
        longitude = st.session_state.longitude

        live_map = folium.Map(
            location=[
                latitude,
                longitude
            ],
            zoom_start=15
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
        ).add_to(live_map)

        st_folium(
            live_map,
            width=1200,
            height=500
        )

    else:

        st.info(
            t["location_instruction"]
        )
    # SAFETY COMPANION
    st.markdown(
        f"""
        <div class="section-heading">
            {t["safety_companion"]}
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.html(
            f"""
            <div class="dashboard-card">

                <div class="card-title">
                    {t["safe_routes_card"]}
                </div>

                <div class="card-text">
                    {t["safe_routes_desc"]}
                </div>

            </div>
            """
        )
    with col2:
        if st.button(
            t["safe_around_card"],
            use_container_width=True,
            key="safe_around_button"
        ):

           st.session_state.page = "around_me"
           st.rerun()
    with col3:

        st.html(
            f"""
            <div class="sos-card">

                <div class="card-title">
                    {t["sos_card"]}
                </div>

                <div class="card-text">
                    {t["sos_desc"]}
                </div>

            </div>
            """
        )

    st.write("")
    st.write("")

    # MORE FEATURES

    st.markdown(
        f"""
        <div class="section-heading">
            {t["more_features"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.html(
            f"""
            <div class="dashboard-card">

                <div class="card-title">
                    {t["multi_language"]}
                </div>

                <div class="card-text">
                    {t["multi_language_desc"]}
                </div>

            </div>
            """
        )

    with col2:

        st.html(
            f"""
            <div class="dashboard-card">

                <div class="card-title">
                    {t["offline_support"]}
                </div>

                <div class="card-text">
                    {t["offline_support_desc"]}
                </div>

            </div>
            """
        )
    with col3:
        st.html(
        f"""
        <div class="dashboard-card">

            <div class="card-title">
                {t["trusted_contacts"]}
            </div>

            <div class="card-text">
                {t["trusted_contacts_desc"]}
            </div>

        </div>
        """
    )

    if st.button(
        "Open Trusted Contacts",
        use_container_width=True
    ):

        st.session_state.page = "trusted_contacts"

        st.rerun()
    