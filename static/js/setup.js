function defer(method) {
    if (document.getElementById("partID") != null) {
        method();
    } else {
        setTimeout(function() { defer(method) }, 50);
    }
}

function generateID() {
    if (sessionStorage.getItem('participantID') == null) {
        const ID = Math.floor(1000 + Math.random() * 9000);
        sessionStorage.setItem('participantID', ID.toString());
    }
    const partID = document.getElementById("partID");
    partID.appendChild(document.createTextNode(sessionStorage.getItem('participantID')));
}

function setup() {
    $('#display-content').load('/p0');
    console.log("SETUP");
    defer(function () {
        generateID();
    })
    sessionStorage.setItem('page', '0');
}