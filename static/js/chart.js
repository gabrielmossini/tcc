document.addEventListener("DOMContentLoaded", function () {
    // Chart setup
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

    let sortOrder = 'desc'; // 'asc' for ascending, 'desc' for descending
    let pollingInterval;

    // Update chart data
    function updateChartData(detectionCount) {
        detectionData.labels.forEach((label, index) => {
            if (label.startsWith("Sem ")) {
                detectionData.datasets[0].data[index] = detectionCount[label] || 0;
            } else {
                detectionData.datasets[1].data[index] = detectionCount[label] || 0;
            }
        });
        detectionChart.update(); // Ensure the chart is updated
    }

    // Update detection table
    function updateDetectionTable(detectionCount) {
        const tableBody = document.getElementById('detection-table-body');
        tableBody.innerHTML = ''; // Clear previous data

        detectionData.labels.forEach((label) => {
            const count = detectionCount[label] || 0; // Default to 0 if not found
            const row = `<tr>
                          <td>${label}</td>
                          <td>${count}</td>
                        </tr>`;
            tableBody.innerHTML += row;
        });
    }

    // Sort table rows
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

    // Event listener for sorting table
        document.getElementById('sort-detections').addEventListener('click', function() {
            sortTable(); // Sort the table based on current order
            sortOrder = sortOrder === 'desc' ? 'asc' : 'desc'; // Toggle the sort order
        });

    // Fetch detections from the server
    function fetchDetections() {
        fetch("/get_detections/")
            .then((response) => response.json())
            .then((data) => {
                console.log("Received data:", data);
                updateAll(data.detectionCount, data.detections);
            })
            .catch((error) => console.error("Error fetching detections:", error));
    }


    // Update all data (chart, table, and alerts)
    function updateAll(detectionCount, detectedObjects) {
        updateChartData(detectionCount);
        updateDetectionTable(detectionCount);
        handleDetectionAlert(detectedObjects);
    }

    // Start polling
    function startPolling() {
        pollingInterval = setInterval(fetchDetections, 5000); // Adjust interval if needed
    }

    // Stop polling
    function stopPolling() {
        clearInterval(pollingInterval);
    }

    // Start polling immediately
    startPolling();
});