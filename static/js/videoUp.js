const feedback = document.getElementById('feedback-content');
const popup = document.getElementById("popup");
setInterval(function () {
    if ((videoElement.srcObject !== null) && (parseInt(sessionStorage.getItem('page')) > 1)) {
        // const videoContext = videoElement.getContext('2d');
        // window.open("", document.getElementById('videoWrap').toDataURL())
        // console.log(videoElement.video)
        context.drawImage(video, 0, 0, w, h);
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
                // Create new element
            // <div class="w3-panel w3-pale-green">
                //   <p>London is the most populous city in the United Kingdom,
                //   with a metropolitan area of over 9 million inhabitants.</p>
                // </div>
                var wrap = document.createElement('div')
                wrap.setAttribute("class", "w3-panel w3-pale-green")
                var textResp = document.createElement('p')
                textResp.appendChild(document.createTextNode(result['response']))
                wrap.appendChild(textResp)
                feedback.appendChild(wrap)
                feedback.scrollTop = feedback.scrollHeight;
                var textRespNew = document.createElement('p')
                textRespNew.appendChild(document.createTextNode(result['response']))
                popup.innerHTML = ''
                popup.appendChild(textRespNew);
                popup.className = popup.className + " w3-show";
                setTimeout(function () {
                    popup.className = popup.className.replace(" w3-show", "");
                }, 3000);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}, 5000)