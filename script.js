async function askAI() {

    let question = document.getElementById("question").value;
    let crop = document.getElementById("crop").value;

    let imageInput = document.getElementById("image");

    // Fake image detection
    if (imageInput.files.length > 0) {
        document.getElementById("answer").innerText =
        "Detected: Leaf Spot Disease\nSolution: Spray Mancozeb.";
        return;
    }

    document.getElementById("answer").innerText = "Loading...";

    let response = await fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question: question,
            crop: crop,
            location: "Tamil Nadu"
        })
    });

    let data = await response.json();

    document.getElementById("answer").innerText = data.answer;
}


function startVoice() {
    let recognition = new webkitSpeechRecognition();
    recognition.lang = "ml-IN";

    recognition.onresult = function(event) {
        document.getElementById("question").value =
        event.results[0][0].transcript;
    };

    recognition.start();
}


function escalate() {
    alert("Query sent to Agriculture Officer!");
}