// Event listener for DOMContentLoaded to ensure the script runs after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Create and append the canvas element to the document body
    const canvas = document.createElement('canvas');
    document.body.insertBefore(canvas, document.body.firstChild);
    const ctx = canvas.getContext('2d');

    // Set canvas dimensions to full viewport width and height
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    // Array to store dot objects
    let dots = [];
    const numberOfDots = 200; // Total number of dots to be generated
    const maxLineLength = 100; // Maximum length for lines connecting dots

    // Object to track mouse position and interaction radius
    let mouse = {
        x: null,
        y: null,
        radius: 100 // Radius around the mouse for interactive effects
    };

    // Class definition for Dot objects
    class Dot {
        constructor() {
            this.x = Math.random() * width; // Random x position
            this.y = Math.random() * height; // Random y position
            this.radius = Math.random() * 3 + 1; // Random radius
            this.baseRadius = this.radius; // Base radius for reset purposes
            this.maxRadius = 10; // Maximum radius for growth
            this.speedX = Math.random() * 2 - 1; // Horizontal speed
            this.speedY = Math.random() * 2 - 1; // Vertical speed
            this.color = `hsl(${Math.random() * 360}, 100%, 50%)`; // Random color
            this.baseColor = this.color; // Base color for reset purposes
        }

        // Method to update dot position based on speed
        move() {
            this.x += this.speedX;
            this.y += this.speedY;

            // Reverse direction if dot hits canvas edges
            if (this.x < 0 || this.x > width) this.speedX *= -1;
            if (this.y < 0 || this.y > height) this.speedY *= -1;

            // Calculate distance from the mouse
            let dx = this.x - mouse.x;
            let dy = this.y - mouse.y;
            let distance = Math.sqrt(dx * dx + dy * dy);

            // Dot interaction with mouse
            if (distance < mouse.radius) {
                if (this.radius < this.maxRadius) {
                    this.radius += 1; // Increase radius
                    this.color = `hsl(${360 * Math.random()}, 100%, 50%)`; // Change color
                }
            } else if (this.radius > this.baseRadius) {
                this.radius -= 1; // Decrease radius to base radius
                this.color = this.baseColor; // Reset to base color
            }
        }

        // Method to draw the dot on the canvas
        draw() {
            ctx.fillStyle = this.color;
            ctx.shadowColor = this.color;
            ctx.shadowBlur = 20; // Shadow for depth effect
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0; // Reset shadowBlur for other elements
        }
    }

    // Function to create dots and add them to the dots array
    function createDots() {
        for (let i = 0; i < numberOfDots; i++) {
            dots.push(new Dot());
        }
    }

    // Function to draw a line between two dots
    function drawLine(dot1, dot2) {
        const distance = Math.sqrt(Math.pow(dot1.x - dot2.x, 2) + Math.pow(dot1.y - dot2.y, 2));
        if (distance < maxLineLength) {
            // Set line width and opacity based on distance
            const lineWidth = 1 + (1 - distance / maxLineLength);
            const opacity = 1 - distance / maxLineLength;

            // Convert HSL to RGBA
            const color1 = hslToRgba(dot1.color, opacity);
            const color2 = hslToRgba(dot2.color, opacity);

            // Create a gradient for the line color
            const gradient = ctx.createLinearGradient(dot1.x, dot1.y, dot2.x, dot2.y);
            gradient.addColorStop(0, color1);
            gradient.addColorStop(1, color2);

            // Draw the line
            ctx.beginPath();
            ctx.strokeStyle = gradient;
            ctx.lineWidth = lineWidth;
            ctx.moveTo(dot1.x, dot1.y);
            ctx.lineTo(dot2.x, dot2.y);
            ctx.stroke();
        }
    }
    
    // Utility function to convert HSL to RGBA
    function hslToRgba(hsl, alpha) {
        // Extract HSL values
        const [h, s, l] = hsl.match(/\d+/g).map(Number);
        let r, g, b;
    
        if (s === 0) {
            r = g = b = l; // Achromatic
        } else {
            const hue2rgb = (p, q, t) => {
                if (t < 0) t += 1;
                if (t > 1) t -= 1;
                if (t < 1/6) return p + (q - p) * 6 * t;
                if (t < 1/2) return q;
                if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
                return p;
            };
    
            const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
            const p = 2 * l - q;
            r = hue2rgb(p, q, h / 360 + 1/3);
            g = hue2rgb(p, q, h / 360);
            b = hue2rgb(p, q, h / 360 - 1/3);
        }
    
        // Return RGBA string
        return `rgba(${r * 255}, ${g * 255}, ${b * 255}, ${alpha})`;
    }
    
    
// Function to animate the canvas
function animate() {
    ctx.clearRect(0, 0, width, height); // Clear the canvas

    // Update and draw each dot
    dots.forEach(dot => {
        dot.move();
        dot.draw();
    });

    // Draw lines between dots
    for (let i = 0; i < dots.length; i++) {
        for (let j = i + 1; j < dots.length; j++) {
            drawLine(dots[i], dots[j]);
        }
    }

    // Request the next animation frame
    requestAnimationFrame(animate);
}

// Create initial dots and start animation
createDots();
animate();

// Handle window resize events
window.addEventListener('resize', () => {
    // Update canvas size and reset dots
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    dots = [];
    createDots();
});

// Handle mouse movement
window.addEventListener('mousemove', (event) => {
    // Update mouse position
    mouse.x = event.x;
    mouse.y = event.y;
});
});
