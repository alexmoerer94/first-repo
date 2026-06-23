import streamlit as st
from activity_service import ActivityService

service = ActivityService()

st.title("Activity Tracker")

tab1, tab2, tab3 = st.tabs(["Log", "Today", "History"])

with tab1:
    desc = st.text_input("What did you do?")
    category = st.selectbox("Category", ["work","break","exercise","social","learning","other"])
    notes = st.text_area("Notes")

    if st.button("Log Activity"):
        service.log_activity(desc, category, notes)
        st.success("Logged!")

with tab2:
    st.subheader("Today's Activities")
    for a in service.get_today():
        st.write(a)

with tab3:
    st.subheader("History")
    for a in service.get_history()[:50]:
        st.write(a)