var NOTE_CONTROLLER = (function () {
    var ds = DATA_SERVICE();
    var username = '';
    var userId = '';
    var saveButton = $('#saveButton');
    var noteTextBox = $('#noteTextarea');
    var transcriptTextBox = $();
    var noteTitle;
    var className;
    var classDropDownList = $('#classDropDownList');
    var noteList = $('#noteList');

    // setup event listeners
    var init = function () {
        populateDropDown();
        dropDownListener();
        loadAllNotes(loadNotesListCallback);
        saveButton.click(function () {
            console.log('Clicked save');
            var note = getNoteContents();

            noteTitle = $('#titleLabel').html();
            className = $('#className').html();
            console.log(className);
            console.log(noteTitle);
            if(noteTitle == 'Untitled Note' || noteTitle == ''
                || className == 'Class Name' || className == '') {
                showUpdatedLabel("Note needs a title and class name before save.");
            }
            else {
                getAllClassesForUser(function(result) {
                    console.log(result);
                   if(result.length == 0 || !checkIfClassExists(result, className)) {
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

    var dropDownListener = function() {
        $('#classDropDownList').on('click', 'li', function() {
            var classSelection = $(this).text();
            console.log(classSelection);
            $('#classDropDown').text(classSelection);
            noteList.empty();
            if(classSelection == 'All') {
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

    var getTranscriptContents = function () {

    };

    var setUsername = function (name) {
        username = name;
    };

    var setUserId = function (id) {
        userId = id;
    };

    var loadAllNotes = function (callback) {
        ds.getAllNotes(userId, callback);
    };

    var loadNotesForClass = function (className, callback) {
        ds.getAllNotesForClass(userId, className, callback);
    };

    var getNote = function (noteId) {
        ds.getNote(userId, noteId, function () {
            console.log(result);
        });
    };

    var createNewNote = function (className, noteName, text) {
        ds.createNewNote(userId, className, noteName, text, function (result) {
            console.log('Success saving note!');
            console.log(result);
        });
    };

    var updateNote = function (noteId, note) {
        ds.updateNote(userId, noteId, note, function () {
            console.log(result);
        });
    };

    var createTranscriptForNote = function () {

    };

    var getAllClassesForUser = function(callback) {
        ds.getAllClasses(userId, callback);
    };

    var populateDropDown = function() {
      getAllClassesForUser(function(result) {
        $.each(result, function(index, value) {
            classDropDownList.append('<li class="classSelection"><a href="#">'+value.class_name+'</a></li>');
        });
      });
    };

    var checkIfClassExists = function(classes, className) {
        var retVal = false;
        for(var i = 0; i < classes.length; i++) {
            if(classes[i].class_name == className) {
                retVal = true;
            }
        }
        return retVal;
    };

    var createNewClass = function(className) {
        ds.createNewClass(userId, className, function(result) {
            console.log('Successful call to create new class!');
            console.log(result);
            showSuccessMsg();
        })
    };

    var showSuccessMsg = function() {
      $('#saveSuccess').fadeIn('slow', function(){
          $('#saveSuccess').delay(2000).fadeOut('slow', function(){});
      });
    };

    var showFailMsg = function() {
      $('#saveFail').fadeIn('slow', function(){
          $('#saveFail').delay(2000).fadeOut('slow', function(){});
      });
    };

    //************** Callbacks ************************

    var loadNotesListCallback = function(result) {
        console.log(result);
        $.each(result, function(index, value){
            var noteName = value.note_name;
            var noteClass = value.class_name;
            noteList.append('<a href="#" class="list-group-item list-group-item-action">'+noteName+' &nbsp;&nbsp;&nbsp;&nbsp;<span class="label label-warning classTag">'+noteClass+'</span></a>');
        });
    };

    return {
        init: init,
        setUserId: setUserId,
        setUsername: setUsername,
        showFailMsg: showFailMsg
    }
});
