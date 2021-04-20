function movePage(direction) {
    $( "#display-content" ).empty();
    // Load items for the specific page
    var page = parseInt(sessionStorage.getItem('page'));
    page = page + direction;
    sessionStorage.setItem('page', page.toString())
    $('#display-content').load('/p' + sessionStorage.getItem('page'))

    const prev = document.getElementById('prev');
    if ((sessionStorage.getItem('page') !== '0') && (!(prev.classList.contains(' w3-show')))) {
        prev.className += " w3-show";
    } else if (sessionStorage.getItem('page') === '0') {
        prev.className = prev.className.replace(" w3-show", "");
        defer(function () {
            generateID();
        })
    }
}