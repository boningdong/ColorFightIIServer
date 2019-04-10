function createGameroom( data ) {
    if (data && data['gameroom_id']) {
        $.ajax( {
            url: "/creategameroom",
            method: "POST",
            dataType: "json",
            contentType: "application/json;charset=UTF-8",
            data: JSON.stringify( data ),
            success: function(msg) {
                document.location.reload()
            }
        } );
    }
}

function getConfig() {
    var data = {};
    data['gameroom_id'] = $( '#gameroom-name' ).val();
    return data;
}

$(function() {
    $( '#create-gameroom-button' ).click( function() {
        createGameroom( getConfig() );
    })
})
