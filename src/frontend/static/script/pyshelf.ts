function getScreenSize() {
    return {
        width: window.innerWidth,
        height: window.innerHeight
    };
}
$(document).ready(function() {
    // Get the current URL
    var url = window.location.href;
    // Get the last part of the URL
    var screenSize = getScreenSize();
    var x: number = screenSize.width;
    var y: number = screenSize.height;
    console.log(x, y);
}
