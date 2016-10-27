(function ($) {
    $.knowledge = function() {
        var hidden = true;
        var keywordsList = $('#keywordsList');
        var floatingPanel = $('#floatingPanel');
        var keywordsButton = $('#keywordsButton');
        var dict = {};
        var stopAugmentRefreshID;


        floatingPanel.css('box-shadow', '10px 10px 8px #888');

        var init = function () {
          keywordsButton.click(function() {
                toggleSlider();
                augmentTranscription();
          });
            stopAugmentRefreshID = setInterval(augmentTranscription, 10000);
            console.log(stopAugmentRefreshID);
        };

        var augmentTranscription = function() {
            var transcription = getTranscript();
            if (transcription !== "" || typeof transcription === 'undefined') {
                populateKeywordPanel(transcription);
            }
        };

        var populateKeywordPanel = function(text) {
            getKeywords(text, keywordsCallback);
        };

        var keywordsCallback = function(keywordsJson) {
            var keywords = [];
            console.log(keywordsJson);
            for(var i = 0; i < keywordsJson.length; i++) {
                var obj = keywordsJson[i];
                var word = obj.text;

                if(!isDuplicate(word)) {
                    keywords.push(obj);
                    keywordsList.append('<a href="#" class="list-group-item">' + obj.text + '</a>');
                }
            }
            var keyWordObjs = {};
            keyWordObjs['keywords'] = keywords;
            console.log('**********' + keywords.toString());
            addDescriptions(keywords, function(result) {console.log(result)});
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

        var addDescriptions = function(keyword_list, callback) {
            if(keyword_list.length === 0) {
                return;
            }

            $.ajax({
                 type: "POST",
                 url: "/add_descriptions",
                 contentType: 'application/json; charset=utf-8',
                 data: JSON.stringify({ keywords: keyword_list}),
                 success: function (result) {
                   callback(result);
                 },
                 error: function () {
                     console.log("Error in receiving descriptions.")
                 }
             });
        };

        var isDuplicate = function (word) {
            var retVal = true;
            if(dict[word] === undefined) {
                dict[word] = true;
                retVal = false;
            }
            return retVal;
        };

        var stopRefreshingKeywords = function() {
            console.log("STOPPING");
            clearInterval(stopAugmentRefreshID);
            console.log(stopAugmentRefreshID);
        };

        return {
            toggleSlider: toggleSlider,
            addDescriptions: addDescriptions,
            getKeywords: getKeywords,
            init: init,
            populateKeywordPanel: populateKeywordPanel,
            stopRefreshingKeywords: stopRefreshingKeywords,

        };
    };

}( jQuery ));