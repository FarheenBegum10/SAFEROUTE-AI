import streamlit as st


def show_routes(t, analyze_route):

    st.markdown(
        '<div class="brand">✦ SAFEROUTE AI</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown(
        f"""
        <div class="hero-title">
            {t["choose_safer"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="hero-text">
            {t["fastest_not_safest"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if (
        st.session_state.latitude is not None
        and st.session_state.longitude is not None
    ):

        start_location = (
            f"📍 Current Location "
            f"({st.session_state.latitude}, "
            f"{st.session_state.longitude})"
        )

        st.success(
            "Your live location is being used as the starting point."
        )

    else:

        start_location = st.text_input(
            t["starting_point"],
            placeholder=t["starting_placeholder"],
            key="routes_starting_point"
        )

    destination = st.text_input(
        t["destination"],
        placeholder=t["destination_placeholder"],
        key="routes_destination"
    )

    st.write("")

    if st.button(
        t["analyze_route"],
        use_container_width=True,
        key="analyze_route_button"
    ):

        if destination and start_location:

            route_a = analyze_route(
                route_name="Route A",
                distance="3.2 km",
                crime_risk=75,
                lighting=40,
                cctv=35,
                traffic=50,
                police_proximity=30
            )

            route_b = analyze_route(
                route_name="Route B",
                distance="4.0 km",
                crime_risk=20,
                lighting=85,
                cctv=80,
                traffic=70,
                police_proximity=75
            )

            routes = [
                route_a,
                route_b
            ]

            safest_route = max(
                routes,
                key=lambda route: route["safety_score"]
            )

            st.write("")

            st.markdown(
                f"""
                <div class="section-heading">
                    {t["route_analysis"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.success(
                f"{t['recommended']}: "
                f"{safest_route['route_name']} "
                f"with a {t['safety_score'].lower()} of "
                f"{safest_route['safety_score']}/100."
            )

            col1, col2 = st.columns(2)

            for index, route in enumerate(routes):

                with [
                    col1,
                    col2
                ][index]:

                    st.html(
                        f"""
                        <div class="route-card">

                            <div class="route-title">
                                {route['route_name']}
                            </div>

                            <br>

                            <div class="route-score">
                                {route['safety_score']}/100
                            </div>

                            <div class="route-info">
                                {t["safety_score"]}
                            </div>

                            <br>

                            <div class="route-info">
                                {t["distance"]}: {route['distance']}
                            </div>

                            <div class="route-info">
                                {t["risk_level"]}: {route['risk_level']}
                            </div>

                        </div>
                        """
                    )

        else:

            st.warning(
                "Please enter a destination."
            )