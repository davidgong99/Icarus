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

        // Make request
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
                $('#view-ship-success').html("Ship successfully created");
                document.getElementById("view-ship-success").style.visibility = "visible";
            },
        }).fail(function (XMLHttpRequest, textStatus, error) {
            $('#add-ship-error').html(XMLHttpRequest.responseText);
            document.getElementById("add-ship-error").style.visibility = "visible";
            console.log("textStatus = " + textStatus);
            console.log("error = " + error);
        })


    })

    $(document).on('click', '#delete-ship-button', function() {
        // Grab inputs
        var deleteID = $('#shipsDelete input[name=spaceshipID]').val();

        // Store into payload object
        var payload = {
            "spaceshipID": deleteID
        }

        // Make request
        $.ajax({
            url: './spaceship',
            method: 'DELETE',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(payload),
            success: function(data) {
                console.log("Successful DELETE:" + data);
                // Redirect to view all existing ships
                showPage("shipsView");
                
                // Clear old information
                $("#deleteID").val('');
                document.getElementById("delete-ship-error").style.visibility = "hidden";

                // Set success message
                $('#view-ship-success').html("Ship successfully deleted");
                document.getElementById("view-ship-success").style.visibility = "visible";
            }
        }).fail(function (XMLHttpRequest, textStatus, error) {
            $('#delete-ship-error').html(XMLHttpRequest.responseText);
            document.getElementById("delete-ship-error").style.visibility = "visible";
            console.log("textStatus = " + textStatus);
            console.log("error = " + error);
        });
    })  
    

    // $(document).on('click','#add-location-button', function() {

    // })


});

function showPage(page){
    console.log("displaying #" + page);

    // Populate ships table when nav moves to the table
    if (page == "shipsView") {
        refreshShips();
    } else if (page == "locationsView") {
        refreshLocations();
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

function refreshLocations() {
    $.ajax({
        url: "./location",
        method: "GET",
        dataType: 'json',
        success: function(data){
            console.log("SUCCESSFUL AJAX");
            console.log(data);

            addLocationsToTable(data);
        }
    });
}

function addShipsToTable(ships) {
    // Remove any existing ships from table
    $('#shipsView > table > tbody').empty();

    for (const [key, value] of Object.entries(ships)) {
        var s = JSON.parse(value);
        $('#shipsView > table > tbody').append(
            '<tr><td>'
            + s.id
            + '</td><td>'
            + s.name
            + '</td><td>'
            + s.model
            + '</td><td>'
            + s.location
            + '</td><td>'
            + s.state
            + '</td></tr>'
        );
    }
}


function addLocationsToTable(locations) {
    // Remove any existing ships from table
    $('#locationsView > table > tbody').empty();

    for (const [key, value] of Object.entries(locations)) {
        var l = JSON.parse(value);
        $('#locationsView > table > tbody').append(
            '<tr><td>'
            + l.id
            + '</td><td>'
            + l.city
            + '</td><td>'
            + l.name
            + '</td><td>'
            + l.planet
            + '</td><td>'
            + l.capacity
            + '</td></tr>'
        );
    }
}
