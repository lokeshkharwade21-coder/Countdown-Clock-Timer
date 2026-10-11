
import streamlit as st
import time

st.set_page_config(
    page_title="Countdown Clock & Timer",
    page_icon="⏱️",
    layout="centered"
)

# Dark theme styling similar to the original Tkinter app
st.markdown("""
<style>
.stApp {
    background-color: #101827;
    color: white;
}
h1 {
    color: #60A5FA !important;
    text-align: center;
    font-size: 32px !important;
}
.timer-display {
    color: #34D399;
    text-align: center;
    font-family: monospace;
    font-size: 48px;
    font-weight: bold;
    padding: 18px 0;
}
.status {
    text-align: center;
    color: white;
    font-size: 17px;
    padding-bottom: 15px;
}
div.stButton > button {
    width: 100%;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>COUNTDOWN TIMER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>Set your time</p>",
            unsafe_allow_html=True)

if "remaining" not in st.session_state:
    st.session_state.remaining = 0
    st.session_state.running = False
    st.session_state.paused = False
    st.session_state.end_time = 0
    st.session_state.status = "Ready to start"
    st.session_state.finished = False

h_col, m_col, s_col = st.columns(3)

with h_col:
    hours = st.number_input("Hours", min_value=0, step=1, value=0)
with m_col:
    minutes = st.number_input("Minutes", min_value=0, max_value=59,
                              step=1, value=0)
with s_col:
    seconds = st.number_input("Seconds", min_value=0, max_value=59,
                              step=1, value=0)

st.markdown("---")

remaining = st.session_state.remaining
if st.session_state.running:
    remaining = max(0, int(st.session_state.end_time - time.time() + 0.999))
    st.session_state.remaining = remaining

hh = remaining // 3600
mm = (remaining % 3600) // 60
ss = remaining % 60

display_color = "#F87171" if st.session_state.finished else "#34D399"
st.markdown(
    f"<div class='timer-display' style='color:{display_color}'>"
    f"{hh:02d}:{mm:02d}:{ss:02d}</div>",
    unsafe_allow_html=True
)

if st.session_state.running and remaining <= 0:
    st.session_state.running = False
    st.session_state.paused = False
    st.session_state.finished = True
    st.session_state.status = "Time's up! Alarm ringing!"
    st.rerun()

status_color = (
    "#F87171" if st.session_state.finished
    else "#FBBF24" if st.session_state.paused
    else "#34D399" if st.session_state.running
    else "white"
)
st.markdown(
    f"<div class='status' style='color:{status_color}'>"
    f"{st.session_state.status}</div>",
    unsafe_allow_html=True
)

start_col, pause_col, reset_col = st.columns(3)

with start_col:
    start_clicked = st.button("START", type="primary",
                              disabled=st.session_state.running)
with pause_col:
    pause_clicked = st.button("PAUSE",
                              disabled=not st.session_state.running)
with reset_col:
    reset_clicked = st.button("RESET")

if start_clicked:
    if not st.session_state.paused:
        total = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        if total <= 0:
            st.error("Please enter a time greater than zero.")
        else:
            st.session_state.remaining = total
            st.session_state.end_time = time.time() + total
            st.session_state.running = True
            st.session_state.paused = False
            st.session_state.finished = False
            st.session_state.status = "Timer is running..."
            st.rerun()
    else:
        st.session_state.end_time = time.time() + st.session_state.remaining
        st.session_state.running = True
        st.session_state.paused = False
        st.session_state.status = "Timer is running..."
        st.rerun()

if pause_clicked:
    st.session_state.remaining = max(
        0, int(st.session_state.end_time - time.time() + 0.999)
    )
    st.session_state.running = False
    st.session_state.paused = True
    st.session_state.status = "Timer paused"
    st.rerun()

if reset_clicked:
    st.session_state.remaining = 0
    st.session_state.running = False
    st.session_state.paused = False
    st.session_state.finished = False
    st.session_state.status = "Ready to start"
    st.rerun()

# Refresh the display while the timer is running
if st.session_state.running:
    time.sleep(1)
    st.rerun()
