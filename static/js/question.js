var questNum;
function registerChoice(choice) {
    // Amber - sand
    const opts = ['a', 'b', 'c', 'd']
    for (var o in opts) {
        console.log(o)
        const opt = document.getElementById(opts[o] + 'Opt')
        const ch = document.getElementById(opts[o] + 'Choice')
        if (opts[o] !== choice) {
            opt.className = opt.className.replace(' w3-amber', ' w3-cyan')
            ch.className = ch.className.replace(' w3-sand', ' w3-pale-blue')
        } else {
            opt.className = opt.className.replace(' w3-cyan', ' w3-amber')
            ch.className = ch.className.replace(' w3-pale-blue', ' w3-sand')
        }
    }
    questNum = parseInt(sessionStorage.getItem('page')) - startNum;
    sessionStorage.setItem(questNum.toString() + "Choice", choice);
}

function displayResults() {
    const correctAns = document.getElementById("correctAns").innerText.toLowerCase();
    console.log("Correct Answer", correctAns)
    const optCo = document.getElementById(correctAns + 'Opt')
    const choiceCo = document.getElementById(correctAns + 'Choice')
    optCo.className = optCo.className
        .replace(' w3-cyan', ' w3-green')
        .replace(' w3-amber', ' w3-green')
    choiceCo.className = choiceCo.className
        .replace(' w3-pale-blue', ' w3-pale-green')
        .replace(' w3-sand', ' w3-pale-green')
    const userAns = sessionStorage.getItem(questNum.toString() + "Choice")
    if (userAns !== correctAns) {
        const optUsr = document.getElementById(userAns + 'Opt')
        const choiceUsr = document.getElementById(userAns + 'Choice')
        optUsr.className = optUsr.className + ' w3-red'
        choiceUsr.className = choiceUsr.className + ' w3-pale-red'
        sessionStorage.setItem(questNum.toString() + "Choice", "incorrect")
    } else {
        sessionStorage.setItem(questNum.toString() + "Choice", "correct")
    }
    const correct = document.getElementById("correctWrap")
    correct.className = correct.className + " w3-show";
    document.getElementById("submit").disabled = true;
    requestResponse();
}

function requestResponse() {
    fetch('/response', {
        credentials: 'include',
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(response => response.json())
        .then(result => {
            console.log(result);
            updateUI(result);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function updateUI(result) {
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
}