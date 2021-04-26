const feedback = document.getElementById('feedback-content');
const popup = document.getElementById("popup");

function uploadSnap() {
    console.log("Take")
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    var uri = canvas.toDataURL('image/png')
    fetch('/emotion', {
        credentials: 'include',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(
          {'usr_img': uri}
          )
      }).then(response => response.json())
        .then(result => {
            console.log(result);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// setInterval(function () {
//     if ((videoElement.srcObject !== null) && (parseInt(sessionStorage.getItem('page')) > startNum)) {
//         // const videoContext = videoElement.getContext('2d');
//         // window.open("", document.getElementById('videoWrap').toDataURL())
//         // console.log(videoElement.video)
//         uploadSnap();
//     }
// }, 2000)
