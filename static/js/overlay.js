document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById("overlay");
    const overlayContainer = document.getElementById("overlay-container");

    if (!canvas) {
        console.error("Canvas element not found!");
        return;
    }

    const context = canvas.getContext("2d");

    // Canvas size
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Create a new Image object for the logo
    const logo = new Image();
    logo.src = "static/images/overlay_logo.png"; // Path to your logo image

    let logoVisible = true;  // Variable to toggle logo visibility
    let overlayDissolved = false;  // Track if the overlay has been dissolved
    let cubesFalling = false; // Track if cubes should fall

    logo.onload = function () {
        // Draw the logo once it's loaded
        const logoWidth = 400;  // Set the desired width for the logo
        const logoHeight = 200; // Set the desired height for the logo
        const logoX = canvas.width / 2 - logoWidth / 2; // Center the logo horizontally
        const logoY = 200; // Position it towards the top of the canvas

        context.drawImage(logo, logoX, logoY, logoWidth, logoHeight);
    };

    // Cube properties
    const cubeSize = 10; // Cube size
    const cubes = []; // Array to store multiple cubes
    const gravity = 9.81; // Speed at which cubes fall

    const mouse = {
        x: 0,
        y: 0,
    };

    const repelDistance = 300; // Distance at which repelling happens
    const maxRepelForce = 20; // Maximum force to repel the cubes
    const lerpFactor = 0.6; // Controls how smoothly the cubes move

    // Create cubes at random positions, making sure they stay within the canvas
    function createCubes(numCubes) {
        for (let i = 0; i < numCubes; i++) {
            const x = Math.random() * (canvas.width - cubeSize);
            const y = Math.random() * (canvas.height - cubeSize);
            cubes.push({ x: x, y: y });
        }
    }

    // Handle mouse movement
    window.addEventListener("mousemove", (event) => {
        mouse.x = event.clientX;
        mouse.y = event.clientY;
    });

    // Handle click to activate cube falling
    canvas.addEventListener("click", () => {
        cubesFalling = true;
        setTimeout(() => {
        overlayDissolved = true; // Start dissolving the overlay after click
        // Start the transition to move the overlay out of view
        overlayContainer.style.transform = "translateY(-100%)";
        }, 1200); 
    });

    function updateCubePositions() {
        cubes.forEach(cube => {
            if (cubesFalling) {
                // Apply gravity to make cubes fall
                cube.y += gravity;
            } else {
                // Calculate the distance from the cube to the mouse
                const dx = mouse.x - cube.x;
                const dy = mouse.y - cube.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < repelDistance) {
                    // Normalize the direction vector
                    const directionX = dx / distance;
                    const directionY = dy / distance;

                    // Calculate the repel force (inversely proportional to distance)
                    const repelForce = Math.pow((repelDistance - distance) / repelDistance, 2) * maxRepelForce;

                    // Update the cube's position based on the repel force
                    cube.x -= directionX * repelForce * lerpFactor;
                    cube.y -= directionY * repelForce * lerpFactor;
                }

                // Prevent cubes from going outside the canvas (boundaries check)
                if (cube.x < 0) cube.x = 0;
                if (cube.x > canvas.width - cubeSize) cube.x = canvas.width - cubeSize;
                if (cube.y < 0) cube.y = 0;
                if (cube.y > canvas.height - cubeSize) cube.y = canvas.height - cubeSize;
            }
        });
    }

    function drawCubes() {
        // Clear the canvas first
        context.clearRect(0, 0, canvas.width, canvas.height);

        // Draw each cube
        context.fillStyle = "#FDFDFD";
        cubes.forEach(cube => {
            context.fillRect(cube.x, cube.y, cubeSize, cubeSize);
        });

        // Draw the logo if it's visible
        if (logoVisible && !overlayDissolved) {
            const logoWidth = 400;
            const logoHeight = 200;
            const logoX = canvas.width / 2 - logoWidth / 2;
            const logoY = 200;
            context.drawImage(logo, logoX, logoY, logoWidth, logoHeight);
        }
    }

    function animate() {
        updateCubePositions();
        drawCubes();
        requestAnimationFrame(animate);
    }

    // Create 50 cubes initially
    createCubes(50);

    animate();

    // Delay flickering by 3 seconds, then flicker every 1 second
    setTimeout(function () {
        setInterval(function () {
            if (!overlayDissolved) {
                logoVisible = !logoVisible;
            }
        }, 500); // Flicker every 1 second
    }, 3000); // Initial 3-second delay


});
