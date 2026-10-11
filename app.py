
import streamlit as st
import time

st.set_page_config(
    page_title="Countdown Clock & Timer",
    page_icon="⏱️",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: #101827;
    color: white;
}
.block-container {
    max-width: 650px;
    padding-top: 2rem;
}
.timer-title {
    color: #60A5FA;
    text-align: center;
    font-family: Arial, sans-serif;
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 25px;
}
.timer-display {
    text-align: center;
    font-family: Consolas, monospace;
    font-size: clamp(36px, 8vw, 52px);
    font-weight: bold;
    margin: 20px 0;
}
.timer-status {
    text-align: center;
    font-family: Arial, sans-serif;
    font-size: 15px;
    margin-bottom: 24px;
}
label, p {
    color: white;
}
div[data-testid="stNumberInput"] input {
    text-align: center;
    background: #ffffff;
    color: #101827;
    font-size: 18px;
}
div.stButton > button {
    width: 100%;
    min-height: 43px;
    font-weight: bold;
    border-radius: 6px;
}
div.stButton > button[kind="primary"] {
    background: #16A34A;
    color: white;
    border: none;
}
div.stButton > button[kind="secondary"] {
    background: #D97706;
    color: white;
    border: none;
}
div[data-testid="stButton"]:nth-of-type(3) button {
    background: #DC2626;
    color: white;
}
</style>
""", unsafe_allow_html=True)

if "remaining" not in st.session_state:
    st.session_state.remaining = 0
    st.session_state.running = False
    st.session_state.paused = False
    st.session_state.end_time = 0.0
    st.session_state.status = "Ready to start"
    st.session_state.finished = False

st.markdown(
    '<div class="timer-title">COUNTDOWN TIMER</div>',
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; color:#CBD5E1;'>Set your time</p>",
    unsafe_allow_html=True
)

@st.fragment(run_every="200ms")
def countdown_interface():
    c1, c2, c3 = st.columns(3)

    with c1:
        h = st.number_input(
            "Hours", min_value=0, step=1,
            value=0, key="hours_input",
            disabled=st.session_state.running
        )

    with c2:
        m = st.number_input(
            "Minutes", min_value=0, max_value=59,
            step=1, value=0, key="minutes_input",
            disabled=st.session_state.running
        )

    with c3:
        s = st.number_input(
            "Seconds", min_value=0, max_value=59,
            step=1, value=0, key="seconds_input",
            disabled=st.session_state.running
        )

    if st.session_state.running:
        st.session_state.remaining = max(
            0,
            int(st.session_state.end_time - time.monotonic() + 0.999)
        )

        if st.session_state.remaining == 0:
            st.session_state.running = False
            st.session_state.paused = False
            st.session_state.finished = True
            st.session_state.status = "Time's up! Alarm ringing!"

    remaining = st.session_state.remaining
    hh = remaining // 3600
    mm = (remaining % 3600) // 60
    ss = remaining % 60

    color = "#F87171" if st.session_state.finished else "#34D399"

    st.markdown(
        f'<div class="timer-display" style="color:{color}">'
        f'{hh:02d}:{mm:02d}:{ss:02d}</div>',
        unsafe_allow_html=True
    )

    if st.session_state.running:
        status_color = "#34D399"
    elif st.session_state.paused:
        status_color = "#FBBF24"
    elif st.session_state.finished:
        status_color = "#F87171"
    else:
        status_color = "white"

    st.markdown(
        f'<div class="timer-status" style="color:{status_color}">'
        f'{st.session_state.status}</div>',
        unsafe_allow_html=True
    )

    b1, b2, b3 = st.columns(3)

    with b1:
        start_clicked = st.button(
            "START", type="primary",
            disabled=st.session_state.running,
            use_container_width=True
        )

    with b2:
        pause_clicked = st.button(
            "PAUSE", type="secondary",
            disabled=not st.session_state.running,
            use_container_width=True
        )

    with b3:
        reset_clicked = st.button(
            "RESET",
            use_container_width=True
        )

    if start_clicked:
        if not st.session_state.paused:
            total = int(h) * 3600 + int(m) * 60 + int(s)

            if total <= 0:
                st.session_state.status = (
                    "Please enter a time greater than zero."
                )
                st.session_state.error = (
                    "Enter a time greater than zero."
                )
            else:
                st.session_state.remaining = total
                st.session_state.end_time = time.monotonic() + total
                st.session_state.running = True
                st.session_state.paused = False
                st.session_state.finished = False
                st.session_state.status = "Timer is running..."
                st.session_state.error = ""
        else:
            st.session_state.end_time = (
                time.monotonic() + st.session_state.remaining
            )
            st.session_state.running = True
            st.session_state.paused = False
            st.session_state.status = "Timer is running..."

    if pause_clicked:
        st.session_state.remaining = max(
            0,
            int(st.session_state.end_time - time.monotonic() + 0.999)
        )
        st.session_state.running = False
        st.session_state.paused = True
        st.session_state.status = "Timer paused"

    if reset_clicked:
        st.session_state.remaining = 0
        st.session_state.running = False
        st.session_state.paused = False
        st.session_state.finished = False
        st.session_state.status = "Ready to start"
        st.session_state.error = ""
        st.session_state.hours_input = 0
        st.session_state.minutes_input = 0
        st.session_state.seconds_input = 0

    if st.session_state.get("error"):
        st.warning(st.session_state.error)

countdown_interface()
