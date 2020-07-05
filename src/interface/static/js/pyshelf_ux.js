$(document).ready(function(){
    function customlog(outstream) {
        /* Gather my variables and output them */
        for (var i = 0; i < outstream.length; i++){
            console.log(">> "+outstream[i]);
        };
    };
    /* Initialize ui variables */
    var outstream = []; // put customlog messages here
    var win_height = window.innerHeight; // Get the displays height
    var win_width = window.innerWidth; // Get the displays width
    var scr_height = window.outerHeight;
    var scr_width = window.outerWidth;
    var hdr_height = $('.app_hdr').height(); // Get our header height
        var ftr_height = $('.app_footer').height(); // Get our footer height
    var nav_width = $('.nav_l').width(); // Get the width of our nav items
    var cmp_height = window.screen.availHeight;
    var max_height = win_height - (hdr_height + ftr_height) - (scr_height - win_height); // Set our available height
    var u_string = "Username";
    var p_string = "Password";
    var s_string = "search by Title, Author, Tags, or Collections"
    customlog([cmp_height]);
    $(".search_submit").click(function(){
            var query = $('.nav_search').val();
            console.log(query);
            window.location.href = '/search/'+query;
    });
    $('.nav_search').on('keypress', function (e) {
            if(e.which === 13){
                    $(this).attr("disabled", "disabled");
                    var query = $('.nav_search').val();
                    window.location.href = '/search/'+query;
                    $(this).removeAttr("disabled");
            }
    });
//    $('#app').css("height", max_height);
//    $('.nav_l').css("max-height", max_height);
//   $('div.shelf').css("max-height", max_height);
    $('.nav_link').on('mouseover', function (e){
        var popover_str = $(this).attr('alt');
        x = $(this).offset().left
        y = $(this).offset().top
        $('.popover').html(popover_str);
        $('.popover').css('left', x+nav_width);
        $('.popover').css('top', y);
        $('.popover').css('display','flex');
    });
    $('.nav_link').on('mouseout', function (e){
        var popover_str = $(this).attr('alt');
        x = $(this).offset().left
        y = $(this).offset().top
        $('.popover').html(popover_str);
        $('.popover').css('left', x);
        $('.popover').css('top', y);
        $('.popover').css('display','none');
    });
    $('#btn_collections').on('click', function (e){
        $('.hidden.vert-nav.collections').toggle()
    });
    $('.input_box').on('click', function(){
        $(this).attr("value","");
    });
    $('.input_box').focusout(function(){
        if ($(this).hasClass('nav_search') && $(this).val() == "") {
           $(this).attr("value", s_string);
        }
        if ($(this).attr("id") == "username" && $(this).val() == "") {
           $(this).attr("value", u_string);
        }
        if ($(this).attr("id") == "password" && $(this).val() == "") {
           $(this).attr("value", p_string);
        }
    });
    $('#btn_login').on('click', function(){
        $('#hdr_nav_login').toggle();
    });
    $('#sortlist').change(function () {
        var optionSelected = $(this).find("option:selected");
        var valueSelected  = optionSelected.val();
        var textSelected   = optionSelected.text();
        window.location.href="/"+valueSelected
    });
    $('#btn-home').on("click", function(){
        _location = $(this).attr('data-location');
        window.location.href=_location;
    });
    $('#search_string').html("<i> "+$('#_search').val().substr(0,15)+"</i>")
    if (win_width >= 1024)
        $('.search_string').attr('size', 20)
        $('.search_string').val("Search")
    if (win_width >= 425)
        $('.search_string').attr('size', 10)
        $('.search_string').val("Search")
});
