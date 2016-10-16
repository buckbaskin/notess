(function ($) {
    $.knowledge = function() {

        var plugin = this;

        var $slider = $('<div id="knowledgeSlider"></div>');

        var showSlider = function() {

        };

        var hideSlider = function() {

        };

        var attachSlider = function() {

        };

        var getKeywords = function(string_text, callback) {
             $.ajax({
                 type: "GET",
                 url: "/get_keywords",
                 data: { text: string_text},
                 success: function (result) {
                   callback(result);
                 },
                 error: function () {
                     console.log("Error in receiving keywords.")
                 }
             });
        };

        return {
            showSlider: showSlider,
            getKeywords: getKeywords,

        };
    };

}( jQuery ));