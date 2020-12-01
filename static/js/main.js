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

        
        
        showPage(displayPage);
    })

    
    // Handle submission for adding spaceship
    $(document).on('click', '#add-ship-button', function() {

        // Grab inputs
        var name = $('#shipsAdd input[name=name]').val();
        var model = $('#shipsAdd input[name=model]').val();
        var location = $('#shipsAdd input[name=location]').val();
        var state = $('#shipsAdd input[name=state]').val();
        
        // Store into payload object
        var payload = {
            'name': name,
            'model': model,
            'location': location,
            'state': state
        };

        // Verify and send data
        $.ajax({
            url: './spaceship',
            method: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(payload),
            success: function(data) {
                // Redirect to view all existing ships
                showPage("shipsView");
                console.log("Successful POST:" + data);

                // Clear old information
                $("#name").val('');
                $("#model").val('');
                $("#location").val('');
                $("#state").val('');
                document.getElementById("add-ship-error").style.visibility = "hidden";

                // Set success message
                $('#add-ship-success').html("Ship successfully created");
                document.getElementById("add-ship-success").style.visibility = "visible";
            },
        }).fail(function (XMLHttpRequest, textStatus, error) {
            $('#add-ship-error').html(XMLHttpRequest.responseText);
            document.getElementById("add-ship-error").style.visibility = "visible";
            console.log("textStatus = " + textStatus);
            console.log("error = " + error);
        })


    })

    
});

function showPage(page){
    console.log("displaying #" + page);

    // Populate ships table when nav moves to the table
    if (page == "shipsView") {
        refreshShips();
    }
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