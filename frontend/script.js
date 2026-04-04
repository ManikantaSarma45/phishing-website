async function checkURL() {
    const url = document.getElementById("urlInput").value;

    if (!url) {
        alert("Enter URL");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        document.getElementById("result").innerText =
            "Prediction: " + data.prediction;

    } catch (error) {
        console.error(error);
        document.getElementById("result").innerText =
            "Error connecting to backend";
    }
}