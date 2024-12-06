window.onload = function() {
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

    let params = getQueryParams();
    let selectedLanguage = params.language;
    let selectedLevel = params.level;
    let selectedQuestions = params.questions;

    if (selectedLanguage) {
        switch (selectedLanguage.toLowerCase()) {
            case 'python':
                editor.session.setMode("ace/mode/python");
                break;
            case 'c':
            case 'cpp':
                editor.session.setMode("ace/mode/c_cpp");
                break;
            case 'java':
                editor.session.setMode("ace/mode/java");
                break;
            case 'php':
                editor.session.setMode("ace/mode/php");
                break;
            case 'javascript':
            case 'nodejs':
                editor.session.setMode("ace/mode/javascript");
                break;
            default:
                editor.session.setMode("ace/mode/text");
                break;
        }
    }

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

    function updateTypingSpeed() {
        if (!startTime) {
            startTime = new Date().getTime();
        }

        let currentTime = new Date().getTime();
        let timeElapsed = (currentTime - startTime) / 1000 / 60;
        let words = charCount / 5;
        wpm = Math.round(words / timeElapsed);

        typingSpeedElement.innerHTML = `Typing Speed:<br>${wpm} WPM`;
    }

    function decreaseTypingSpeed() {
        timer = setInterval(() => {
            if (wpm > 0) {
                wpm = Math.max(0, wpm - 10);
                typingSpeedElement.innerHTML = `Typing Speed:<br>${wpm} WPM`;
            } else {
                clearInterval(timer);
            }
        }, 200);
    }

    function updateTimer() {
        elapsedTime++;
        let minutes = Math.floor(elapsedTime / 60);
        let seconds = elapsedTime % 60;
        timerElement.innerHTML = `Time:<br>${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }

    editor.on("input", function() {
        if (!startTime) {
            startTime = new Date().getTime();
            typingTimer = setInterval(updateTimer, 1000);
        }

        charCount = editor.getValue().length;
        lastTypingTime = new Date().getTime();

        updateTypingSpeed();

        clearInterval(timer);
    });

    editor.on("change", function() {
        if (editor.getValue().length === 0) {
            resetTypingSpeedAndTimer();
        }
    });

    setInterval(() => {
        let currentTime = new Date().getTime();
        if (currentTime - lastTypingTime > 1000 && charCount > 0) {
            decreaseTypingSpeed();
        }
    }, 1000);

    function setFormInputs() {
        document.getElementById('hidden-language').value = selectedLanguage;
        document.getElementById('hidden-level').value = selectedLevel;
        document.getElementById('hidden-questions').value = selectedQuestions;
    }

    // Set the hidden inputs when the page loads
    setFormInputs();

    // Save editor content to hidden textarea on form submission
    document.querySelector('form').onsubmit = function() {
        document.getElementById('hidden-answer').value = editor.getValue();
    };
};
