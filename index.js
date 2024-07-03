// const express = require('express');
// const axios = require('axios');
// const path = require('path');
// const port = 3000;
// const app = express();

// // Serve static files from the 'public' directory
// app.use(express.static(path.join(__dirname, 'public')));
// app.use(express.json());

// // Define routes
// app.get('/system-metrics', async (req, res) => {
//     try {
//         const response = await axios.get('http://localhost:5001/metrics');
//         res.json(response.data);
//     } catch (error) {
//         console.error('Error fetching metrics:', error);
//         res.status(500).send('Error fetching metrics');
//     }
// });

// app.get('/chrome-history', async (req, res) => {
//     const { start_date, start_time, end_date, end_time } = req.query;
//     try {
//         const response = await axios.get('http://localhost:5001/metrics2', {
//             params: { start_date, start_time, end_date, end_time }
//         });
//         res.json(response.data);
//     } catch (error) {
//         console.error('Error fetching history:', error);
//         res.status(500).send('Error fetching history');
//     }
// });

// // New route for cleaning temporary files
// app.post('/clean-temp-files', async (req, res) => {
//     try {
//         const response = await axios.post('http://localhost:5001/clean-temp-files');
//         res.json(response.data);
//     } catch (error) {
//         console.error('Error cleaning temp files:', error);
//         res.status(500).send('Error cleaning temp files');
//     }
// });


// app.post('/execute-cmd', async (req, res) => {
//     const command = req.body.command;
//     try {
//         const response = await axios.post('http://localhost:5001/execute-cmd', { command });
//         res.json(response.data);
//     } catch (error) {
//         res.status(500).json({ error: `Error executing command: ${error.message}` });
//     }
// });

// app.get('/fetch', async (req, res) => {
//     const { url } = req.query;
//     try {
//         const response = await axios.get(`http://localhost:5001/scrape?url=${encodeURIComponent(url)}`);
//         res.json(response.data);
//     } catch (error) {
//         console.error('Error fetching data from Flask API:', error);
//         res.status(500).json({ error: `Error fetching data from Flask API: ${error.message}` });
//     }
// });


// app.get('/storage', async (req, res) => {
//     try {
//         const response = await axios.get('http://localhost:5001/storage');
//         const disk = response.data;
        
//         // Logging for debugging
//         console.log('Disk data:', disk);

//         res.json(disk);
//     } catch (error) {
//         console.error('Error fetching storage data:', error);
//         res.status(500).send(`Error fetching storage data: ${error.toString()}`);
//     }
// });

// app.get('/packets', (req, res) => {
//     const { protocol, dst_ip, dst_port } = req.query;
//     let filteredPackets = capturedPackets;

//     if (protocol) {
//         filteredPackets = filteredPackets.filter(pkt => pkt.protocol === protocol);
//     }

//     if (dst_ip) {
//         filteredPackets = filteredPackets.filter(pkt => pkt.dst_ip === dst_ip);
//     }

//     if (dst_port) {
//         filteredPackets = filteredPackets.filter(pkt => pkt.dst_port === parseInt(dst_port));
//     }

//     res.json(filteredPackets);
// });

// const fetchPackets = async () => {
//     try {
//         const response = await axios.get('http://localhost:5001/packets');
//         capturedPackets = response.data;
//     } catch (error) {
//         console.error('Error fetching packets:', error);
//     }
// };

// setInterval(fetchPackets, 1000);
// // Start the server
// app.listen(port, () => {
//     console.log(`Server is running on http://localhost:${port}`);
// });


const express = require('express');
const axios = require('axios');
const path = require('path');
const port = 3000;
const app = express();

let backendIp = 'localhost:5001';  // Default backend IP

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

// Endpoint to set the IP address
app.post('/set-ip', (req, res) => {
    const { ip } = req.body;
    if (ip) {
        backendIp = `${ip}:5001`;
        res.sendStatus(200);
    } else {
        res.sendStatus(400);
    }
});

// Define routes
app.get('/system-metrics', async (req, res) => {
    try {
        const response = await axios.get(`http://${backendIp}/metrics`);
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching metrics:', error);
        res.status(500).send('Error fetching metrics');
    }
});

app.get('/chrome-history', async (req, res) => {
    const { start_date, start_time, end_date, end_time } = req.query;
    try {
        const response = await axios.get(`http://${backendIp}/metrics2`, {
            params: { start_date, start_time, end_date, end_time }
        });
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching history:', error);
        res.status(500).send('Error fetching history');
    }
});

app.post('/clean-temp-files', async (req, res) => {
    try {
        const response = await axios.post(`http://${backendIp}/clean-temp-files`);
        res.json(response.data);
    } catch (error) {
        console.error('Error cleaning temp files:', error);
        res.status(500).send('Error cleaning temp files');
    }
});

app.post('/execute-cmd', async (req, res) => {
    const command = req.body.command;
    try {
        const response = await axios.post(`http://${backendIp}/execute-cmd`, { command });
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: `Error executing command: ${error.message}` });
    }
});

app.get('/fetch', async (req, res) => {
    const { url } = req.query;
    try {
        const response = await axios.get(`http://${backendIp}/scrape?url=${encodeURIComponent(url)}`);
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching data from Flask API:', error);
        res.status(500).json({ error: `Error fetching data from Flask API: ${error.message}` });
    }
});

app.get('/storage', async (req, res) => {
    try {
        const response = await axios.get(`http://${backendIp}/storage`);
        const disk = response.data;

        // Logging for debugging
        console.log('Disk data:', disk);

        res.json(disk);
    } catch (error) {
        console.error('Error fetching storage data:', error);
        res.status(500).send(`Error fetching storage data: ${error.toString()}`);
    }
});

app.get('/packets', (req, res) => {
    const { protocol, dst_ip, dst_port } = req.query;
    let filteredPackets = capturedPackets;

    if (protocol) {
        filteredPackets = filteredPackets.filter(pkt => pkt.protocol === protocol);
    }

    if (dst_ip) {
        filteredPackets = filteredPackets.filter(pkt => pkt.dst_ip === dst_ip);
    }

    if (dst_port) {
        filteredPackets = filteredPackets.filter(pkt => pkt.dst_port === parseInt(dst_port));
    }

    res.json(filteredPackets);
});

const fetchPackets = async () => {
    try {
        const response = await axios.get(`http://${backendIp}/packets`);
        capturedPackets = response.data;
    } catch (error) {
        console.error('Error fetching packets:', error);
    }
};

setInterval(fetchPackets, 1000);

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
