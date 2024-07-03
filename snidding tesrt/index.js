

const express = require('express');
const axios = require('axios');
const path = require('path');
const port = 3000;
const app = express();

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Define routes
app.get('/system-metrics', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5001/metrics');
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching metrics:', error);
        res.status(500).send('Error fetching metrics');
    }
});

app.get('/chrome-history', async (req, res) => {
    const { start_date, start_time, end_date, end_time } = req.query;
    try {
        const response = await axios.get('http://localhost:5001/metrics2', {
            params: { start_date, start_time, end_date, end_time }
        });
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching history:', error);
        res.status(500).send('Error fetching history');
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
