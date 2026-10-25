import streamlit as st


def show_around_me(t):

    st.markdown(
        '<div class="brand">✦ SAFEROUTE AI</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown(
        f"""
        <div class="hero-title">
            {t["safe_around_card"]}
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
    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.html(
            """
            <div class="dashboard-card">

                <div class="card-title">
                    🚓 Nearby Police Stations
                </div>

                <div class="card-text">
                    Find nearby police stations and emergency support locations.
                </div>

            </div>
            """
        )

    with col2:

        st.html(
            """
            <div class="dashboard-card">

                <div class="card-title">
                    🏥 Nearby Hospitals
                </div>

                <div class="card-text">
                    Quickly locate nearby hospitals and medical assistance.
                </div>

            </div>
            """
        )

    with col3:

        st.html(
            """
            <div class="dashboard-card">

                <div class="card-title">
                    🏪 Safe Public Places
                </div>

                <div class="card-text">
                    Discover nearby public places where help is easily available.
                </div>

            </div>
            """
        )
        st.write("")
        st.write("")

    if st.button(
        "Find Safety Places Near Me",
        use_container_width=True
    ):

        if (
            st.session_state.latitude is not None
            and st.session_state.longitude is not None
        ):

            latitude = st.session_state.latitude
            longitude = st.session_state.longitude

            st.success(
                "📍 Searching for nearby safety places..."
            )

            st.write("")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.html(
                    """
                    <div class="dashboard-card">

                        <div class="card-title">
                            🚓 Police Stations
                        </div>

                        <div class="card-text">
                            Nearby police stations available for emergency support.
                        </div>

                    </div>
                    """
                )

            with col2:

                st.html(
                    """
                    <div class="dashboard-card">

                        <div class="card-title">
                            🏥 Hospitals
                        </div>

                        <div class="card-text">
                            Nearby hospitals and medical assistance locations.
                        </div>

                    </div>
                    """
                )

            with col3:

                st.html(
                    """
                    <div class="dashboard-card">

                        <div class="card-title">
                            🏪 Public Places
                        </div>

                        <div class="card-text">
                            Nearby public places where help is easily available.
                        </div>

                    </div>
                    """
                )

        else:

            st.warning(
                "Please go to the Dashboard and click 'Use my live location' first."
            )