



let play_video = 1940
function handleButtonClick(event) {
    var buttonclass = event.target.parentElement.parentElement.id;
    play_video = buttonclass;
    
}

function speed_to_color(speed) {
    if(speed <= 20) return `rgb(255, 0, 0)`;
    else if(speed <= 60) return `rgb(255, ${Math.floor((speed - 20) * 256 / 40)}, 0)`;
    else if(speed < 100) return `rgb(${Math.floor((speed - 60) * 256 / 40)}, 255, 0)`;
    else return `rgb(0, 255, 0)`;
}

// Add event listeners to all buttons
document.querySelectorAll('button').forEach(button => {
    button.addEventListener('click', handleButtonClick);
});


function updateInfo() {
    const img = document.getElementById('videoStream');
    img.src = `./gui/${play_video}.jpg?${new Date().getTime()}`; // Add a timestamp to avoid caching
    const imgtitle = document.getElementById('videoTitle');
    imgtitle.textContent = `Showing mileage ${play_video} monitor`;

    var innerElements = document.querySelectorAll('.videorow');
    // Modify each element with the specific class value
    innerElements.forEach(innerElement => {
        let mileage = innerElement.id
        innerElement.querySelectorAll('.mileage')[0].textContent = mileage + ' m';
        fetch(`./gui/${innerElement.id}.json`) 
        .then(response => response.json()) // Parse the JSON data
        .then(data => {
            let avgElement = innerElement.querySelectorAll('.avg')[0]
            let predElement = innerElement.querySelectorAll('.pred')[0]
            avgElement.textContent = data[0] + ' km/hr';
            predElement.textContent = data[1] + ' km/hr';
            avgElement.style.background = speed_to_color(data[0])
            predElement.style.background = speed_to_color(data[1])
        })
    });
}



setInterval(updateInfo, 100); // Update the image every 100ms