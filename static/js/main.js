$(document).ready(function(){
    console.log("READY");
    // When page loads, display #shipsView
    $('.container > div').hide();
    $('.container > #shipsView').show();

    // Populate ships table for initial viewing
    refreshShips();

    // Handle clicking of nav items
    $('nav ul li').click(function() {
        console.log("naviation clickged");
        var displayPage = $(this).attr('data-displays');

        // Populate ships table when nav moves to the table
        if (displayPage == "shipsView") {
            refreshShips();
        }
        
        showPage(displayPage);
    })

    
    

    
});

function showPage(page){
    console.log("displaying #" + page);
    $('.container > div').hide();
    $('#'+page).show();
}

function refreshShips() {
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