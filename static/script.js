const ws = new WebSocket('ws://localhost:8766');

// Main chart for candlesticks
let chart = LightweightCharts.createChart(document.getElementById('chart'), {
    width: 800,
    height: 500,
    layout: {
        backgroundColor: '#FFFFFF',
        textColor: '#000000',
    },
    grid: {
        vertLines: { color: '#E3E3E3' },
        horzLines: { color: '#E3E3E3' },
    },
});

// Create candlestick series
let candlestickSeries = chart.addCandlestickSeries();

// Moving Average series on the main chart
let ma200Series = chart.addLineSeries({ color: 'red', lineWidth: 2 });
let ma50Series = chart.addLineSeries({ color: 'orange', lineWidth: 2 });
let ma40Series = chart.addLineSeries({ color: 'green', lineWidth: 2 });

// Separate RSI chart positioned below the main chart
let rsiChart = LightweightCharts.createChart(document.getElementById('rsi-chart'), {
    width: 800,
    height: 150,  // Smaller height for RSI chart
    layout: {
        backgroundColor: '#FFFFFF',
        textColor: '#000000',
    },
    grid: {
        vertLines: { color: '#E3E3E3' },
        horzLines: { color: '#E3E3E3' },
    },
    timeScale: { visible: true },
    priceScale: { position: 'right' },
});

// RSI series on the RSI chart
let rsiSeries = rsiChart.addAreaSeries({
    topColor: '#2962FF',
    bottomColor: 'rgba(41, 98, 255, 0.28)',
    lineColor: '#2962FF',
    lineWidth: 2,
    priceFormat: {
        type: 'custom',
        formatter: (price) => price.toFixed(2),
    },
});

// Function to sync time scales between charts
function syncTimeScales(mainChart, subChart) {
    mainChart.timeScale().subscribeVisibleLogicalRangeChange((range) => {
        subChart.timeScale().setVisibleLogicalRange(range);
    });

    subChart.timeScale().subscribeVisibleLogicalRangeChange((range) => {
        mainChart.timeScale().setVisibleLogicalRange(range);
    });
}

// Synchronize main chart and RSI chart time scales
syncTimeScales(chart, rsiChart);

// WebSocket event handlers
ws.onopen = function() {
    console.log("WebSocket connection opened.");
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received data:', data);

    // Update table with latest data
    document.getElementById('data-table').innerHTML = `
        <tr>
            <td>${data.Date}</td>
            <td>${data.Open}</td>
            <td>${data.High}</td>
            <td>${data.Low}</td>
            <td>${data.Close}</td>
            <td>${data.Volume}</td>
            <td>${data.RSI ? data.RSI.toFixed(2) : 'N/A'}</td>
            <td>${data.SMA_40 ? data.SMA_40.toFixed(2) : 'N/A'}</td>
            <td>${data.SMA_50 ? data.SMA_50.toFixed(2) : 'N/A'}</td>
            <td>${data.SMA_200 ? data.SMA_200.toFixed(2) : 'N/A'}</td>
        </tr>
    `;

    // Convert Date to timestamp for Lightweight Charts
    let time = new Date(data.Date).getTime() / 1000;

    // Update candlestick chart
    candlestickSeries.update({
        time: time,
        open: data.Open,
        high: data.High,
        low: data.Low,
        close: data.Close,
    });

    // Update SMA lines incrementally
    if (data.SMA_40) ma40Series.update({ time: time, value: data.SMA_40 });
    if (data.SMA_50) ma50Series.update({ time: time, value: data.SMA_50 });
    if (data.SMA_200) ma200Series.update({ time: time, value: data.SMA_200 });

    // Update RSI chart
    if (data.RSI) {
        rsiSeries.update({
            time: time,
            value: data.RSI,
        });
    }
};

ws.onclose = function() {
    console.log("WebSocket connection closed.");
};

ws.onerror = function(error) {
    console.log("WebSocket error:", error);
};

