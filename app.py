```python
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Countdown Clock & Timer",
    page_icon="⏱️",
    layout="centered"
)

html_code = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    background: #101827;
    color: white;
    font-family: Arial, sans-serif;
}

.timer-app {
    width: 100%;
    max-width: 460px;
    min-height: 610px;
    margin: 0 auto;
    padding: 45px 12px 25px;
    text-align: center;
    background: #101827;
}

h1 {
    margin: 0 0 22px;
    color: #60A5FA;
    font-size: 34px;
    font-weight: bold;
    white-space: nowrap;
}

.subtitle {
    font-size: 23px;
    margin-bottom: 35px;
}

.inputs {
    display: flex;
    justify-content: center;
    gap: 14px;
}

.time-field {
    width: 31%;
    min-width: 0;
}

.time-field label {
    display: block;
    color: #CBD5E1;
    font-size: 15px;
    margin-bottom: 12px;
}

.time-field input {
    width: 100%;
    height: 48px;
    border: 1px solid #d1d5db;
    border-radius: 7px;
    background: #ffffff;
    color: #111827;
    text-align: center;
    font-size: 27px;
    font-weight: bold;
    outline: none;
    padding: 4px;

    /* Hide number input arrows */
    -moz-appearance: textfield;
    appearance: textfield;
}

/* Hide arrows in Chrome, Edge and Safari */
.time-field input::-webkit-inner-spin-button,
.time-field input::-webkit-outer-spin-button {
    -webkit-appearance: none;
    appearance: none;
    margin: 0;
}

.buttons {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 21px;
}

button {
    flex: 1;
    height: 53px;
    border: 1px solid #64748b;
    color: white;
    font-size: 15px;
    cursor: pointer;
}

button:active {
    opacity: 0.8;
}

.start {
    background: #16A34A;
}

.pause {
    background: #D97706;
}

.reset {
    background: #DC2626;
}

.display {
    margin-top: 78px;
    color: #34D399;
    font-family: Consolas, monospace;
    font-size: 58px;
    font-weight: bold;
    letter-spacing: -2px;
    white-space: nowrap;
    line-height: 1.2;
}

.status {
    margin-top: 37px;
    font-size: 21px;
    color: white;
}

@media (max-width: 380px) {
    .timer-app {
        padding-top: 35px;
    }

    h1 {
        font-size: 27px;
    }

    .subtitle {
        font-size: 20px;
    }

    .inputs {
        gap: 8px;
    }

    .display {
        font-size: 45px;
        margin-top: 65px;
    }

    .buttons {
        gap: 7px;
    }

    button {
        font-size: 12px;
    }
}
</style>
</head>

<body>
<div class="timer-app">

    <h1>COUNTDOWN TIMER</h1>

    <div class="subtitle">Set your time</div>

    <div class="inputs">
        <div class="time-field">
            <label for="hours">Hours</label>
            <input id="hours" type="number"
                   min="0" max="999" value="00">
        </div>

        <div class="time-field">
            <label for="minutes">Minutes</label>
            <input id="minutes" type="number"
                   min="0" max="59" value="00">
        </div>

        <div class="time-field">
            <label for="seconds">Seconds</label>
            <input id="seconds" type="number"
                   min="0" max="59" value="00">
        </div>
    </div>

    <div class="display" id="display">00:00:00</div>

    <div class="status" id="status">Ready to start</div>

    <div class="buttons">
        <button class="start" id="start">START</button>
        <button class="pause" id="pause">PAUSE</button>
        <button class="reset" id="reset">RESET</button>
    </div>

</div>

<script>
let remaining = 0;
let running = false;
let paused = false;
let endTime = 0;
let interval = null;

let audioContext = null;
let alarmOscillator = null;

const display = document.getElementById("display");
const statusText = document.getElementById("status");
const hours = document.getElementById("hours");
const minutes = document.getElementById("minutes");
const seconds = document.getElementById("seconds");

function showTime(total) {
    const h = Math.floor(total / 3600);
    const m = Math.floor((total % 3600) / 60);
    const s = total % 60;

    display.textContent =
        String(h).padStart(2, "0") + ":" +
        String(m).padStart(2, "0") + ":" +
        String(s).padStart(2, "0");
}

function playAlarm() {
    try {
        audioContext = audioContext ||
            new (window.AudioContext ||
                 window.webkitAudioContext)();

        audioContext.resume();

        alarmOscillator = audioContext.createOscillator();
        const gain = audioContext.createGain();

        alarmOscillator.connect(gain);
        gain.connect(audioContext.destination);

        alarmOscillator.type = "sine";
        alarmOscillator.frequency.value = 880;
        gain.gain.value = 0.15;

        alarmOscillator.start();
        alarmOscillator.stop(
            audioContext.currentTime + 0.8
        );
    } catch (error) {
        console.log("Audio unavailable", error);
    }
}

function tick() {
    if (!running) return;

    remaining = Math.max(
        0,
        Math.ceil((endTime - Date.now()) / 1000)
    );

    showTime(remaining);

    if (remaining <= 0) {
        clearInterval(interval);
        interval = null;
        running = false;
        paused = false;

        display.style.color = "#F87171";
        statusText.textContent =
            "Time's up! Alarm ringing!";
        statusText.style.color = "#F87171";

        playAlarm();
    }
}

document.getElementById("start").addEventListener(
    "click", function () {
        if (running) return;

        if (!paused) {
            const h = Number(hours.value);
            const m = Number(minutes.value);
            const s = Number(seconds.value);

            if (
                hours.value.trim() === "" ||
                minutes.value.trim() === "" ||
                seconds.value.trim() === "" ||
                !Number.isInteger(h) ||
                !Number.isInteger(m) ||
                !Number.isInteger(s) ||
                h < 0 || h > 999 ||
                m < 0 || m > 59 ||
                s < 0 || s > 59
            ) {
                statusText.textContent =
                    "Enter valid time (minutes/seconds 0-59).";
                statusText.style.color = "#F87171";
                return;
            }

            remaining = h * 3600 + m * 60 + s;

            if (remaining <= 0) {
                statusText.textContent =
                    "Please enter a time greater than zero.";
                statusText.style.color = "#F87171";
                return;
            }
        }

        if (audioContext &&
            audioContext.state === "suspended") {
            audioContext.resume();
        }

        display.style.color = "#34D399";
        statusText.style.color = "#34D399";
        statusText.textContent = "Timer is running...";

        running = true;
        paused = false;
        endTime = Date.now() + remaining * 1000;

        tick();

        if (running) {
            interval = setInterval(tick, 100);
        }
    }
);

document.getElementById("pause").addEventListener(
    "click", function () {
        if (!running) return;

        remaining = Math.max(
            0,
            Math.ceil((endTime - Date.now()) / 1000)
        );

        running = false;
        paused = true;

        clearInterval(interval);
        interval = null;

        showTime(remaining);

        statusText.textContent = "Timer paused";
        statusText.style.color = "#FBBF24";
    }
);

document.getElementById("reset").addEventListener(
    "click", function () {
        running = false;
        paused = false;

        clearInterval(interval);
        interval = null;

        remaining = 0;

        hours.value = "00";
        minutes.value = "00";
        seconds.value = "00";

        showTime(0);

        display.style.color = "#34D399";
        statusText.style.color = "white";
        statusText.textContent = "Ready to start";
    }
);
</script>
</body>
</html>
"""

components.html(
    html_code,
    height=650,
    scrolling=False
)
```
