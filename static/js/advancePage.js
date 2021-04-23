const startNum = 2;
const endNum = 20;
function movePage(direction) {
    $( "#display-content" ).empty();
    // Load items for the specific page
    var page = parseInt(sessionStorage.getItem('page'));
    page = page + direction;
    sessionStorage.setItem('page', page.toString())
    if (page > startNum && page < endNum) {
        // Load questions
        $('#display-content').load('/question?questNum=' + (page - startNum).toString())
        if (sessionStorage.getItem((page - startNum).toString() + "Choice") !== null) {
            // Need to clear choices
            sessionStorage.removeItem((page - startNum).toString() + "Choice");
        }
    } else {
        $('#display-content').load('/p' + sessionStorage.getItem('page'))
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