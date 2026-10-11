
import streamlit as st
import time

st.set_page_config(
    page_title="Countdown Timer",
    page_icon="⏱️",
    layout="centered"
)

# ---------- ORIGINAL DARK THEME ----------
st.markdown("""
<style>
.stApp {
    background: #101827;
    color: #e5e7eb;
}

header[data-testid="stHeader"] {
    background: #101827;
}

.block-container {
    max-width: 500px;
    padding-top: 2.5rem;
    padding-bottom: 2rem;
}

h1 {
    text-align: center;
    color: #60a5fa !important;
    font-family: Arial, sans-serif;
    font-size: 30px !important;
    font-weight: 700 !important;
    letter-spacing: 1px;
}

.set-time {
    text-align: center;
    color: #e5e7eb;
    font-size: 17px;
    margin-top: 18px;
    margin-bottom: 15px;
}

label {
    color: #d1d5db !important;
}

div[data-testid="stNumberInput"] input {
    background: #1e293b;
    color: #ffffff;
    border: 1px solid #475569;
    border-radius: 6px;
    text-align: center;
}

.timer-display {
    background: #0b1220;
    border: 1px solid #263449;
    border-radius: 10px;
    padding: 20px 4px;
    margin-top: 20px;
    margin-bottom: 15px;
    text-align: center;
    color: #22c55e;
    font-family: Consolas, "Courier New", monospace;
    font-size: 49px;
    font-weight: bold;
    letter-spacing: 3px;
}

.status {
    text-align: center;
    color: #cbd5e1;
    font-size: 15px;
    min-height: 25px;
    margin-bottom: 15px;
}

.st-key-start_btn button {
    background: #22c55e !important;
    color: #07130b !important;
    border: none !important;
    font-weight: bold !important;
}

.st-key-pause_btn button {
    background: #f59e0b !important;
    color: #1f1300 !important;
    border: none !important;
    font-weight: bold !important;
}

.st-key-reset_btn button {
    background: #ef4444 !important;
    color: white !important;
    border: none !important;
    font-weight: bold !important;
}

.st-key-start_btn button:hover,
.st-key-pause_btn button:hover,
.st-key-reset_btn button:hover {
    filter: brightness(1.12);
}

.st-key-start_btn button,
.st-key-pause_btn button,
.st-key-reset_btn button {
    min-height: 43px;
    border-radius: 7px;
}

div[data-testid="stAlert"] {
    border-radius: 7px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
defaults = {
    "remaining": 0,
    "end_time": None,
    "running": False,
    "paused": False,
    "finished": False,
    "status": "Set time and press START",
    "error": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- TITLE ----------
st.markdown("<h1>COUNTDOWN TIMER</h1>", unsafe_allow_html=True)
st.markdown(
    '<div class="set-time">Set your time</div>',
    unsafe_allow_html=True
)

# ---------- TIME INPUTS ----------
c1, c2, c3 = st.columns(3)

with c1:
    hours = st.number_input(
        "Hours", min_value=0, max_value=999,
        value=0, step=1, key="hours"
    )

with c2:
    minutes = st.number_input(
        "Minutes", min_value=0, max_value=59,
        value=0, step=1, key="minutes"
    )

with c3:
    seconds = st.number_input(
        "Seconds", min_value=0, max_value=59,
        value=0, step=1, key="seconds"
    )

# ---------- TIMER ACTIONS AND DISPLAY ----------
@st.fragment(run_every="200ms")
def timer_panel():

    # Calculate live remaining time
    if st.session_state.running and st.session_state.end_time is not None:
        st.session_state.remaining = max(
            0, int(st.session_state.end_time - time.monotonic() + 0.999)
        )

        if st.session_state.remaining <= 0:
            st.session_state.running = False
            st.session_state.paused = False
            st.session_state.finished = True
            st.session_state.status = "Time's up!"

    total = st.session_state.remaining

    hh = total // 3600
    mm = (total % 3600) // 60
    ss = total % 60

    display_color = (
        "#ef4444" if st.session_state.finished else "#22c55e"
    )

    st.markdown(
        f"""
        <div class="timer-display"
             style="color:{display_color};">
            {hh:02d}:{mm:02d}:{ss:02d}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="status">{st.session_state.status}</div>',
        unsafe_allow_html=True
    )

    b1, b2, b3 = st.columns(3)

    with b1:
        if st.button("▶ START", key="start_btn", use_container_width=True):
            if st.session_state.running:
                st.session_state.status = "Timer is already running"
            else:
                if not st.session_state.paused:
                    duration = (
                        int(st.session_state.hours) * 3600
                        + int(st.session_state.minutes) * 60
                        + int(st.session_state.seconds)
                    )

                    if duration <= 0:
                        st.session_state.status = "Please enter a valid time"
                        st.rerun()

                    st.session_state.remaining = duration

                if st.session_state.remaining > 0:
                    st.session_state.end_time = (
                        time.monotonic() + st.session_state.remaining
                    )
                    st.session_state.running = True
                    st.session_state.paused = False
                    st.session_state.finished = False
                    st.session_state.status = "Timer is running..."

                st.rerun(scope="fragment")

    with b2:
        if st.button("⏸ PAUSE", key="pause_btn", use_container_width=True):
            if st.session_state.running:
                st.session_state.remaining = max(
                    0,
                    int(st.session_state.end_time - time.monotonic() + 0.999)
                )
                st.session_state.running = False
                st.session_state.paused = True
                st.session_state.end_time = None
                st.session_state.status = "Timer paused"
            else:
                st.session_state.status = "Timer is not running"

            st.rerun(scope="fragment")

    with b3:
        if st.button("↻ RESET", key="reset_btn", use_container_width=True):
            st.session_state.remaining = 0
            st.session_state.end_time = None
            st.session_state.running = False
            st.session_state.paused = False
            st.session_state.finished = False
            st.session_state.status = "Set time and press START"
            st.rerun(scope="fragment")


timer_panel()
