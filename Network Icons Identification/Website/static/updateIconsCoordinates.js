// Get the position and size of the screenshot element
const imagePositionInfo = document
    .getElementById("screenshot")
    .getBoundingClientRect();

// Get all canvas elements
let canvases = document.getElementsByTagName("canvas");

// Set the size and position of each canvas to match the screenshot
for (let i = 0; i < canvases.length; i++) {
    canvases[i].height = imagePositionInfo.height;
    canvases[i].width = imagePositionInfo.width;
    canvases[i].top = imagePositionInfo.top;
    canvases[i].left = imagePositionInfo.left;
}

// Initialize state and coordinate arrays
var state = "network";
var network_coordinates = [];
var service_coordinates = [];
var call_coordinates = [];

// Function to handle menu button clicks
function menu_button_clicked(event) {
    const button = event.target;
    const buttons = document.getElementsByTagName("button");
    // Reset font weight for all menu buttons
    for (let i = 0; i < buttons.length; i++) {
        if (buttons[i].id.includes("menu")) {
            buttons[i].style.fontWeight = 400;
        }
    }
    // Set font weight for the clicked button
    button.style.fontWeight = 1000;
    state = button.id.split("-")[0];
    console.log(state);

    // Reset zIndex for all canvases
    document.getElementById("network-canvas").style.zIndex = 1;
    document.getElementById("service-canvas").style.zIndex = 1;
    document.getElementById("call-canvas").style.zIndex = 1;

    // Set zIndex for the selected canvas
    document.getElementById(state + "-canvas").style.zIndex = 10;
}

// Define colors for the canvases
const colours = ["red", "blue", "green"];

// Set canvas rectangle border and color
for (let i = 0; i < canvases.length; i++) {
    let ctx = canvases[i].getContext("2d");
    ctx.strokeStyle = colours[i];
    ctx.lineWidth = 2;
}

// Get the offset of the first canvas
var canvasOffset = canvases[0].getBoundingClientRect();
var offsetX = canvasOffset.left;
var offsetY = canvasOffset.top;

var isDown = false; // Track if the mouse is down
var startX; // Starting X coordinate
var startY; // Starting Y coordinate

// Handle mouse down event
function handleMouseDown(e) {
    console.log("handleMouseDown");
    e.preventDefault();
    e.stopPropagation();

    startX = parseInt(e.clientX - offsetX);
    startY = parseInt(e.clientY - offsetY);

    isDown = true;
}

// Handle mouse up event
function handleMouseUp(e) {
    console.log("handleMouseUp");
    e.preventDefault();
    e.stopPropagation();

    isDown = false;

    console.log(network_coordinates);
}

// Handle mouse out event
function handleMouseOut(e) {
    console.log("handleMouseOut");
    e.preventDefault();
    e.stopPropagation();

    isDown = false;

    console.log(network_coordinates);
}

// Handle mouse move event
function handleMouseMove(e) {
    if (!isDown) {
        return;
    }

    console.log("handleMouseMove");

    e.preventDefault();
    e.stopPropagation();

    mouseX = parseInt(e.clientX - offsetX);
    mouseY = parseInt(e.clientY - offsetY);

    let ctx = e.target.getContext("2d");

    // Clear the canvas
    ctx.clearRect(0, 0, canvases[0].width, canvases[0].height);

    let width = mouseX - startX;
    let height = mouseY - startY;

    // Draw the rectangle
    ctx.strokeRect(startX, startY, width, height);

    // Calculate coordinates, taking into account negative width and height
    let x1 = startX < mouseX ? startX : mouseX;
    let y1 = startY < mouseY ? startY : mouseY;
    let x2 = startX < mouseX ? mouseX : startX;
    let y2 = startY < mouseY ? mouseY : startY;

    // Store coordinates based on the current state
    if (state === "network") {
        network_coordinates = [x1, y1, x2, y2];
    } else if (state === "service") {
        service_coordinates = [x1, y1, x2, y2];
    } else if (state === "call") {
        call_coordinates = [x1, y1, x2, y2];
    }
}

// Add event listeners to each canvas
for (let i = 0; i < canvases.length; i++) {
    canvases[i].addEventListener("mousedown", function (e) {
        handleMouseDown(e);
    });
    canvases[i].addEventListener("mousemove", function (e) {
        handleMouseMove(e);
    });
    canvases[i].addEventListener("mouseup", function (e) {
        handleMouseUp(e);
    });
    canvases[i].addEventListener("mouseout", function (e) {
        handleMouseOut(e);
    });
}

// Function to handle confirm button click
function confirm_button_clicked(event) {
    // Check if all coordinates are selected
    if (
        network_coordinates.length === 0 ||
        service_coordinates.length === 0 ||
        (call_coordinates.length === 0 && window.callServiceIconPresent)
    ) {
        alert("Please select all the coordinates");
        return;
    }
    console.log(network_coordinates);
    console.log(service_coordinates);
    console.log(call_coordinates);
    // Save coordinates to cookies in format "x1, y1, x2, y2"
    document.cookie = `networkIconCoordinates=${network_coordinates}`;
    document.cookie = `networkStrengthIconCoordinates=${service_coordinates}`;
    document.cookie = `callServiceIconCoordinates=${call_coordinates}`;
    location.href = "/";
}
