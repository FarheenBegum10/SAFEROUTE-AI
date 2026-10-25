import streamlit as st


def show_trusted_contacts(t):

    st.markdown(
        '<div class="brand">✦ SAFEROUTE AI</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown(
        f"""
        <div class="hero-title">
            {t["trusted_contacts"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="hero-text">
            {t["trusted_contacts_desc"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    st.html(
        """
        <div class="dashboard-card">

            <div class="card-title">
                Add a Trusted Contact
            </div>

            <div class="card-text">
                Add someone you trust to contact during an emergency.
            </div>

        </div>
        """
    )

    st.write("")

    name = st.text_input(
        "Contact Name",
        placeholder="Enter name"
    )

    phone = st.text_input(
        "Phone Number",
        placeholder="Enter phone number"
    )

    st.write("")

    if st.button(
        "Add Trusted Contact",
        use_container_width=True
    ):

        if name and phone:

            if "trusted_contacts_list" not in st.session_state:

                st.session_state.trusted_contacts_list = []

            st.session_state.trusted_contacts_list.append(
                {
                    "name": name,
                    "phone": phone
                }
            )

            st.success(
                f"{name} has been added as a trusted contact."
            )

            st.rerun()

        else:

            st.warning(
                "Please enter both name and phone number."
            )

    st.write("")
    st.write("")

    st.markdown(
        """
        <div class="section-heading">
            Your Trusted Contacts
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if (
        "trusted_contacts_list" in st.session_state
        and st.session_state.trusted_contacts_list
    ):

        for index, contact in enumerate(
            st.session_state.trusted_contacts_list
        ):

            st.html(
                f"""
                <div class="dashboard-card">

                    <div class="card-title">
                        👤 {contact["name"]}
                    </div>

                    <div class="card-text">
                        📞 {contact["phone"]}
                    </div>

                </div>
                """
            )

            if st.button(
                f"Remove {contact['name']}",
                key=f"remove_contact_{index}"
            ):

                st.session_state.trusted_contacts_list.pop(index)

                st.rerun()

    else:

        st.info(
            "No trusted contacts added yet."
        )