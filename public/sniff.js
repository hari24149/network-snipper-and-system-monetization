async function fetchPackets() {
    const protocol = document.getElementById('protocol').value;
    const dst_ip = document.getElementById('dst_ip').value;
    const dst_port = document.getElementById('dst_port').value;

    let url = '/packets?';
    if (protocol) url += `protocol=${protocol}&`;
    if (dst_ip) url += `dst_ip=${dst_ip}&`;
    if (dst_port) url += `dst_port=${dst_port}&`;

    const response = await fetch(url);
    const packets = await response.json();
    const tableBody = document.getElementById('packets-table').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';

    packets.forEach(packet => {
        const row = tableBody.insertRow();
        row.insertCell(0).innerText = packet.src_site;
        row.insertCell(1).innerText = packet.src_ip;
        row.insertCell(2).innerText = packet.src_port;
        row.insertCell(3).innerText = packet.dst_site;
        row.insertCell(4).innerText = packet.dst_ip;
        row.insertCell(5).innerText = packet.dst_port;
        row.insertCell(6).innerText = packet.protocol;
    });
}

function filterPackets() {
    fetchPackets();
}

setInterval(fetchPackets, 100);