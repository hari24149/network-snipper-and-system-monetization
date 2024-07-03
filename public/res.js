google.charts.load('current', { packages: ['gauge'] });

google.charts.setOnLoadCallback(drawChart2);

let chart;
let data;
const options = {
    width: 400,
    height: 120,
    redFrom: 90,
    redTo: 100,
    yellowFrom: 75,
    yellowTo: 90,
    minorTicks: 5
};

const MAX_NETWORK_VALUE = 10000000; // Adjust this value based on realistic maximum

function drawChart2() {
    data = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Memory', 0],
        ['CPU', 0],
        ['Network', 0]
    ]);

    chart = new google.visualization.Gauge(document.getElementById('chart_div'));
    chart.draw(data, options);

    fetchMetrics(); // Fetch initial metrics
    setInterval(fetchMetrics, 1000); // Fetch metrics every 5 seconds

    function fetchMetrics() {
        fetch('/system-metrics')
            .then(response => response.json())
            .then(metrics => {
                data.setValue(0, 1, metrics.Memory);
                data.setValue(1, 1, metrics.CPU);
                data.setValue(2, 1, metrics.Network);
                chart.draw(data, options);
            })
            .catch(error => console.error('Error fetching metrics:', error));
    }
}



document.getElementById('clean-button').addEventListener('click', () => {
    fetch('/clean-temp-files', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.getElementById('result');
        if (data.deleted.length > 0) {
            resultDiv.innerHTML = `Deleted files: ${data.deleted.length}`;
        } else {
            resultDiv.innerHTML = `No files were deleted.`;
        }
        if (data.skipped.length > 0) {
            resultDiv.innerHTML += `<br>Skipped files: ${data.skipped.length}`;
        }
    })
    .catch(error => {
        document.getElementById('result').innerHTML = 'Error cleaning temp files.';
        console.error('Error:', error);
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const commandInput = document.getElementById('commandInput');
    const output = document.getElementById('output');
    
    commandInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            const command = commandInput.value.trim();
            output.textContent += `${command}\n`;
            commandInput.value = '';
            sendCommand(command);
        }
    });
    
    function sendCommand(command) {
        fetch('/execute-cmd', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ command })
        })
        .then(response => response.json())
        .then(data => {
            if (data.output) {
                output.textContent += data.output;
            } else {
                output.textContent += data.error;
            }
            output.textContent += '\n$ ';
        })
        .catch(error => {
            output.textContent += `Error: ${error.message}\n$ `;
        });
    }
});
async function fetchStorageInfo() {
    try {
        const response = await fetch('/storage');
        const data = await response.json();
        console.log(data); // Log data for debugging
        
        document.getElementById('total').innerText = data.total;
        document.getElementById('used').innerText = data.used;
        document.getElementById('free').innerText = data.free;
        document.getElementById('percent').innerText = data.percent;
    } catch (error) {
        console.error('Error fetching storage info:', error);
    }
}

fetchStorageInfo();

