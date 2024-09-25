import streamlit as st

st.set_page_config(
        page_title="Welcome",
        page_icon="🎵",
        initial_sidebar_state="expanded",
)

st.write("# Favourite Music Releases Visualiser")

st.sidebar.success("Select a page above!")

st.markdown(
        """
        This is a multi-page app which visualises a list of my favourite music releases!

        I hope that you find an Album, EP, Soundtrack and/or other music release that would also be/become a favourite for you!

        **Select a page from the sidebar** that may be of interest to you! 😄

        Enjoy!
        """
)
