import streamlit as st

# footer
footer = """<style> .footer {
position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; color: black; text-align: center;
}
</style>
<div class="footer">
This is a test
</div>
"""
st.markdown(footer, unsafe_allow_html=False)