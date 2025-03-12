document.addEventListener("DOMContentLoaded", function () {
    const videos = [
        "https://youtube.com/embed/GCHr4nGW_Oc?si=P1ru01g_-p1vJDLL",
        "https://youtube.com/embed/ouAGhpVyLvI?si=6MYdPp4RGfEZenF2",
        "https://youtube.com/embed/yR2XeZPAgZg?si=lZifXTn0vW5ZpSAS",

        
        
    ];

    const container = document.getElementById("video-container");

    if (container) {
        videos.forEach(url => {
            let iframe = document.createElement("iframe");
            iframe.width = "560";
            iframe.height = "315";
            iframe.src = url;
            iframe.frameBorder = "0";
            iframe.allowFullscreen = true;
            container.appendChild(iframe);
        });
    } else {
        console.error("No se encontró el contenedor de videos.");
    }
});
