$(document).ready(function(){
    console.log("READY");
    // When page loads, display #shipsView
    $('.container > div').hide();
    $('.container > #shipsView').show();

    // Handle clicking of nav items
    $('nav ul li').click(function() {
        console.log("naviation clickged");
        var displayPage = $(this).attr('data-displays');
        showPage(displayPage);
    })
    console.log("adsads");

    refreshShips();

    console.log("after refresh ships");

});

function showPage(page){
    console.log("displaying #" + page);
    $('.container > div').hide();
    $('#'+page).show();
}

function refreshShips() {
    console.log("pre-ajax");
    $.ajax({
        url: "./spaceship",
        method: "GET",
        dataType: 'json',
        success: function(data){
            console.log("SUCCESSFUL AJAX");
            console.log(data);

            addShipsToTable(data);
        }
    });
    console.log("post-ajax");
}

function addShipsToTable(ships) {
    // Remove any existing ships from table
    $('table > tbody').empty();

    len = Object.keys(ships).length;
    
    // Loop through each ship, and append to table as a new row
    for (i = 0; i < len; i++) {
        var obj = JSON.parse(ships[i]);
        $('table > tbody').append(
            '<tr><td>'
            + obj.id
            + '</td><td>'
            + obj.name
            + '</td></tr>'
        );
    }
}