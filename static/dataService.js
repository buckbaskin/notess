var DATA_SERVICE = (function () {
    var noteId;
    var currentTranscriptId;
    var allTranscripts = [];
    var setFinalTranscript;
    var noteController = NOTE_CONTROLLER();

    var defaultCallback = function (result) {
        console.log(result)
    };

    //GET v1/class/all
    var getAllClasses = function (userId, callback) {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/v1/class/all",
            data: {username: userId},
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot get notes.")
            }
        });
    };

    // POST /v1/class/new
    var createNewClass = function (userId, className, callback) {
        $.ajax({
            type: "POST",
            url: '/v1/class/new?username=' + userId + '&class_name=' + className,
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({class_name: className}), //redundancy
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot create new notes");
                noteController.showFailMsg();
            }
        });
    };

    //GET v1/note/all
    var getAllNotes = function(userId, callback) {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/v1/note/all",
            data: {username: userId},
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot get notes.")
            }
        });
    };

    //GET v1/note/class
    var getAllNotesForClass = function (userId, className, callback) {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/v1/note/class",
            data: {username: userId, class_name: className},
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot get notes.")
            }
        });
    };

    // POST /v1/note/new
    var createNewNote = function (userId, className, noteName, text, callback) {
        console.log('/v1/note/new?username=' + userId);
        $.ajax({
            type: "POST",
            url: '/v1/note/new?username=' + userId,
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({
                class_name: className,
                note_name: noteName,
                text: text
            }),
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
    var getCurrentTranscript = function (userId, transcriptId, callback) {
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

    // GET /v1/transcript/note
    var getAllTranscriptForUser = function (callback) {
        console.log('/v1/transcript/note?username=' + userId);
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/v1/transcript/all",
            data: {username: userId},
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot get notes.")
            }
        });
    };

    // GET /v1/transcript/note
    var getAllTranscriptForNote = function (callback) {
        console.log('simulated /v1/transcript/note?username=' + userId + '&note_id=' + noteId);
        getAllTranscriptForUser(function(result){
            var filtered = [];
            for (var i = 0; i < result.length; i++) {
                console.log(result[i].note_id.$oid);
                if (result[i].note_id.$oid == noteId)
                    filtered.push(result[i]);
            }
            callback(filtered);
        })
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

    var onTranscriptCreate = function () {
        createTranscriptForNote({text: ''}, function (result) {
            result = JSON.parse(result);
            currentTranscriptId = result._id.$oid;
            //allTranscriptIds.push(currentTranscriptId);
            console.log('tid=' + currentTranscriptId);
            //console.log('tids=' + allTranscriptIds);

            updateNote({current_transcription_id: currentTranscriptId},defaultCallback)
        })
    };

    var onTranscriptUpdate = function (finalized) {
        updateTranscript({text: finalized}, function () {
            // Do nothing.
        });
    };

    var setTranscriptSetter = function (setterFunction) {
        setFinalTranscript = setterFunction;
    };


    // Part of the below code interacts with the UI.

    // Saving mechanism for the text box.
    var lastSavedTime = new Date().getTime();
    var uploadedID = 0;
    var pendingID = 0;
    var timeout = 1500;

    var textArea = $('#noteTextarea');
    var noteTitle = $('#titleEditor');
    var noteTitleLabel = $('#titleLabel');

    // Download and display server content on load.
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
                getAllTranscriptForNote(function (result){
                    allTranscripts = result;
                    console.log(allTranscripts);
                });
            }
        })
    };

    // Updates the server when we detect local changes.
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
                defaultCallback(callback);
            });
            //console.log('sent--' + textArea.val());
        }
    };

    // textArea.on('input', function () {
    //     pendingID++;
    //     if (uploadedID < pendingID) {
    //         showUpdatedLabel("Pending changes");
    //     }
    //     setTimeout(function () {
    //         // Stop auto save for now
    //         //  onNoteUpdate();
    //     }, timeout);
    // });

    // noteTitle.on('focusout', function () {
    //     var newTitle = noteTitleLabel.innerText;
    //     updateNote({note_name: newTitle}, defaultCallback)
    // });

    return {
        createNewClass: createNewClass,
        getAllClasses: getAllClasses,
        getAllNotes: getAllNotes,
        getAllNotesForClass: getAllNotesForClass,
        createNewNote: createNewNote,
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
