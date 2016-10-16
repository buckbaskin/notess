(function ( $ ) {
    $.knowledge = function(string_text) {
        $.ajax({
            type: "GET",
            url: "/get_keywords",
            data: { text: string_text}
        }).done(function( result ) {
             console.log(result)
        });
    };
}( jQuery ));