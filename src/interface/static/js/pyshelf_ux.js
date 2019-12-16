$(document).ready(function(){
        $(".search_submit").click(function(){
                var query = $('.nav_search').val();
                console.log(query);
                window.location.href = '/search/'+query;
        })
        $('.nav_search').on('keypress', function (e) {
                if(e.which === 13){
                        $(this).attr("disabled", "disabled");
                        var query = $('.nav_search').val();
                        window.location.href = '/search/'+query;
                        $(this).removeAttr("disabled");
                }
        });
})
