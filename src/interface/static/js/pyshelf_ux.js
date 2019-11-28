$(document).ready(function(){
    //_set = $('input#_set').attr('value');
    $('input.next_page').on('click', function(){next_page(1)});
    $('input.prev_page').on('click', function(){prev_page(1)});

    function next_page(set){
        /*
                var re = new RegExp(/^.*\//);
                var _root =  re.exec(window.location.href);
                var _path = _root[0].substring(0, _root[0].length -1)
                document.location.href = 'next_page?bookset='+set;
        */
        console.log("next_page clicked");
        var _r = $.get('next_page', 'bookset='+set);
        console.log(_r);
    }

    function prev_page(set){
        /*
                var re = new RegExp(/^.*\//);
                var _root = re.exec(window.location.href);
                document.location.href = _root+'prev_page?bookset='+set;
        */
        console.log("prev_page clicked");
        $.get('prev_page', 'bookset='+set);
    }
});
