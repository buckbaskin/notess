var DATA_SERVICE = (function () {
    var userId;
    var noteId;

    // Saving mechanism for the text box.
    var lastSavedTime = new Date().getTime();
    var uploadedID = 0;
    var pendingID = 0;
    var timeout = 1500;

    var textArea = $('#noteTextarea');
    var noteTitle = $('#titleEditor');
    var noteTitleLabel = document.getElementById('titleLabel')

    var currentTranscriptId;
    var allTranscriptIds = [];
    var setFinalTranscript;

    var reflectiveCallback = function (result) {
        console.log(result)
    };

    //GET v1/class/all
    var getAllClasses = function (callback) {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/v1/class/all",
            data: {user_name: userId},
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot get notes.")
            }
        });
    };

    // POST /v1/class/new
    var createNewClass = function (class_name, callback) {

        $.ajax({
            type: "POST",
            url: '/v1/class/new?username=' + userId + '&class_name=' + class_name,
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({class_name: class_name}), //redundancy
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot create new notes")
            }
        });
    };

    //GET v1/note/all
    var getAllNote = function (callback) {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/v1/note/all",
            data: {user_name: userId},
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot get notes.")
            }
        });
    };

    //GET v1/note/class
    var getAllNoteForClass = function (classname, callback) {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/v1/note/class",
            data: {user_name: userId, class_name: classname},
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot get notes.")
            }
        });
    };

    // POST /v1/note/new
    var createNewNote = function (content, callback) {
        console.log('/v1/note/new?username=' + userId);

        $.ajax({
            type: "POST",
            url: '/v1/note/new?username=' + userId,
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(content),
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot create new notes")
            }
        });
    };

    // POST /v1/note/update
    var updateNote = function (content, callback) {
        console.log('/v1/note/update?username=' + userId + '&note_id=' + noteId);

        $.ajax({
            type: "POST",
            url: '/v1/note/update?username=' + userId + '&note_id=' + noteId,
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(content),
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot create new notes")
            }
        });
    };

    // GET /v1/note/get
    var getNote = function (callback) {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/v1/note/get",
            data: {user_name: userId, note_id: noteId},
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot get notes.")
            }
        });
    };

    // GET /v1/transcript/note
    var getCurrentTranscript = function (callback) {
        console.log('/v1/transcript/one?username=' + userId + '&transcript_id=' + currentTranscriptId);
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/v1/transcript/one",
            data: {username: userId, transcript_id: currentTranscriptId},
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot get notes.")
            }
        });
    };

    // POST /v1/transcript/new
    var createTranscriptForNote = function (content, callback) {
        console.log('/v1/transcript/new?username=' + userId + '&note_id=' + noteId);

        $.ajax({
            type: "POST",
            url: '/v1/transcript/new?username=' + userId + '&note_id=' + noteId,
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(content),
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot create new notes")
            }
        });
    };

    // POST /v1/transcript/update
    var updateTranscript = function (content, callback) {
        console.log('/v1/transcript/update?username=' + userId + '&transcript_id=' + currentTranscriptId);

        $.ajax({
            type: "POST",
            url: '/v1/transcript/update?username=' + userId + '&transcript_id=' + currentTranscriptId,
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(content),
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot create new notes")
            }
        });
    };

    var onNewNoteCreate = function (userid) {
        userId = userid;
        createNewNote({class_name: '', note_name: 'New Note', text: 'This is your new note'}, function (result) {
            result = JSON.parse(result);
            noteId = result._id.$oid;
            console.log(result._id.$oid);
            console.log(window.location.host);
            window.location.replace('http://' + window.location.host + '/docs?user_name='+ userId +'&note_id=' + noteId);
        });
    };

    var onNoteLoad = function (userid, note_id) {
        userId = userid;
        noteId = note_id;
        getNote(function (result) {
            console.log(result);
            var text = result['text'];
            textArea.val(text);
            noteTitleLabel.innerText = result.note_name;
            if (result.current_transcription_id == 'none'){
                console.log("no tid")
            }else{
                currentTranscriptId = result.current_transcription_id;
                getCurrentTranscript(function callback(result) {
                    setFinalTranscript(result.text);
                });
            }
        })
    };

    var onNoteUpdate = function () {
        var d = new Date();
        var time = d.getTime();
        var delta = time - lastSavedTime;
        if (delta > timeout) {
            lastSavedTime = time;
            uploadedID = pendingID;
            //save note call
            var pendingText = textArea.val();
            showUpdatedLabel("All Changes Saved");
            updateNote({text: pendingText}, function (callback) {
                reflectiveCallback(callback);
            });
            //console.log('sent--' + textArea.val());
        }
    };

    var showPendingLabel = function () {
        if (uploadedID < pendingID) {
            showUpdatedLabel("Pending changes");
        }
    };

    textArea.on('input', function () {
        pendingID++;
        showPendingLabel();
        setTimeout(function () {
            onNoteUpdate();
        }, timeout);
    });

    noteTitle.on('focusout', function () {
        var newTitle = noteTitleLabel.innerText;
        updateNote({note_name: newTitle}, reflectiveCallback)
    });

    var onTranscriptCreate = function () {
        createTranscriptForNote({text: ''}, function (result) {
            result = JSON.parse(result);
            currentTranscriptId = result._id.$oid;
            allTranscriptIds.push(currentTranscriptId);
            console.log('tid=' + currentTranscriptId);
            console.log('tids=' + allTranscriptIds);

            updateNote({current_transcription_id: currentTranscriptId},reflectiveCallback)
        })
    };

    var onTranscriptUpdate = function (finalized) {
        updateTranscript({text: finalized}, function () {
            // Do nothing.
        });
    };

    var showUpdatedLabel = function (text) {
        // Get the snackbar DIV
        var x = document.getElementById("snackbar2");

        // Add the "show" class to DIV
        x.className = "show";

        x.innerHTML = text;
    };

    var setTranscriptSetter = function (setterFunction) {
        setFinalTranscript = setterFunction;
    }

    return {
        createNewClass: createNewClass,
        getAllClasses: getAllClasses,
        getAllNote: getAllNote,
        getAllNoteForClass: getAllNoteForClass,
        getNote: getNote,
        onNoteLoad: onNoteLoad,
        onNewNoteCreate: onNewNoteCreate,
        updateNote: updateNote,
        getTranscriptForNote: getCurrentTranscript,
        createTranscriptForNote: createTranscriptForNote,
        onTranscriptCreate: onTranscriptCreate,
        onTranscriptUpdate: onTranscriptUpdate,
        setTranscriptSetter: setTranscriptSetter
    }

});
