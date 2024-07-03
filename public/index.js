function click12() {
    const fileUrl = "asearts/app/app.py";  // Relative URL to the file in the same directory
    const element = document.createElement('a');
    element.setAttribute('href', fileUrl);
    element.setAttribute('download', 'app.py');

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);


    setTimeout(function() {
        window.location.href = "home.html";
    }, 2000);
}
