(function ($) {
    $.knowledge = function() {
        var hidden = true;
        var floatingPanel = $('#floatingPanel');
        floatingPanel.css('box-shadow', '10px 10px 8px #888');
        var keywordsButton = $('#keywordsButton');


        var init = function () {
          keywordsButton.click(function() {
                toggleSlider();
          });
        };

        var toggleSlider = function() {
            if(hidden) {
                // show
                floatingPanel.animate({left: '-=500'}, 200, function(){});
                hidden = false;
            }
            else {
                // hide
                floatingPanel.animate({left: '+=500'}, 200, function(){});
                hidden = true;
            }
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
            toggleSlider: toggleSlider,
            getKeywords: getKeywords,
            init: init,

        };
    };

}( jQuery ));