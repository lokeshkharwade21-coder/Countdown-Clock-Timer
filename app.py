
import streamlit as st
import time

st.set_page_config(
    page_title="Countdown Clock & Timer",
    page_icon="⏱️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- SESSION STATE ----------
defaults = {
    "remaining": 0,
    "end_time": None,
    "running": False,
    "paused": False,
    "finished": False,
    "status": "Ready to start",
    "hours": "00",
    "minutes": "00",
    "seconds": "00",
    "message": "",
    "message_type": "error"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- CSS: MATCH ORIGINAL TKINTER DESIGN ----------
st.markdown("""
<style>
.stApp {
    background-color: #101827;
    color: white;
}
header[data-testid="stHeader"] {
    background: #101827;
}
#MainMenu, footer, [data-testid="stToolbar"] {
    visibility: hidden;
}
.block-container {
    max-width: 525px;
    padding-top: 25px;
    padding-bottom: 35px;
}
h1 {
    color: #60A5FA !important;
    text-align: center;
    font-family: Arial, sans-serif;
    font-size: 34px !important;
    font-weight: bold !important;
    white-space: nowrap;
    margin-bottom: 30px;
}
.subtitle {
    text-align: center;
    color: white;
    font: 20px Arial, sans-serif;
    margin-bottom: 23px;
}
div[data-testid="stTextInput"] label {
    color: #CBD5E1 !important;
    text-align: center;
    display: block;
    font-size: 15px;
}
div[data-testid="stTextInput"] input {
    background: #FFFFFF !important;
    color: #111827 !important;
    border: 1px solid #9CA3AF !important;
    border-radius: 0 !important;
    text-align: center;
    font-family: Arial, sans-serif;
    font-size: 23px !important;
    font-weight: bold;
    height: 43px;
}
.timer-display {
    text-align: center;
    color: #34D399;
    font-family: Consolas, monospace;
    font-size: clamp(37px, 9vw, 57px);
    line-height: 1.3;
    font-weight: bold;
    white-space: nowrap;
    margin-top: 40px;
    margin-bottom: 26px;
    font-variant-numeric: tabular-nums;
}
.timer-status {
    text-align: center;
    color: white;
    font: 18px Arial, sans-serif;
    margin-bottom: 27px;
    min-height: 24px;
}
div.st-key-start button {
    background: #16A34A !important;
    color: white !important;
}
div.st-key-pause button {
    background: #D97706 !important;
    color: white !important;
}
div.st-key-reset button {
    background: #DC2626 !important;
    color: white !important;
}
div.st-key-start button,
div.st-key-pause button,
div.st-key-reset button {
    border-radius: 0 !important;
    height: 43px;
    font-family: Arial, sans-serif;
    font-size: 17px;
    font-weight: bold;
    border: 1px solid #64748b !important;
}
div.st-key-start button:hover,
div.st-key-pause button:hover,
div.st-key-reset button:hover {
    filter: brightness(1.12);
}
div[data-testid="stAlert"] {
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADING ----------
st.markdown(
    '<h1>COUNTDOWN TIMER</h1>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Set your time</div>',
    unsafe_allow_html=True
)

# ---------- INPUTS ----------
c1, c2, c3 = st.columns(3, gap="small")

with c1:
    st.text_input("Hours", key="hours", max_chars=3)

with c2:
    st.text_input("Minutes", key="minutes", max_chars=2)

with c3:
    st.text_input("Seconds", key="seconds", max_chars=2)


def parse_time():
    values = [
        st.session_state.hours.strip(),
        st.session_state.minutes.strip(),
        st.session_state.seconds.strip()
    ]

    if not all(v.isdigit() for v in values):
        raise ValueError(
            "Enter valid whole numbers for hours, minutes and seconds."
        )

    h, m, s = map(int, values)

    if h < 0 or not 0 <= m <= 59 or not 0 <= s <= 59:
        raise ValueError(
            "Minutes and seconds must be between 0 and 59."
        )

    total = h * 3600 + m * 60 + s

    if total <= 0:
        raise ValueError("Please enter a time greater than zero.")

    return total


# ---------- BUTTONS ----------
b1, b2, b3 = st.columns(3, gap="small")

with b1:
    start_clicked = st.button(
        "START", key="start",
        use_container_width=True
    )

with b2:
    pause_clicked = st.button(
        "PAUSE", key="pause",
        use_container_width=True
    )

with b3:
    reset_clicked = st.button(
        "RESET", key="reset",
        use_container_width=True
    )


# ---------- START ----------
if start_clicked:
    st.session_state.message = ""

    if st.session_state.running:
        st.session_state.status = "Timer is already running..."
    else:
        try:
            if not st.session_state.paused:
                st.session_state.remaining = parse_time()

            if st.session_state.remaining > 0:
                st.session_state.end_time = (
                    time.monotonic() + st.session_state.remaining
                )
                st.session_state.running = True
                st.session_state.paused = False
                st.session_state.finished = False
                st.session_state.status = "Timer is running..."

        except ValueError as error:
            st.session_state.message = str(error)
            st.session_state.message_type = "error"
            st.session_state.status = "Ready to start"


# ---------- PAUSE ----------
if pause_clicked:
    if st.session_state.running:
        st.session_state.remaining = max(
            0,
            int(
                st.session_state.end_time
                - time.monotonic() + 0.999
            )
        )
        st.session_state.running = False
        st.session_state.paused = True
        st.session_state.end_time = None
        st.session_state.status = "Timer paused"
    else:
        st.session_state.status = "Timer is not running"


# ---------- RESET ----------
if reset_clicked:
    st.session_state.remaining = 0
    st.session_state.end_time = None
    st.session_state.running = False
    st.session_state.paused = False
    st.session_state.finished = False
    st.session_state.status = "Ready to start"
    st.session_state.hours = "00"
    st.session_state.minutes = "00"
    st.session_state.seconds = "00"
    st.session_state.message = ""


# ---------- LIVE COUNTDOWN ----------
if st.session_state.running:
    st.session_state.remaining = max(
        0,
        int(
            st.session_state.end_time
            - time.monotonic() + 0.999
        )
    )

    if st.session_state.remaining <= 0:
        st.session_state.running = False
        st.session_state.paused = False
        st.session_state.end_time = None
        st.session_state.finished = True
        st.session_state.status = "Time's up! Alarm ringing!"


# ---------- DISPLAY ----------
total = st.session_state.remaining
hh = total // 3600
mm = (total % 3600) // 60
ss = total % 60

display_color = (
    "#F87171" if st.session_state.finished else "#34D399"
)

st.markdown(
    f'<div class="timer-display" style="color:{display_color}">'
    f'{hh:02d}:{mm:02d}:{ss:02d}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="timer-status">{st.session_state.status}</div>',
    unsafe_allow_html=True
)

if st.session_state.message:
    st.error(st.session_state.message)

if st.session_state.finished:
    st.warning("Time is up!")

# Refresh the page periodically while running so the countdown
# updates in the browser.
if st.session_state.running:
    time.sleep(0.2)
    st.rerun()
