//Guardar el elemento y el contexto 

/*
const mainCanvas = document.getElementById("main-canvas")
const context = mainCanvas.getContext("2d")

let initialX;
let initialY;

const dibujar = (cursorX, cursorY) => {
    context.beginPath();
    context.moveTo(initialX,initialY);
    context.lineWidth = 30;
    context.strokeStyle = "#000";
    context.lineCap = "round";
    context.lineJoin = "round";
    context.lineTo(cursorX, cursorY);
    context.stroke();

    initialX = cursorX;
    initialY = cursorY;
};

const mouseDown = (evt) => {

    initialX = evt.offsetX;
    initialY = evt.offsetY;
    dibujar(initialX,initialY);
    mainCanvas.addEventListener("mousemove",mouseMoving)
};

const mouseMoving = (evt) => {
    dibujar(evt.offsetX,evt.offsetY);
}

const mouseUp = () => {
    mainCanvas.removeEventListener("mousemove", mouseMoving);
}

mainCanvas.addEventListener("mousedown", mouseDown);
mainCanvas.addEventListener("mouseup", mouseUp)
*/


// Obtener elementos del DOM
const canvas = document.getElementById("main-canvas");
const context = canvas.getContext("2d");
const colorPicker = document.getElementById("color-picker");
const brushSize = document.getElementById("brush-size");
const eraserSize = document.getElementById("eraser-size");
const eraserButton = document.getElementById("eraser");
const clearCanvasButton = document.getElementById("clear-canvas");
const saveDrawingButton = document.getElementById("save-drawing");
const uploadImageButton = document.getElementById("upload-image");

let isDrawing = false;
let initialX, initialY;
let currentColor = "#000000";
let currentLineWidth = 5;
let currentEraserSize = 20;
let isEraser = false;

// Función para comenzar a dibujar
const startDrawing = (e) => {
    isDrawing = true;
    initialX = e.offsetX;
    initialY = e.offsetY;
};

// Función para detener el dibujo
const stopDrawing = () => {
    isDrawing = false;
    context.beginPath();
};

// Función para dibujar o borrar en el canvas
const draw = (e) => {
    if (!isDrawing) return;

    context.lineWidth = isEraser ? currentEraserSize : currentLineWidth;
    context.lineCap = "round";
    context.strokeStyle = isEraser ? "#fff" : currentColor;

    context.beginPath();
    context.moveTo(initialX, initialY);
    context.lineTo(e.offsetX, e.offsetY);
    context.stroke();

    initialX = e.offsetX;
    initialY = e.offsetY;
};

// Cargar imagen como referencia
const uploadImage = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const img = new Image();
    img.src = URL.createObjectURL(file);

    img.onload = () => {
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.drawImage(img, 0, 0, canvas.width, canvas.height);
    };
};

// Eventos del canvas
canvas.addEventListener("mousedown", startDrawing);
canvas.addEventListener("mousemove", draw);
canvas.addEventListener("mouseup", stopDrawing);
canvas.addEventListener("mouseleave", stopDrawing);

// Cambiar color
colorPicker.addEventListener("input", (e) => {
    currentColor = e.target.value;
    isEraser = false;
});

// Cambiar tamaño del pincel
brushSize.addEventListener("input", (e) => {
    currentLineWidth = e.target.value;
});

// Cambiar tamaño del borrador
eraserSize.addEventListener("input", (e) => {
    currentEraserSize = e.target.value;
});

// Activar borrador
eraserButton.addEventListener("click", () => {
    isEraser = true;
});

// Limpiar el lienzo
clearCanvasButton.addEventListener("click", () => {
    context.clearRect(0, 0, canvas.width, canvas.height);
});

// Guardar el dibujo
saveDrawingButton.addEventListener("click", () => {
    const link = document.createElement("a");
    link.download = "dibujo.png";
    link.href = canvas.toDataURL();
    link.click();
});

// Cargar imagen
uploadImageButton.addEventListener("change", uploadImage);