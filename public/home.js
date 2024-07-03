function chrhis() {
    window.location.href = "histry.html";
}
function res(){
    window.location.href = "resource.html";
}
function sniff(){
    window.location.href = "sniff.html";
}
function scrape(){
    window.location.href = "webscrape.html";
}
document.addEventListener('DOMContentLoaded', function() {
    let ip = localStorage.getItem('backendIp');
    if (!ip) {
        ip = prompt('Enter the IP address:');
        if (ip) {
            localStorage.setItem('backendIp', ip);
            setBackendIp(ip);
            alert('IP address set successfully!');
        }
    } else {
        setBackendIp(ip);
    }

    document.getElementById('change-ip-btn').addEventListener('click', function() {
        const newIp = prompt('Enter the new IP address:');
        if (newIp) {
            localStorage.setItem('backendIp', newIp);
            setBackendIp(newIp);
        }
    });
});

function setBackendIp(ip) {
    fetch('/set-ip', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ip })
    }).then(response => {
        if (response.ok) {
            document.getElementById('connected-ip').textContent = ip;
        } else {
            alert('Failed to set IP address');
        }
    });
}