$(document).ready(function(){
        $(".search_submit").click(function(){
                var query = $('.nav_search').val();
                console.log(query);
                window.location.href = '/search/'+query;
        })
})
