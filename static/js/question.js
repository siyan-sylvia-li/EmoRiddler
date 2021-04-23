var questNum;
const name = "Mindy";

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
    //<img src="img_snowtops.jpg" class="w3-circle" alt="Norway" style="width:50vw; height: 50vw;">
    // Panel
    const wrap = document.createElement('div');
    wrap.setAttribute("class", "w3-panel w3-pale-green w3-cell-row")
    wrap.setAttribute("style", "padding-left:0;")
    const imgWrap = document.createElement('div')
    imgWrap.setAttribute("style", "width: 3vw; height: 3vw; display: inline-block; vertical-align: top;")
    imgWrap.setAttribute("class", "w3-cell")
    // Image of Mindy
    const agentImg = document.createElement('img')
    agentImg.setAttribute("src", "data:image/png;base64,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")
    agentImg.setAttribute("class", "w3-border")
    agentImg.setAttribute("style", "width: 3vw; height: 3vw;")
    imgWrap.appendChild(agentImg)
    // Agent name
    const nameP = document.createElement('p')
    nameP.setAttribute("style", "color: gray; opacity: 80%; margin-bottom: 0; margin-top: 0;")
    nameP.appendChild(document.createTextNode(name))
    // Text Response
    const textResp = document.createElement('p');
    textResp.setAttribute("style", "margin-bottom: 0; margin-top: 0;")
    textResp.appendChild(document.createTextNode(result['response']))
    const txtWrap = document.createElement("div")
    txtWrap.appendChild(nameP);
    txtWrap.appendChild(textResp);
    txtWrap.setAttribute("style", "display: inline-block;");
    txtWrap.setAttribute("class", "w3-cell w3-margin-left")
    wrap.appendChild(imgWrap);
    wrap.appendChild(txtWrap);
    feedback.appendChild(wrap);
    feedback.scrollTop = feedback.scrollHeight;
    const textRespNew = document.createElement('p');
    textRespNew.appendChild(document.createTextNode(name + ": " + result['response']))
    popup.innerHTML = ''
    popup.appendChild(textRespNew);
    popup.className = popup.className + " w3-show";
    setTimeout(function () {
        popup.className = popup.className.replace(" w3-show", "");
    }, 3000);
}