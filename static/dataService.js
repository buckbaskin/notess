var DATA_SERVICE = (function(){

  var getNotesList = function(userID, callback) {
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "",
        data: {user_id: userID},
        success: function (result) {
            callback(result);
        },
        error: function () {
            console.log("Error retrieving notes list.")
        }
    });
  }

  var getNote = function(noteID, callback) {
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "",
        data: {note_id: noteID},
        success: function (result) {
            callback(result);
        },
        error: function () {
            console.log("Error retrieving note.")
        }
    });
  }

  var saveNote = function(userID, note, callback) {
    $.ajax({
        type: "PUT",
        dataType: "json",
        url: "",
        data: {
          user_id: userID,
          note_string: note
        },
        success: function (result) {
            callback(result);
        },
        error: function () {
            console.log("Error saving note.")
        }
    });
  }

  var getTranscription = function(trasncriptionID, callback) {
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "",
        data: {transcription_id: transcriptionID},
        success: function (result) {
            callback(result);
        },
        error: function () {
            console.log("Error retrieving transcription.")
        }
    });
  }

  var saveTranscription = function(userID, callback) {
    $.ajax({
        type: "PUT",
        dataType: "json",
        url: "",
        data: {user_id: userID},
        success: function (result) {
            callback(result);
        },
        error: function () {
            console.log("Error saving transcription.")
        }
    });
  }

  return {
    getNotesList: getNotesList,
    getNote: getNote,
    saveNote: saveNote,
    getTranscription: getTranscription,
    saveTranscription: saveTranscription
  }

});
