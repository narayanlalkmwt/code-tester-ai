answer.js
// answer.js

let editor = ace.edit("editor");
editor.setTheme("ace/theme/cobalt");

let typingSpeedElement = document.getElementById("typing-speed");
let timerElement = document.getElementById("timer");
let startTime = null;
let charCount = 0;
let wpm = 0;
let timer = null;
let lastTypingTime = 0;
let elapsedTime = 0;
let typingTimer = null;

// Function to get query parameters from the URL
function getQueryParams() {
    let params = {};
    let search = window.location.search.substring(1);
    if (search) {
        let pairs = search.split('&');
        for (let i = 0; i < pairs.length; i++) {
            let pair = pairs[i].split('=');
            params[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1]);
        }
    }
    return params;
}

// Get the query parameters
let params = getQueryParams();
let selectedLanguage = params.language;
let selectedLevel = params.level;
let selectedQuestions = params.questions;

// Set the editor mode based on the selectedLanguage parameter
if (selectedLanguage) {
    switch (selectedLanguage.toLowerCase()) {
        case 'python':
            editor.session.setMode("ace/mode/python");
            break;
        case 'cpp':
            editor.session.setMode("ace/mode/c_cpp");
            break;
        case 'java':
            editor.session.setMode("ace/mode/java");
            break;
        default:
            editor.session.setMode("ace/mode/text");
            break;
    }
}

// Function to reset the typing speed and timer
function resetTypingSpeedAndTimer() {
    startTime = null;
    charCount = 0;
    wpm = 0;
    elapsedTime = 0;
    typingSpeedElement.innerHTML = `Typing Speed:<br>0 WPM`;
    timerElement.innerHTML = `Time:<br>00:00`;
    clearInterval(timer);
    clearInterval(typingTimer);
}

// Function to update the typing speed based on the number of characters typed
function updateTypingSpeed() {
    if (!startTime) {
        startTime = new Date().getTime();
    }

    let currentTime = new Date().getTime();
    let timeElapsed = (currentTime - startTime) / 1000 / 60; // time elapsed in minutes
    let words = charCount / 5; // average word length
    wpm = Math.round(words / timeElapsed);

    typingSpeedElement.innerHTML = `Typing Speed:<br>${wpm} WPM`;
}

// Function to decrease the typing speed over time if the user stops typing
function decreaseTypingSpeed() {
    timer = setInterval(() => {
        if (wpm > 0) {
            wpm = Math.max(0, wpm - 10); // Decrease by 10 WPM instead of 20
            typingSpeedElement.innerHTML = `Typing Speed:<br>${wpm} WPM`;
        } else {
            clearInterval(timer);
        }
    }, 200); // Increase the interval to 200 ms instead of 100 ms
}

// Function to update the timer display
function updateTimer() {
    elapsedTime++;
    let minutes = Math.floor(elapsedTime / 60);
    let seconds = elapsedTime % 60;
    timerElement.innerHTML = `Time:<br>${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

// Event listener for typing in the editor
editor.on("input", function() {
    if (!startTime) {
        startTime = new Date().getTime();
        typingTimer = setInterval(updateTimer, 1000);
    }

    charCount = editor.getValue().length;
    lastTypingTime = new Date().getTime();

    // Update typing speed on each keystroke
    updateTypingSpeed();

    // Reset the decrease speed interval
    clearInterval(timer);
});

// Event listener for changes in the editor
editor.on("change", function() {
    if (editor.getValue().length === 0) {
        resetTypingSpeedAndTimer();
    }
});

// Interval to detect when typing stops and start decreasing speed
setInterval(() => {
    let currentTime = new Date().getTime();
    if (currentTime - lastTypingTime > 1000 && charCount > 0) { // 1 second of inactivity
        decreaseTypingSpeed();
    }
}, 1000);

// Function to set hidden form inputs before submitting
function setFormInputs() {
    document.getElementById('hidden-language').value = selectedLanguage;
    document.getElementById('hidden-level').value = selectedLevel;
    document.getElementById('hidden-questions').value = selectedQuestions;
}

// Set the hidden form inputs when the form is submitted
document.getElementById('next-form').addEventListener('submit', setFormInputs);