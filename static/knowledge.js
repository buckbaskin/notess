(function ($) {
    $.knowledge = function() {
        var hidden = true;
        var keywordsList = $('#keywordsList');
        var floatingPanel = $('#floatingPanel');
        var keywordsButton = $('#keywordsButton');
        floatingPanel.css('box-shadow', '10px 10px 8px #888');



        var init = function () {
          keywordsButton.click(function() {
                toggleSlider();
          });
        };

        var populateKeywordPanel = function(text) {
            getKeywords(text, keywordsCallback);
        };

        var keywordsCallback = function(keywordsJson) {
            var keywords = [];
            for(var i = 0; i < keywordsJson.length; i++) {
                var obj = keywordsJson[i];
                console.log(obj);
                keywords.push(obj.text);
                keywordsList.append('<a href="#" class="list-group-item">' + obj.text + '</a>');
            }
            console.log(keywords);
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
                 dataType: "json",
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
            populateKeywordPanel: populateKeywordPanel

        };
    };

}( jQuery ));