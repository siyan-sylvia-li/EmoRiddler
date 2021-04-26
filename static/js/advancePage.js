const startNum = 2;
const endNum = 15;
const evalInterval = 6;
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
            if ((qNum === 7) || (qNum === 10)) {
                $('#display-content').load('/small_question?questNum=' + qNum.toString())
            } else if (qNum === 2) {
                $('#display-content').load('/long_question?questNum=' + qNum.toString())
            } else {
                $('#display-content').load('/question?questNum=' + qNum.toString())
            }
            if (sessionStorage.getItem(qNum.toString() + "Choice") !== null) {
                // Need to clear choices
                sessionStorage.removeItem(qNum.toString() + "Choice");
            }
        }

    } else if (page <= startNum) {
        $('#display-content').load('/p' + sessionStorage.getItem('page'));
        if (page === startNum) {
            updateUI({'response': "Hi, I'm Mindy. Let's Do This! :)"})
        }
    } else {
        // Calculate the number of items correct
        const cCount = calculateCorrect();
        $('#display-content').load('/final?count=' + cCount.toString());
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