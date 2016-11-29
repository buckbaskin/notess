var DATA_SERVICE = (function () {

    //GET v1/class/all
    var getAllClasses = function (userid, callback) {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/v1/class/all",
            data: {user_name: userid},
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot get notes.")
            }
        });
    };

    // POST /v1/class/new
    var createNewClass = function (userid, class_name, callback) {

        $.ajax({
            type: "POST",
            url: '/v1/class/new?username=' + userid + '&class_name=' + class_name,
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
    var getAllNote = function (userid, callback) {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/v1/note/all",
            data: {user_name: userid},
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot get notes.")
            }
        });
    };

    //GET v1/note/class
    var getAllNoteForClass = function (userid, classname, callback) {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/v1/note/class",
            data: {user_name: userid, class_name: classname},
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot get notes.")
            }
        });
    };

    // POST /v1/note/new
    var createNewNote = function (userid, content, callback) {
        console.log('/v1/note/new?username=' + userid);

        $.ajax({
            type: "POST",
            url: '/v1/note/new?username=' + userid,
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
    var updateNote = function (userid, noteid, content, callback) {
        console.log('/v1/note/update?username=' + userid + '&note_id=' + noteid);

        $.ajax({
            type: "POST",
            url: '/v1/note/update?username=' + userid + '&note_id=' + noteid,
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
    var getNote = function (userid, noteid, callback) {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/v1/note/get",
            data: {user_name: userid, note_id: noteid},
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot get notes.")
            }
        });
    };

    // GET /v1/transcript/note
    var getTranscriptForNote = function (userid, noteid, callback) {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/v1/transcript/note",
            data: {user_name: userid, note_id: noteid},
            success: function (result) {
                callback(result);
            },
            error: function () {
                console.log("Cannot get notes.")
            }
        });
    };

    // POST /v1/transcript/new
    var createTranscriptForNote = function (userid, noteid, content, callback) {
        console.log('/v1/transcript/new?username=' + userid + '&note_id=' + noteid);

        $.ajax({
            type: "POST",
            url: '/v1/transcript/new?username=' + userid + '&note_id=' + noteid,
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

    return {
        createNewClass: createNewClass,
        getAllClasses:getAllClasses,
        getAllNote: getAllNote,
        getAllNoteForClass: getAllNoteForClass,
        createNewNote: createNewNote,
        getNote: getNote,
        updateNote: updateNote,
        getTranscriptForNote: getTranscriptForNote,
        createTranscriptForNote: createTranscriptForNote
    }

});
