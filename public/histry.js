google.charts.load('current', { packages: ['corechart', 'bar', 'table'] });

google.charts.setOnLoadCallback(drawCharts);

function click12() {
  setTimeout(drawCharts, 1000);
}

function drawCharts() {
  drawSystemMetricsChart();
  drawChromeHistoryCharts();
}

function drawSystemMetricsChart() {
  fetch('/system-metrics')
    .then(response => response.json())
    .then(metrics => {
      const data = google.visualization.arrayToDataTable([
        ['Metric', 'Value'],
        ['CPU', metrics.CPU],
        ['Memory', metrics.Memory]
      ]);

      const options = {
        title: 'System Metrics',
        pieHole: 0.4
      };

      const chart = new google.visualization.PieChart(document.getElementById('donutchart'));
      chart.draw(data, options);
    })
    .catch(error => console.error('Error fetching system metrics:', error));
}

function drawChromeHistoryCharts() {
  const start_date = document.getElementById("start_date").value;
  const start_time = document.getElementById("start_time").value;
  const end_date = document.getElementById("end_date").value;
  const end_time = document.getElementById("end_time").value;

  fetch(`/chrome-history?start_date=${start_date}&start_time=${start_time}&end_date=${end_date}&end_time=${end_time}`)
    .then(response => response.json())
    .then(history => {
      const historyData = [['Site', 'Visit Count', 'URL']];
      history.forEach(entry => {
        historyData.push([entry.domain, entry.visit_count, entry.url]);
      });

      // Debugging: Log the historyData array
      console.log('History Data for Table:', historyData);

      drawBarChart(historyData);
      drawTable(historyData);
    })
    .catch(error => console.error('Error fetching Chrome history:', error));
}

function drawBarChart(historyData) {
  // Exclude the URL column for the bar chart
  const barData = historyData.map(item => [item[0], item[1]]);

  // Debugging: Log the barData array
  console.log('Data for Bar Chart:', barData);

  const data = google.visualization.arrayToDataTable(barData);

  const barOptions = {
    chart: {
      title: 'Chrome History',
      subtitle: 'Visit counts of different sites',
    },
    bars: 'horizontal' // Required for Material Bar Charts.
  };

  const barChart = new google.charts.Bar(document.getElementById('columnchart_material'));
  barChart.draw(data, google.charts.Bar.convertOptions(barOptions));
}

function drawTable(historyData) {
  const data = google.visualization.arrayToDataTable(historyData);

  const tableOptions = {
    showRowNumber: true,
    width: '100%',
    height: '100%'
  };

  const tableChart = new google.visualization.Table(document.getElementById('history_table'));
  tableChart.draw(data, tableOptions);
}
