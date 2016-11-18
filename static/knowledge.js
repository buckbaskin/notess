(function ($) {
    $.knowledge = function () {
        var recording = false;
        var hidden = true;
        var keywordsList = $('#keywordsList');
        var floatingPanel = $('#floatingPanel');
        var keywordsButton = $('#keywordsButton');
        var closeButton = $('#closebtn');
        var knowledge_cards = [];
        var dict = {};
        var stopAugmentRefreshID;
        var $recordButton = $('#start_button');
        var $refreshButton = $('#refresh_button');
        var transcription;
        var GWS_CORE;
        var defaultTitle = "Untitled Note"

        var recordButtonHandler = function () {
            $recordButton.click(function () {
                if (recording) {
                    // switch flag state to no recording
                    recording = false;
                    stopRefreshingKeywords(stopAugmentRefreshID);
                }
                else {
                    recording = true;
                }
            });
        };

        var refreshButtonHandler = function () {
            $refreshButton.click(function () {
                augmentTranscription();
            });
        };

        var init = function (gws_core) {
            GWS_CORE = gws_core;
            recordButtonHandler();
            refreshButtonHandler();
            floatingPanel.css('box-shadow', '10px 10px 8px #888');
            keywordsButton.click(function () {
                toggleSlider();
                augmentTranscription();
            });
            closeButton.click(function () {
                toggleSlider();
            });
            //stopAugmentRefreshID = setInterval(augmentTranscription, 5000);
            console.log(stopAugmentRefreshID);
        };

        var augmentTranscription = function () {
            transcription = GWS_CORE.getTranscript();
            if (transcription !== "" || typeof transcription === 'undefined') {
                populateKeywordPanel(transcription);
            }
        };

        var populateKeywordPanel = function (text) {
            if (text !== "" || typeof text === 'undefined') {
                getKeywords(text, keywordsCallback);
            }
            else {
                console.log('Text for populate keywords is empty.');
            }
        };

        var showSnackBar = function () {
            // Get the snackbar DIV
            var x = document.getElementById("snackbar")

            // Add the "show" class to DIV
            x.className = "show";

            // After 3 seconds, remove the show class from DIV
            setTimeout(function () {
                x.className = x.className.replace("show", "");
            }, 4500);
        }

        var keywordsCallback = function (keywordsJson) {
            // stores the 'text' field of each JSON object
            keywords = [];
            // stores the entire JSON object
            var keywordsJsonObjects = [];
            var updated = false;
            for (var i = 0; i < keywordsJson.length; i++) {
                var obj = keywordsJson[i];
                var word = obj.text;

                if (!isDuplicate(word)) {
                    keywords.push(word);
                    keywordsJsonObjects.push(obj);
                    //keywordsList.append('<a href="#" class="list-group-item">' + obj.text + '</a>');
                    updated = true;
                }
            }
            addDescriptions(keywordsJsonObjects, descriptionCallback);
            GWS_CORE.addKeywords(keywords);
            if (updated) {
                showSnackBar();
            }
            console.log("breakpoint")
        };

        var descriptionCallback = function (result) {
            var resultList = JSON.parse(result)["keywords"]
            for (var i = 0; i < resultList.length; i++) {
                var keywordItem = resultList[i];
                if (keywordItem.description != 'none') {
                    add_knowledge_card(create_knowledge_card(keywordItem.text, keywordItem.description));
                }
            }
            // Knowledge card added.
            updateKnowledgeCard();
        };

        function generateDisplayableCard(card) {
            var title = '<a href="' + GWS_CORE.generateGoogleSearchURL(card.keyword) + '" target="_blank"' +
                '><div class="list-group-item"><b><div class="knowledge-card-title">' +
                card.keyword + '</div></b></div></a>';
            var description = '<div class="knowledge-card-description"><div class="list-group-item">' + card.description + '</div>';
            return title + description;
        }

        var updateKnowledgeCard = function () {
            for (var key in knowledge_cards) {
                var card = knowledge_cards[key];
                if (!card.displayed){
                    keywordsList.append(generateDisplayableCard(card));
                    card.displayed = true;
                }
            }
        };

        var toggleSlider = function () {
            if (hidden) {
                populateKeywordPanel(GWS_CORE.getTranscript());
                // show
                // floatingPanel.animate({left: '-=500'}, 200, function(){});
                document.getElementById("floatingPanel").style.width = "30%";
                hidden = false;
            }
            else {
                // hide
                // floatingPanel.animate({left: '+=500'}, 200, function(){});
                document.getElementById("floatingPanel").style.width = "0";
                hidden = true;
            }
        };

        var getKeywords = function (string_text, callback) {
            $.ajax({
                type: "GET",
                dataType: "json",
                url: "/get_keywords",
                data: {text: string_text},
                success: function (result) {
                    callback(result);
                },
                error: function () {
                    console.log("Error in receiving keywords.")
                }
            });
        };

        var addDescriptions = function (keyword_list, callback) {
            if (keyword_list.length === 0) {
                return;
            }

            $.ajax({
                type: "POST",
                url: "/add_descriptions",
                contentType: 'application/json; charset=utf-8',
                data: JSON.stringify({keywords: keyword_list}),
                success: function (result) {
                    callback(result);
                },
                error: function () {
                    console.log("Error in receiving descriptions.")
                }
            });
        };

        var create_knowledge_card = function (keyword, description) {
            var knowledge_card = {};
            knowledge_card.displayed = false;
            knowledge_card.keyword = keyword;
            knowledge_card.description = description;
            return knowledge_card;
        };

        var add_knowledge_card = function (knowledge_card) {
            if (!((knowledge_card.keyword.toUpperCase()) in knowledge_cards)) {
                knowledge_cards[knowledge_card.keyword.toUpperCase()] = knowledge_card;
            }
        };

        var isDuplicate = function (word) {
            var retVal = true;
            if (dict[word] === undefined) {
                dict[word] = true;
                retVal = false;
            }
            return retVal;
        };

        var stopRefreshingKeywords = function () {
            clearInterval(stopAugmentRefreshID);
        };

        // Handle Title Editing
        // TODO: Get title from database if opening existing note
        var endEdit = function(e) {
            var input = $(e.target),
                label = input && input.prev();
            label.text(input.val() === '' ? defaultTitle : input.val());
            input.hide();
            label.show();
        };

        $('.clickedit').hide()
        .focusout(endEdit)
        .keyup(function (e) {
            if ((e.which && e.which == 13) || (e.keyCode && e.keyCode == 13)) {
                endEdit(e);
                return false;
            } else {
                return true;
            }
        })
        .prev().click(function () {
            $(this).hide();
            $(this).next().show().focus();
        });

        return {
            toggleSlider: toggleSlider,
            addDescriptions: addDescriptions,
            getKeywords: getKeywords,
            init: init,
            populateKeywordPanel: populateKeywordPanel,
            stopRefreshingKeywords: stopRefreshingKeywords,
            isDuplicate: isDuplicate
        };
    };

}(jQuery));