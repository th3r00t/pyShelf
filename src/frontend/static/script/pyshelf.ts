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

function getParams() {
  var url = window.location.href;
  var params = url.split('?')[1];
  if (params) {
    var paramstr = params.split('&');
    var paramsObj = {};
    for (var i = 0; i < paramstr.length; i++) {
      var param = paramstr[i].split('=');
      paramsObj[param[0]] = param[1];
    }
    return paramsObj;
  }
  return null;
}

function localStorePutTest(data) {
  console.log('localStorePutTest');
  localStorage.setItem('test', JSON.stringify(data));
}

function localStoreGetTest() {
  console.log('localStoreGetTest');
  console.log(localStorage.getItem('test'));
}

$(document).ready(function() {
  console.log(getParams());
  $(".navbar-burger").click(function(){
    $(".navbar-burger").toggleClass("is-active");
    $(".navbar-menu").toggleClass("is-active");
  });

  sizeMaster();
  $(window).on('resize', function() {
    sizeMaster();
  });
})
