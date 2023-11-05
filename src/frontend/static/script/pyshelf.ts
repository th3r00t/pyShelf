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

$(document).ready(function() {
  // Get the current URL
  var url = window.location.href;
  console.log(url);
  // Get the last part of the URL
  $(".navbar-burger").click(function(){
    $(".navbar-burger").toggleClass("is-active");
    $(".navbar-menu").toggleClass("is-active");
  });
  sizeMaster();
  $(window).on('resize', function() {
    sizeMaster();
  });
})
