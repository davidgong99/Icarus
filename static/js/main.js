$(document).ready(function(){
    // When page loads, display #shipsView
    $('.container > div').hide();
    $('.container > #shipsView').show();

    // Populate ships table for initial viewing
    refreshShips();

    // Handle clicking of nav items
    $('nav ul li').click(function() {
        var displayPage = $(this).attr('data-displays');        
        showPage(displayPage);
    })

    
    // ======================
    //
    //      Add spaceship
    //
    // ======================
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
            // Write and display error message
            $('#add-ship-error').html(XMLHttpRequest.responseText);
            document.getElementById("add-ship-error").style.visibility = "visible";
        })
    })

    // ======================
    //
    //      Update spaceship state
    //
    // ======================
    // Handle submission for updating spaceship state
    $(document).on('click', '#update-ship-button', function() {

        // Grab inputs
        var spaceshipID = $('#shipsUpdate input[name=updateShipID]').val();
        var newState = $('#shipsUpdate input[name=newState]').val();
        
        // Store into payload object
        var payload = {
            'spaceshipID': spaceshipID,
            'state': newState
        };

        // Make request
        $.ajax({
            url: './spaceship',
            method: 'PUT',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(payload),
            success: function(data) {
                // Redirect to view all existing ships
                showPage("shipsView");

                // Clear old information
                $("#updateShipID").val('');
                $("#newState").val('');
                document.getElementById("update-ship-error").style.visibility = "hidden";

                // Set success message
                $('#view-ship-success').html("Ship successfully updated");
                document.getElementById("view-ship-success").style.visibility = "visible";
            },
        }).fail(function (XMLHttpRequest, textStatus, error) {
            // Write and display error message
            $('#update-ship-error').html(XMLHttpRequest.responseText);
            document.getElementById("update-ship-error").style.visibility = "visible";
            
        })
    })



    // ======================
    //
    //      Delete spaceship
    //
    // ======================
    // Handle submission for deleting spaceship
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
                // Redirect to view all existing ships
                showPage("shipsView");
                
                // Clear old information
                $("#spaceshipID").val('');
                document.getElementById("delete-ship-error").style.visibility = "hidden";

                // Set success message
                $('#view-ship-success').html("Ship successfully deleted");
                document.getElementById("view-ship-success").style.visibility = "visible";
            }
        }).fail(function (XMLHttpRequest, textStatus, error) {
            // Write and display error message
            $('#delete-ship-error').html(XMLHttpRequest.responseText);
            document.getElementById("delete-ship-error").style.visibility = "visible";
        });
    })  
    


    // ======================
    //
    //      Add location
    //
    // ======================
    // Handle submission for adding location
    $(document).on('click','#add-location-button', function() {
        // Grab inputs
        var city = $('#locationsAdd input[name=city]').val();
        var name = $('#locationsAdd input[name=name]').val();
        var planet = $('#locationsAdd input[name=planet]').val();
        var capacity = $('#locationsAdd input[name=capacity]').val();

        // Store into payload object
        var payload = {
            "city": city,
            "name": name,
            "planetName": planet,
            "capacity": capacity
        }

        // Make request
        $.ajax({
            url: './location',
            method: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(payload),
            success: function(data) {
                // Redirect to view all existing locations
                showPage("locationsView");

                // Clear old information
                $("#city").val('');
                $("#location_name").val('');
                $("#planet").val('');
                $("#capacity").val('');
                document.getElementById("add-location-error").style.visibility = "hidden";

                // Set success message
                $('#view-location-success').html("Location successfully created");
                document.getElementById("view-location-success").style.visibility = "visible";
            },
        }).fail(function (XMLHttpRequest, textStatus, error) {
            // Write and display error message
            $('#add-location-error').html(XMLHttpRequest.responseText);
            document.getElementById("add-location-error").style.visibility = "visible";
        })
    })

    // ======================
    //
    //      Delete location
    //
    // ======================
    // Handle submission for deleting location
    $(document).on('click', '#delete-location-button', function() {
        // Grab inputs
        var deleteID = $('#locationsDelete input[name=locationID]').val();

        // Store into payload object
        var payload = {
            "locationID": deleteID
        }

        // Make request
        $.ajax({
            url: './location',
            method: 'DELETE',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(payload),
            success: function(data) {
                // Redirect to view all existing locations
                showPage("locationsView");
                
                // Clear old information
                $("#locationID").val('');
                document.getElementById("delete-location-error").style.visibility = "hidden";

                // Set success message
                $('#view-location-success').html("Location successfully deleted");
                document.getElementById("view-location-success").style.visibility = "visible";
            }
        }).fail(function (XMLHttpRequest, textStatus, error) {
            // Write and display error message
            $('#delete-location-error').html(XMLHttpRequest.responseText);
            document.getElementById("delete-location-error").style.visibility = "visible";
        });
    })  

    // ======================
    //
    //      Travel
    //
    // ======================
    // Handle submission for spaceship travel between locations
    $(document).on('click', '#travel-button', function() {
        // Grab inputs
        var spaceshipID = $('#travel input[name=travelShipID]').val();
        var locationID = $('#travel input[name=travelLocationID]').val();
        
        // Store into payload object
        var payload = {
            'spaceshipID': spaceshipID,
            'locationID': locationID
        };

        // Make request
        $.ajax({
            url: './travel',
            method: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(payload),
            success: function(data) {
                // Redirect to view all existing ships
                showPage("shipsView");

                // Clear old information
                $("#travelShipID").val('');
                $("#travelLocationID").val('');
               
                document.getElementById("travel-error").style.visibility = "hidden";

                // Set success message
                $('#view-ship-success').html("Ship successfully travelled");
                document.getElementById("view-ship-success").style.visibility = "visible";
            },
        }).fail(function (XMLHttpRequest, textStatus, error) {
            // Write and display error message
            $('#travel-error').html(XMLHttpRequest.responseText);
            document.getElementById("travel-error").style.visibility = "visible";
        })
    })

});


// Redirection function for nav bar
// Hides and shows necessary elements
function showPage(page){
    // Populate ships table when nav moves to the table
    if (page == "shipsView") {
        refreshShips();
    } else if (page == "locationsView") {
        refreshLocations();
    }
    $('.container > div').hide();
    $('#'+page).show();
}

// Request and display spaceships in spaceship table
function refreshShips() {
    $.ajax({
        url: "./spaceship",
        method: "GET",
        dataType: 'json',
        success: addShipsToTable
    });
}

// Request and display locations in location table
function refreshLocations() {
    $.ajax({
        url: "./location",
        method: "GET",
        dataType: 'json',
        success: addLocationsToTable
    });
}


// Render spaceships as rows in table
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

// Render locations as rows in table
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
            + '</td><td>'
            + l.maxCapacity
            + '</td></tr>'
        );
    }
}
