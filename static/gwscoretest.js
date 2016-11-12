var GWS_CORE_TEST = (function() {
    var final_transcript = '';
    var interim_transcript = '';
    var ignore_onend;
    var start_timestamp;
    var keywords = [];



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
        keywords_list = keywords.split(" ");
        for (var i = 0; i < keywords_list.length; i++)
            url = url + "+" + keywords_list[i];
        return url;
    }

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
    }

    function setKeywords(words) {
        keywords = words;
    }

    return {
        getTranscript: getTranscript,
        getInterimTranscript: getInterimTranscript,
        startButton: startButton,
        showInfo: showInfo,
        getKeywords: getKeywords,
        addKeywords: addKeywords,
        setKeywords: setKeywords,
    };
})();
