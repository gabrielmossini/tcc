document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("detectionChart").getContext("2d");
    const detectionData = {
        labels: [
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
            "Colete Refletivo",
        ],
        datasets: [
            {
                label: "Sem EPI",
                data: Array(11).fill(0),
                backgroundColor: "rgba(255, 0, 0, 0.2)",
                borderColor: "rgba(255, 0, 0, 1)",
                borderWidth: 1,
            },
            {
                label: "EPI",
                data: Array(11).fill(0),
                backgroundColor: "rgba(0, 255, 0, 0.2)",
                borderColor: "rgba(0, 255, 0, 1)",
                borderWidth: 1,
            },
        ],
    };

    const detectionChart = new Chart(ctx, {
        type: "bar",
        data: detectionData,
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });

    let sortOrder = 'desc';
    let pollingInterval;

    function updateChartData(detectionCount) {
        detectionData.labels.forEach((label, index) => {
            if (label.startsWith("Sem ")) {
                detectionData.datasets[0].data[index] = detectionCount[label] || 0;
            } else {
                detectionData.datasets[1].data[index] = detectionCount[label] || 0;
            }
        });
        detectionChart.update();
    }

    function updateDetectionTable(detectionCount) {
        const tableBody = document.getElementById('detection-table-body');
        tableBody.innerHTML = '';

        detectionData.labels.forEach((label) => {
            const count = detectionCount[label] || 0;
            const row = `<tr>
                          <td>${label}</td>
                          <td>${count}</td>
                        </tr>`;
            tableBody.innerHTML += row;
        });
    }

    function sortTable() {
        const tableBody = document.getElementById('detection-table-body');
        const rows = Array.from(tableBody.querySelectorAll('tr'));

        rows.sort((a, b) => {
            const aValue = parseInt(a.querySelector('td:nth-child(2)').innerText, 10);
            const bValue = parseInt(b.querySelector('td:nth-child(2)').innerText, 10);
            return sortOrder === 'desc' ? aValue - bValue : bValue - aValue;
        });

        tableBody.innerHTML = '';
        rows.forEach(row => tableBody.appendChild(row));
    }

        document.getElementById('sort-detections').addEventListener('click', function() {
            sortTable();
            sortOrder = sortOrder === 'desc' ? 'asc' : 'desc';
        });

    function fetchDetections() {
        fetch("/get_detections/")
            .then((response) => response.json())
            .then((data) => {
                console.log("Received data:", data);
                updateAll(data.detectionCount, data.detections);
            })
            .catch((error) => console.error("Error fetching detections:", error));
    }


    function updateAll(detectionCount, detectedObjects) {
        updateChartData(detectionCount);
        updateDetectionTable(detectionCount);
    }

    function startPolling() {
        pollingInterval = setInterval(fetchDetections, 5000);
    }

    function stopPolling() {
        clearInterval(pollingInterval);
    }

    startPolling();
});