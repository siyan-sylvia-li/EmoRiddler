const startNum = 2;
const endNum = 20;
const evalInterval = 5;
function movePage(direction) {
    $( "#display-content" ).empty();
    // Load items for the specific page
    var page = parseInt(sessionStorage.getItem('page'));
    page = page + direction;
    sessionStorage.setItem('page', page.toString())
    if (page > startNum && page < endNum) {
        if ((page - startNum) % evalInterval === 0) {
            $('#display-content').load('/feedback')
            updateUI({'response': "Please fill out the survey about your experience so far! Thank you :)"})
        } else {
            const qNum = (page - startNum) - Math.floor((page - startNum) / evalInterval)
            // Load questions
            $('#display-content').load('/question?questNum=' + qNum.toString())
            if (sessionStorage.getItem(qNum.toString() + "Choice") !== null) {
                // Need to clear choices
                sessionStorage.removeItem(qNum.toString() + "Choice");
            }
        }

    } else {
        $('#display-content').load('/p' + sessionStorage.getItem('page'));
        if (page === startNum) {
            updateUI({'response': "Hi, I'm Mindy. Let's Do This! :)"})
        }
    }

    // const prev = document.getElementById('prev');
    // if ((sessionStorage.getItem('page') !== '0') && (!(prev.classList.contains(' w3-show')))) {
    //     prev.className += " w3-show";
    // } else if (sessionStorage.getItem('page') === '0') {
    //     prev.className = prev.className.replace(" w3-show", "");
    //     defer(function () {
    //         generateID();
    //     })
    // }
}