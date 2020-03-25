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
    var win_width = window.innwerWidth; // Get the displays width
    var scr_height = window.outerHeight;
    var scr_width = window.outerWidth;
    var hdr_height = $('.app_hdr').height(); // Get our header height
    var ftr_height = $('.app_footer').height(); // Get our footer height
    var nav_width = $('.nav_l').width(); // Get the width of our nav items
    var cmp_height = window.screen.availHeight;
    var max_height = win_height - (hdr_height + ftr_height) - (scr_height - win_height); // Set our available height
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
    $('#app').css("height", max_height);
    $('.nav_l').css("max-height", max_height);
    $('div.shelf').css("max-height", max_height);
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
})
