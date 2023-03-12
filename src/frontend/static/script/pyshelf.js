function getScreenSize() {
    return {
        width: window.innerWidth,
        height: window.innerHeight
    };
}
function sizeMaster() {
    var size = getScreenSize();
    var navbar = $('#navbar-main').height();
    var footer = $('#footer-main').height();
    var master = $('#master').height(size.height - navbar - footer);
}
$(document).ready(function () {
    // Get the current URL
    var url = window.location.href;
    // Get the last part of the URL
    sizeMaster();
    $(window).on('resize', function () {
        sizeMaster();
    });
});
