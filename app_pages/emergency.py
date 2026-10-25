import streamlit as st


def show_emergency(t):

    st.markdown(
        '<div class="brand">✦ SAFEROUTE AI</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown(
        f"""
        <div class="hero-title">
            {t["emergency_title"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="hero-text">
            {t["emergency_desc"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    st.html(
        """
        <div class="sos-card">

            <div class="card-title">
                🚨 Need immediate help?
            </div>

            <div class="card-text">
                Activate SOS to start your emergency safety response.
            </div>

        </div>
        """
    )

    st.write("")
    st.write("")

    if st.button(
        "🚨 Activate Emergency SOS",
        use_container_width=True
    ):

        st.session_state.sos_activated = True

    if st.session_state.get(
        "sos_activated",
        False
    ):

        st.success(
            "🚨 Emergency SOS Activated"
        )

        st.write("")

        st.info(
            "Your emergency response has been initiated."
        )

        st.write("")

        st.markdown(
            """
            <div class="location-card">

                <div class="location-title">
                    📍 Live Location
                </div>

                <div class="location-details">
                    Your current location will be shared with your trusted emergency contacts.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")
        st.write("")

        st.markdown(
            """
            <div class="dashboard-card">

                <div class="card-title">
                    👥 Trusted Emergency Contacts
                </div>

                <div class="card-text">
                    Your saved emergency contacts will be notified during an emergency.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")
        st.write("")

        if st.button(
            "Cancel Emergency SOS",
            use_container_width=True
        ):

            st.session_state.sos_activated = False
            st.rerun()