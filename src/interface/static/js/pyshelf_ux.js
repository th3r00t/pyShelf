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
    var s_string = "search by Title, Author, Tags, or Collections";
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
    $('.nav_link').on('mouseover', function (e){
        var popover_str = $(this).attr('alt');
        x = $(this).offset().left;
        y = $(this).offset().to;
        $('.popover').html(popover_str);
        $('.popover').css('left', x+nav_width);
        $('.popover').css('top', y);
        $('.popover').css('display','flex');
    });
    $('.nav_link').on('mouseout', function (e){
        var popover_str = $(this).attr('alt');
        x = $(this).offset().left;
        y = $(this).offset().top;
        $('.popover').html(popover_str);
        $('.popover').css('left', x);
        $('.popover').css('top', y);
        $('.popover').css('display','none');
    });
    $('#btn_collections').on('click', function (e){
        $('.hidden.vert-nav.collections').toggle();
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
    })
    $('.favorite_action').on('click', function(){
        $(this).children('a').toggleClass('favorite');
    });
    $('#sortlist').change(function () {
        var optionSelected = $(this).find("option:selected");
        var valueSelected  = optionSelected.val();
        var textSelected   = optionSelected.text();
        window.location.href="/"+valueSelected;
    });
    $('#btn-home').on("click", function(){
        _location = $(this).attr('data-location');
        window.location.href=_location;
    });
    $('#flip_sort').on("click", function(){
        window.location.href="/flip_sort/"+$("#_order").val();
    });
    $('#search_string').html("<i> "+$('#_search').val().substr(0,15)+"</i>");
    
    $('#pop_over_0').dialog({ autoOpen: false });
    resize_search();
    $(window).resize(resize_search(win_width));

    $('#pop_over_0').on('click', 'div.collection', function(){
        window.location.href = '/show_collection/'+$(this).attr('data');
    });
    $('#btn_login').on('click', function() {
        var isopen = $('#pop_over_0').dialog("isOpen");
        if (isopen) {
            $('#pop_over_0').dialog("close");
            return;
        }
        customlog(['Login Clicked']);
        $.ajax({
            type: "GET", url: "/live", data: {hook: 'register'},
            success: function (response) {
                // Set the dialog title
                $('#pop_over_0').dialog({
                    title: "User Controls",
                    maxHeight: (win_height - 100),
                    minWidth: $("#horiz_nav_main").width(),
                    hide: {effect: "blind", duration: 1000},
                    show: {effect: "blind", duration: 1000},
                    position: {
                        my: "top", at: "bottom", of: $("#horiz_nav_main")
                    }
                });
                // clear and create a new container
                $('#pop_over_0').html('<div id=usercp class="mx-auto">');
                // Populate the container from response.data
                $('#usercp').append('<div class="row" id="usercp-inner">');
                $('#usercp-inner').append(response.data);
                $('#usercp-inner').append('</div>');
                $('#usercp').append('</div>');
                // Close the container
                $('#pop_over').append('</div>');
                // Now open this dialog
                $('#pop_over_0').dialog("open");
            },
            error: function (response) {
                customlog(["Failure", response]);
            }
        });
    });
    $('#btn_logout').on('click', function() {
        window.location.href = '/logout';
    });
    $('#coll_button').on('click', function(){
        var isopen = $('#pop_over_0').dialog("isOpen");
        if (isopen){
            $('#pop_over_0').dialog("close");
            return;
        }
        customlog(['Collections Clicked']);
        $.ajax({
            type: "GET", url: "/live", data: {hook: 'collection_listing'},
            success: function(response){
                // Set the dialog title
                $('#pop_over_0').dialog({
                    title: "Collections",
                    maxHeight: (win_height-100),
                    minWidth: $("#horiz_nav_main").width(),
                    hide: { effect: "blind", duration: 1000 },
                    show: { effect: "blind", duration: 1000 },
                    position: { my: "top", at: "bottom", of: $("#horiz_nav_main")
                    }
                });
                // clear and create a new container
                $('#pop_over_0').html('<div id=collections>');
                // Populate the container from response.data
                $.each(response.data, function(index, value){
                    $('#collections').append("<div class=collection data='"+value+"/"+$('#_set').val()+"'>"+value+"</div>");
                });
                // Close the container
                $('#pop_over').append('</div>');
                // Now open this dialog
                $('#pop_over_0').dialog("open");
            },
            error: function(response){
                customlog(["Failure", response]);
            }
        });
    });
    $('.info-button').on('click', function(){
        var isopen = $('#pop_over_0').dialog("isOpen");
        if (isopen){
            $('#pop_over_0').dialog("close");
            return;
        }
        customlog(['Book Details Clicked', $(this).attr('data')]);
        $.ajax({
            type: "GET", url: "/live", data: {hook: 'details', pk:$(this).attr('data')},
            success: function(response){
                // Set the dialog title
                $('#pop_over_0').dialog({
                    title: "Collections",
                    maxHeight: (win_height-100),
                    minWidth: $("#horiz_nav_main").width(),
                    hide: { effect: "blind", duration: 1000 },
                    show: { effect: "blind", duration: 1000 },
                    position: { my: "top", at: "bottom", of: $("#horiz_nav_main")
                    }
                });
                // clear and create a new container
                $('#pop_over_0').html('<div id=collections>');
                // Populate the container from response.data
                $.each(response.data, function(index, value){
                    $('#collections').append("<div class=collection data='"+value+"/"+$('#_set').val()+"'>"+value+"</div>");
                });
                // Close the container
                $('#pop_over').append('</div>');
                // Now open this dialog
                $('#pop_over_0').dialog("open");
            },
            error: function(response){
                customlog(["Failure", response]);
            }
        });
    });
});
function resize_search(win_width){
    if (win_width <= 1025){
        $('.search_string').attr('size', 20);
        $('.search_string').val("Search");
    }
    if (win_width <= 426){
        $('.search_string').attr('size', 10);
        $('.search_string').val("Search");
    }
}

