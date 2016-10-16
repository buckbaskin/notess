(function ( $ ) {
    $.knowledge = function(string_text) {
        $.ajax({
            type: "GET",
            url: "/get_keywords",
            data: { text: string_text}
        }).done(function( result ) {
             console.log(result)
        });

        var $slider = $('<div id="knowledgeSlider"></div>');

        var showSlider = function() {

        };

        var hideSlider = function() {

        };

        var attachSlider = function() {

        };


        return {
            showSlider: showSlider,

        };
    };
}( jQuery ));