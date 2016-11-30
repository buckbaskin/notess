var NOTE_CONTROLLER = function () {
    var ds = DATA_SERVICE();
    var username = '';
    var userId = '';
    var noteId;
    var saveButton = $('#saveButton');
    var noteTextBox = $('#noteTextarea');
    var transcript = $('#final_span');
    var noteTitle;
    var className;
    var classDropDownList = $('#classDropDownList');
    var noteList = $('#noteList');
    var updateButton = $('#updateButton');
    var deleteButtonCol = $('#deleteButtonCol');

    // setup event listeners
    var init = function () {
        deleteNoteListener();
        updateButtonListener();
        populateDropDown();
        dropDownListener();
        noteSelectionListener();
        loadAllNotes(loadNotesListCallback);
        saveButton.click(function () {
            console.log('Clicked save');
            var note = getNoteContents();

            noteTitle = $('#titleLabel').html();
            className = $('#className').html();
            console.log(className);
            console.log(noteTitle);
            if (noteTitle == 'Untitled Note' || noteTitle == ''
                || className == 'Class Name' || className == '') {
                showUpdatedLabel("Note needs a title and class name before save.");
            }
            else {
                getAllClassesForUser(function (result) {
                    console.log(result);
                    if (result.length == 0 || !checkIfClassExists(result, className)) {
                        console.log('creating a new class');
                        createNewClass(className);
                        createNewNote(className, noteTitle, note);
                    }
                    else {
                        createNewNote(className, noteTitle, note);
                    }
                });
            }
        });
    };

    var dropDownListener = function () {
        $('#classDropDownList').on('click', 'li', function () {
            var classSelection = $(this).text();
            console.log(classSelection);
            $('#classDropDown').text(classSelection);
            noteList.empty();
            if (classSelection == 'All') {
                loadAllNotes(loadNotesListCallback);
            }
            else {
                loadNotesForClass(classSelection, loadNotesListCallback);
            }
        });
    };

    var showUpdatedLabel = function (text) {
        // Get the snackbar DIV
        var x = document.getElementById("snackbar2");
        // Add the "show" class to DIV
        x.className = "show";
        x.innerHTML = text;
    };

    var getNoteContents = function () {
        return noteTextBox.val();
    };

    var setUsername = function (name) {
        username = name;
    };

    var setUserId = function (id) {
        userId = id;
        console.log(userId);
    };

    var loadAllNotes = function (callback) {
        ds.getAllNotes(userId, callback);
    };

    var loadNotesForClass = function (className, callback) {
        ds.getAllNotesForClass(userId, className, callback);
    };

    var getNote = function (noteId, callback) {
        ds.getNote(userId, noteId, callback);
    };

    var createNewNote = function (className, noteName, text) {
        ds.createNewNote(userId, className, noteName, text, function (result) {
            console.log('Success saving note!');
            console.log(JSON.parse(result));
            var noteId = JSON.parse(result)._id.$oid;
            console.log(noteId);
            createTranscriptForNote(noteId, function (result2) {
                console.log('Successful transcript save');
                console.log(result2);
            });
        });
    };

    var updateNote = function (noteId, note, callback) {
        ds.updateNote(userId, noteId, note, callback);
    };

    var createTranscriptForNote = function (noteId, callback) {
        var text = transcript.text();
        ds.createTranscriptForNote(userId, noteId, text, callback);
    };

    var getAllClassesForUser = function (callback) {
        ds.getAllClasses(userId, callback);
    };

    var populateDropDown = function () {
        getAllClassesForUser(function (result) {
            $.each(result, function (index, value) {
                classDropDownList.append('<li class="classSelection"><a href="#">' + value.class_name + '</a></li>');
            });
        });
    };

    var checkIfClassExists = function (classes, className) {
        var retVal = false;
        for (var i = 0; i < classes.length; i++) {
            if (classes[i].class_name == className) {
                retVal = true;
            }
        }
        return retVal;
    };

    var createNewClass = function (className) {
        ds.createNewClass(userId, className, function (result) {
            console.log('Successful call to create new class!');
            console.log(result);
            showSuccessMsg();
        });
    };

    var showSuccessMsg = function () {
        $('#saveSuccess').fadeIn('slow', function () {
            $('#saveSuccess').delay(2000).fadeOut('slow', function () {
            });
        });
    };

    var showSuccessUpdateMsg = function () {
        $('#updateSuccess').fadeIn('slow', function () {
            $('#updateSuccess').delay(2000).fadeOut('slow', function () {
            });
        });
    };

    var noteSelectionListener = function () {
        $('#noteList').on('click', 'a', function (e) {
            e.preventDefault();
            var noteId = $(this).attr('value');
            window.location.replace('http://' + window.location.host + '/edit?user=' + userId + '&note_id=' + noteId);
        });
    };

    var setNoteId = function(id) {
        noteId = id;
        console.log(noteId);
    };

    var populateEditPage = function() {
        getNote(noteId, function(result) {
            console.log(result);
            noteTitle = result.note_name;
            className = result.class_name;

            $('#titleLabel').html(noteTitle);
            $('#className').html(className);
            noteTextBox.val(result.text);
        });

        getTranscriptsForNote(noteId, function(result) {
            if(result.length > 0) {
                var trans = result[0].text;
                transcript.text(trans);
            }
        });
    };

    var getTranscriptsForNote = function(noteId, callback) {
        ds.getTranscriptsForNote(userId, noteId, callback);
    };

    var updateButtonListener = function() {
      updateButton.click(function() {
        updateNote(noteId, getNoteContents(), function(result) {
            console.log("Successful note update!");
            console.log(result);
            showSuccessUpdateMsg();
        });
      });
    };

    var deleteNoteListener = function() {
        $('.deleteNoteButton').click(function(e){
            console.log("Clicked delete!");
        });
    };

    //************** Callbacks ************************
    var loadNotesListCallback = function (result) {
        $.each(result, function (index, value) {
            var noteName = value.note_name;
            var noteClass = value.class_name;
            var element = $('<a href="#" class="list-group-item list-group-item-action noteElement">' + noteName + ' &nbsp;&nbsp;&nbsp;&nbsp;<span class="label label-warning classTag">' + noteClass + '</span></a>');
            var deleteRow = $('<div class="row deleteRow"><button class="btn btn-md btn-danger deleteNoteButton"><span class="glyphicon glyphicon-trash"></span></button></div>');
            var deleteButton = deleteRow.find('.deleteNoteButton');

            element.attr('value', value._id.$oid);
            noteList.append(element);
            deleteButton.attr('value', value._id.$oid);
            deleteButtonCol.append(deleteRow);
        });
    };

    return {
        init: init,
        setUserId: setUserId,
        setUsername: setUsername,
        setNoteId: setNoteId,
        populateEditPage: populateEditPage
    }
};
