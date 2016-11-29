var GWS_CORE = (function() {
    var final_transcript = '';
    var interim_transcript = '';
    var recognizing = false;
    var ignore_onend;
    var start_timestamp;
    var keywords = [];
    var DATA_SERVICE;
    var start_button = document.getElementById("start_button");

    function init(dataService){
        DATA_SERVICE = dataService;
        dataService.setTranscriptSetter(setFinalTranscript);
    }

    if (!('webkitSpeechRecognition' in window)) {

    } else {
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onstart = function() {
            recognizing = true;
            DATA_SERVICE.onTranscriptCreate();
            showInfo('info_speak_now');
        };

        recognition.onerror = function(event) {
            if (event.error == 'no-speech') {
                showInfo('info_no_speech');
                ignore_onend = true;
            }
            if (event.error == 'audio-capture') {
                showInfo('info_no_microphone');
                ignore_onend = true;
            }
            if (event.error == 'not-allowed') {
                if (event.timeStamp - start_timestamp < 100) {
                    showInfo('info_blocked');
                } else {
                    showInfo('info_denied');
                }
                ignore_onend = true;
            }
        };

        recognition.onend = function() {
            recognizing = false;
            if (ignore_onend) {
                return;
            }
            if (!final_transcript) {
                showInfo('info_start');
                return;
            }
            showInfo('');
            if (window.getSelection) {
                window.getSelection().removeAllRanges();
                var range = document.createRange();
                range.selectNode(document.getElementById('final_span'));
                window.getSelection().addRange(range);
            }
        };

        recognition.onresult = function(event) {
            interim_transcript = '';
            for (var i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    final_transcript += event.results[i][0].transcript;
                } else {
                    interim_transcript += event.results[i][0].transcript;
                }
            }
            final_transcript = capitalize(final_transcript);
            final_span.innerHTML = linebreak(final_transcript);
            interim_span.innerHTML = linebreak(interim_transcript);
            if (final_transcript || interim_transcript) {
                // showButtons('inline-block');
            }
            showKeywordHyperlinks();
            DATA_SERVICE.onTranscriptUpdate(getTranscript());
        };
    }

    var showKeywordHyperlinks = function() {
        keywords = getKeywords();
        //console.log(keywords);
        var str = document.getElementById("final_span") ;
        keywords.sort(function(a, b){
            return b.length - a.length;
        });
        for (var i = 0; i < keywords.length; i++) {
            var word = keywords[i];
            var reg = new RegExp(word, "g");
            str.innerHTML = str.innerHTML.replace(reg, function(s) {
                return "<mark><a href='" + generateGoogleSearchURL(keywords[i]) + "'" + 'target="_blank"' +">" + word + "</a></mark>";
            });
        }
    };

    var generateGoogleSearchURL = function (keywords) {
        var url = "https://www.google.com/#q=";
        var keywords_list = keywords.split(" ");
        for (var i = 0; i < keywords_list.length; i++)
            url = url + "+" + keywords_list[i];
        return url;
    };

    var two_line = /\n\n/g;
    var one_line = /\n/g;
    function linebreak(s) {
        return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
    }

    var first_char = /\S/;
    function capitalize(s) {
        return s.replace(first_char, function(m) { return m.toUpperCase(); });
    }

    function startButton(event) {
        if (recognizing) {
            recognition.stop();
            start_button.innerHTML = "Restart Recording";
            return;
        }
        start_button.innerHTML = "Stop Recording";
        final_transcript = '';
        recognition.lang = 'en-US';
        recognition.start();
        ignore_onend = false;
        final_span.innerHTML = '';
        interim_span.innerHTML = '';
        // start_img.src = 'mic-slash.gif';
        showInfo('info_allow');
        start_timestamp = event.timeStamp;
    }

    function showInfo(s) {
        if (s) {
            for (var child = info.firstChild; child; child = child.nextSibling) {
                if (child.style) {
                    child.style.display = child.id == s ? 'inline' : 'none';
                }
            }
            info.style.visibility = 'visible';
        } else {
            info.style.visibility = 'hidden';
        }
    }

    function getTranscript() {
        return final_transcript;
    }

    function getInterimTranscript() {
        return interim_transcript;
    }

    function getKeywords() {
        return keywords;
    }

    function addKeywords(words) {
        keywords = keywords.concat(words);
        console.log("*** SET: " + keywords);
    }

    function setKeywords(words) {
        keywords = words;
    }

    function simulateTranscription(event){
        var textArea = document.getElementById("noteTextarea") ;
        var simulated_transcript = textArea.value;
        if (simulated_transcript.length < 10)
            simulated_transcript = "Bayesian inference is largely based on the principles of Bayes' theorem.";
        final_transcript = simulated_transcript;
        final_span.innerHTML = linebreak(final_transcript);
        //refresher = setInterval(highlightSimulation, 1500);
    }

    function setFinalTranscript(text){
        final_transcript = text;
        final_span.innerHTML = linebreak(final_transcript);
        //refresher = setInterval(highlightSimulation, 1500);
    }

    function highlightSimulation(){
        var final_span = document.getElementById("final_span") ;
        final_span.innerHTML = linebreak(final_transcript);
        showKeywordHyperlinks()
    }

    return {
        getTranscript: getTranscript,
        getInterimTranscript: getInterimTranscript,
        highlightSimulation: highlightSimulation,
        startButton: startButton,
        showInfo: showInfo,
        init: init,
        getKeywords: getKeywords,
        generateGoogleSearchURL: generateGoogleSearchURL,
        addKeywords: addKeywords,
        setKeywords: setKeywords,
        simulateTranscription: simulateTranscription,
    };
})();
