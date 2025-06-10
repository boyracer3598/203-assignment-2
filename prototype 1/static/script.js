let angle = 0;
let isSquished = false;
let isPopped = false;


function rotateImage() {
    const image = document.getElementById('Image-rotate');
    
    let speed = 5; // degrees per interval
    const intervalId = setInterval(() => {
        angle = (angle + speed) % 360;
        image.style.transform = `rotate(${angle}deg)`;
        speed = Math.max(0, speed - 0.1); // Gradually decrease speed, clamped to a minimum of 0
        if (speed <= 0) {
            speed = 0; // Stop decreasing speed when it reaches zero
            clearInterval(intervalId);
        }
    }, 100);
}


function squishImage(){
    const image = document.getElementById('Image-squish');
    let scale = 1;
    if(!isSquished){
        image.style.transform = `scaleY(${scale-0.2})`;
        isSquished = true;
    }else{
        image.style.transform = `scaleY(${scale})`;
        isSquished = false;
    }
    
}

function dragImage(){
    const image = document.getElementById('Image-drag');
    
}

function popBalloon(){
    if (isPopped) return; // Prevent multiple pops
    isPopped = true; // Set popped state to true
    image = document.getElementById('Image-balloon');
    image.src = 'static/images/balloon2.png';
    setTimeout(() => {
        image.src = 'static/images/balloon3.png';
        setTimeout(() => {
            image.src = 'static/images/balloon4.png';
        }, 300);
    }, 300);
}

function resetBalloon() {
    if (!isPopped) return; // Only reset if it was popped
    isPopped = false; // Reset popped state
    const image = document.getElementById('Image-balloon');
    image.src = 'static/images/balloon1.png'; // Reset to original balloon image
}