(function ( $ ) {
    $.knowledge = function(text) {
        $.ajax({
            type: "POST",
            url: "~/pythoncode.py",
            data: { param: text}
        }).done(function( o ) {
             // do something
        });
    };
}( jQuery ));