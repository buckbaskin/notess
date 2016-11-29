(function ($) {
    $.knowledge = function () {
        var recording = false;
        var hidden = true;
        var tutorial = $('#tutorial');
        var keywordsList = $('#keywordsList');
        var floatingPanel = $('#floatingPanel');
        var keywordsButton = $('#keywordsButton');
        var closeButton = $('#closebtn');
        var loadingWheel = $("#loading");
        var knowledge_cards = [];
        var dict = {};
        var stopAugmentRefreshID;
        var $recordButton = $('#start_button');
        var $refreshButton = $('#refresh_button');
        var transcription;
        var GWS_CORE;
        var DATA_SERVICE;
        var defaultTitle = "Untitled Note";
        var currentTranscriptionId = "";
        var transcriptions = [];

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
                onTranscriptionUpdate();
            });
        };

        var init = function (gws_core, data_service) {
            GWS_CORE = gws_core;
            loadingWheel.hide();
            DATA_SERVICE = data_service;
            if (document.cookie != "tutorial=true"){
                document.cookie = "tutorial=true";
                tutorial.modal('toggle');
            }else{
                console.log("Tutorial already displayed")
            }
            recordButtonHandler();
            refreshButtonHandler();
            floatingPanel.css('box-shadow', '10px 10px 8px #888');
            keywordsButton.click(function () {
                toggleSlider();
                onTranscriptionUpdate();
            });
            closeButton.click(function () {
                toggleSlider();
            });
            //stopAugmentRefreshID = setInterval(onTranscriptionUpdate, 5000);
            console.log(stopAugmentRefreshID);
        };

        var onTranscriptionUpdate = function () {
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

        var showSnackBar = function (hasNewKeyword) {
            // Get the snackbar DIV
            var x = document.getElementById("snackbar");

            // Add the "show" class to DIV
            x.className = "show";

            if (hasNewKeyword){
                x.innerHTML = "New keywords added";
            }else{
                x.innerHTML = "Refreshed, no new keywords found";
            }

            // After 3 seconds, remove the show class from DIV
            setTimeout(function () {
                x.className = x.className.replace("show", "");
            }, 3000);
        };

        var keywordsCallback = function (keywordsJson) {
            loadingWheel.show();
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
            if (keywordsJsonObjects.length == 0){
                loadingWheel.hide();
            }
            addDescriptions(keywordsJsonObjects, descriptionCallback);
            GWS_CORE.addKeywords(keywords);
            showSnackBar(updated);
            GWS_CORE.highlightSimulation();
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
            loadingWheel.hide();
            console.log('Hiding Wheel!');
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
                document.getElementById("floatingPanel").style.width = "40%";
                hidden = false;
            }
            else {
                // hide
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