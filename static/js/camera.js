document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("start-camera").addEventListener("click", startCamera);
    document.getElementById("stop-camera").addEventListener("click", stopCamera);

    function startCamera() {
        document.getElementById("video-container").style.display = "block";
        document.getElementById("start-camera").style.display = "none";
        document.getElementById("stop-camera").style.display = "block";
        document.getElementById("video").src = "/video_feed/";
        startPolling();
    }

    function stopCamera() {
        document.getElementById("video-container").style.display = "none";
        document.getElementById("start-camera").style.display = "block";
        document.getElementById("stop-camera").style.display = "none";
        document.getElementById("video").src = "";
        stopPolling();
    }

    let pollingInterval;

    function startPolling() {
        pollingInterval = setInterval(fetchDetections, 1000);
    }

    function stopPolling() {
        clearInterval(pollingInterval);
    }

    function fetchDetections() {
        fetch("/get_detections/")
            .then((response) => response.json())
            .then((data) => {
                console.log("Received data:", data);
                handleDetectionAlert(data.detections);
                updateDetectionTable(data.detectionCount);
            })
            .catch((error) => console.error("Error fetching detections:", error));
    }

    function handleDetectionAlert(detectedObjects) {
        const alertsDiv = document.getElementById("alerts");
        alertsDiv.innerHTML = "";
        detectedObjects.forEach((obj) => {
            if (obj.startsWith("Sem ")) {
                const alertElement = document.createElement("div");
                alertElement.innerText = `${obj} Detectado!`;
                alertElement.style.color = "red";
                alertsDiv.appendChild(alertElement);
            }
            updateChartData(obj); // Update the chart for each detected object
        });
    }

    function updateDetectionTable(detectionCount) {
        const tableBody = document.getElementById('detection-table-body');
        tableBody.innerHTML = '';  // Clear previous data

        const labels = [
            "Protecao de Ouvido",
            "Capacete",
            "Mascara",
            "Sem Luva",
            "Sem Capacete",
            "Sem Botina",
            "Sem Colete Refletivo",
            "Botina",
            "Oculos de Protecao",
            "Luvas de Protecao",
            "Colete Refletivo"
        ];

        labels.forEach((label) => {
            const count = detectionCount[label] || 0;  // Default to 0 if not found
            const row = `<tr>
                            <td>${label}</td>
                            <td>${count}</td>
                        </tr>`;
            tableBody.innerHTML += row;
        });
    }

    function toggleMute(isMuted) {
        document.getElementById('status').innerText = isMuted ? 'Alerta Desativado' : 'Alerta Ativado';
        document.getElementById('mute-button').style.display = isMuted ? 'none' : 'inline';
        document.getElementById('unmute-button').style.display = isMuted ? 'inline' : 'none';
        document.getElementById('mute-button').classList.toggle('muted', isMuted);
        document.getElementById('unmute-button').classList.toggle('muted', !isMuted);
    }

    function handleMuteToggle() {
        fetch('/toggle-mute/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            toggleMute(data.muted);
        });
    }

    document.getElementById('mute-button').addEventListener('click', handleMuteToggle);
    document.getElementById('unmute-button').addEventListener('click', handleMuteToggle);

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});