async function fetchData() {
    const url = document.getElementById('url').value;
    try {
        const response = await fetch(`/fetch?url=${encodeURIComponent(url)}`);
        const data = await response.json();

        document.getElementById('title').textContent = `Title: ${data.title || 'N/A'}`;
        document.getElementById('description').textContent = `Description: ${data.description || 'N/A'}`;
        document.getElementById('headings').textContent = `Headings: ${data.headings.join(', ') || 'N/A'}`;

        const linksContainer = document.getElementById('links');
        linksContainer.innerHTML = 'Links: ';
        data.links.forEach(link => {
            const a = document.createElement('a');
            a.href = link.href;
            a.textContent = link.text || link.href;
            a.target = '_blank';
            linksContainer.appendChild(a);
            linksContainer.appendChild(document.createTextNode(' | '));
        });

        const imagesContainer = document.getElementById('images');
        imagesContainer.innerHTML = 'Images: ';
        data.images.forEach(src => {
            const img = document.createElement('img');
            img.src = src;
            img.alt = 'Image';
            img.style.width = '100px';
            img.style.margin = '5px';
            imagesContainer.appendChild(img);
        });

        document.getElementById('scrapedData').textContent = data.html || data.error;
    } catch (error) {
        document.getElementById('scrapedData').textContent = 'Error fetching data';
    }
}
