$(document).ready(function(){
    function customlog(outstream) {
        /* Gather my variables and output them */
        for (var i = 0; i < outstream.length; i++){
            console.log(">> "+outstream[i]);
        };
    };
    /* Initialize ui variables */
    let outstream = []; // put customlog messages here
    let win_height = window.innerHeight; // Get the displays height
    let win_width = window.innerWidth; // Get the displays width
    let scr_height = window.outerHeight;
    let scr_width = window.outerWidth;
    let hdr_height = $('.app_hdr').height(); // Get our header height
    let ftr_height = $('.app_footer').height(); // Get our footer height
    let nav_width = $('.nav_l').width(); // Get the width of our nav items
    let cmp_height = window.screen.availHeight;
    let max_height = win_height - (hdr_height + ftr_height) - (scr_height - win_height); // Set our available height
    const u_string = "Username";
    const p_string = "Password";
    const s_string = "search by Title, Author, Tags, or Collections";
    const popover = $('#pop_over_0')
    const navlink = $('.nav_link')
    const inputbox = $('input_box')
    const loginbtn = $('#btn_login')
    const server = ('ws://127.0.0.1:1337')
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
    $(navlink).on('mouseover', function (e){
        var popover_str = $(this).attr('alt');
        x = $(this).offset().left;
        y = $(this).offset().to;
        $('.popover').html(popover_str);
        $('.popover').css('left', x+nav_width);
        $('.popover').css('top', y);
        $('.popover').css('display','flex');
    });
    $(navlink).on('mouseout', function (e){
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
    $(inputbox).on('click', function(){
        $(this).attr("value","");
    });
    $(inputbox).focusout(function(){
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
    $(loginbtn).on('click', function(){
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
    $(popover).dialog({ autoOpen: false });
    $(popover).on('click', 'div.collection', function(){
        window.location.href = '/show_collection/'+$(this).attr('data');
    });
    $(loginbtn).on('click', function() {
        var isopen = $('#pop_over_0').dialog("isOpen");
        if (isopen) {
            $('#pop_over_0').dialog("close");
            return;
        }
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
        //window.location.href = '/logout';
        var isopen = $('#pop_over_0').dialog("isOpen");
        if (isopen) {
            $('#pop_over_0').dialog("close");
            return;
        }
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
        $('#usercp-inner').append(
            '<div class="col-auto" id="usercp-col1">' +
            '<button type="submit" class="btn-sm btn-secondary import-btn"><i class="fas fa-file-import"></i>&nbsp; Import Books</button>' +
            '</div>' +
            '<div class="col-auto" id="usercp-col2">' +
            '<button type="submit" class="btn-sm btn-secondary logout-btn"><i class="fas fa-sign-out-alt"></i>&nbsp; Logout</button>' +
            '</div>'
        );
        $('#usercp-inner').append('</div>');
        $('#usercp').append('</div>');
        // Close the container
        $('#pop_over').append('</div>');
        // Now open this dialog
        $('#pop_over_0').dialog("open");
    });
    $(document).on('click', '.logout-btn', function(){window.location.href = '/logout'});
    $(document).on('click', '.import-btn', function(){
        let socket = PyshelfSocket(server);
        ping(socket);
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
                    title: response.data['title'],
                    maxHeight: (win_height-100),
                    minWidth: $("#horiz_nav_main").width(),
                    hide: { effect: "blind", duration: 1000 },
                    show: { effect: "blind", duration: 1000 },
                    position: { my: "center center", at: "center center", of: window
                    }
                });
                // clear and create a new container
                $('#pop_over_0').html('<div id=book_expanded>');
                // Populate the container from response.data
                $('#book_expanded').append('<div class=row><div class="col-auto">Title</div><div class="col-auto text-muted">'+response.data['title']+'</div></div>')
                $('#book_expanded').append('<div class=row><div class="col-auto">Author</div><div class="col-auto text-muted">'+response.data['author']+'</div></div>')
                if (response.data['description']!== null){
                    $('#book_expanded').append('<div class=row><div class="col-auto">Expanded Description</div><div class="col-auto text-muted">'+response.data['description']+'</div></div>')

                }
                if (response.data['tags'] !== null){
                    $('#book_expanded').append('<div class=row><div class="col-auto">Tags</div><div class="col-auto text-muted">'+response.data['tags']+'</div></div>')
                }
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
    resize_search();
    $(window).resize(resize_search(win_width));
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

function PyshelfSocket(address) {
    const connection = new WebSocket(address);
    connection.onconnect = function(e){
       ping(connection);
    };
    connection.onmessage = function(rcvd){
       sock_rx(rcvd) 
    };
    return connection;
}
function sock_rx(rcvd) {
    if (rcvd.data == 'pong') { pong(rcvd.data) }
    else { console.log("<<[rx] :"+rcvd.data) }
}
function sock_status(sock) {
    let buffered = sock.connection.bufferedAmmount;
    let ready = sock.connection.readyState;
    return [buffered, ready];
}
function ping(sock) {
    sock.send('ping')
}
function pong(rcvd) {
    console.log("<<["+rcvd.data+"] "+rcvd.data)
}
