var StudentProfile = (function() {

    // PRIVATE VARIABLES
        
    var apiUrl = 'http://localhost:5000'; //backend running on localhost

    // FINISH ME (Task 4): You can use the default smile space, but this means
    //            that your new smiles will be merged with everybody else's
    //            which can get confusing. Change this to a name that 
    //            is unlikely to be used by others. 
    var accountSpace = 'default'; // The account space to use. 


    // PRIVATE METHODS
      
   /**
    * HTTP GET request 
    * @param  {string}   url       URL path, e.g. "/api/smiles"
    * @param  {function} onSuccess   callback method to execute upon request success (200 status)
    * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
    * @return {None}
    */
   var makeGetRequest = function(url, onSuccess, onFailure) {
       $.ajax({
           type: 'GET',
           url: apiUrl + url,
           dataType: "json",
           success: onSuccess,
           error: onFailure
       });
   };

    /**
     * HTTP POST request
     * @param  {string}   url       URL path, e.g. "/api/smiles"
     * @param  {Object}   data      JSON data to send in request body
     * @param  {function} onSuccess   callback method to execute upon request success (200 status)
     * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
     * @return {None}
     */
    var makePostRequest = function(url, data, onSuccess, onFailure) {
        $.ajax({
            type: 'POST',
            url: apiUrl + url,
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            success: onSuccess,
            error: onFailure
        });
    };
        
    /**
     * Add function to load profile data.
     * @return {None}
     */
    var loadProfileData = function(e) {

        var url_string = window.location.href;
        var url = new URL(url_string);
        var id = url.searchParams.get("id"); // The account id to identify the user

        var onSuccess = function(data) {
            // Update name, Gpa, major on page
            $("#name").text(data.student.first_name + " " + data.student.last_name);
            document.getElementById("gpa").innerHTML = "GPA: ".bold() + data.student.gpa;
            document.getElementById("major").innerHTML = "Major: ".bold() + data.student.major;
        };
        var onFailure = function() { 
            console.error('Get profile data failed'); 
        };
        
        // Send account info to server
        makeGetRequest('/api/students/' + id, onSuccess, onFailure);


    };


    /**
     * Add event handlers for editing profile.
     * @return {None}
     */
    var attachEditProfileHandler = function(e) {

        // Update Button to submit profile changes
        updateButton = $(".card-footer").first().find("button");

        // Body of edit profile card
        editBody = $(".card-body");

        // Add on click handler for create account button
        updateButton.on('click', function(e) {

            var account = {}; // Prepare the account object to send to the server
            var url_string = window.location.href;
            var url = new URL(url_string);
            var id = url.searchParams.get("id"); // The account id to identify the user

            // Collect the new account information
            account.gpa = editBody.find("#editGpa").val();
            account.major = editBody.find("#editMajor").val();
            //account.grad_date = editBody.find("editGrad").val();
            
            var onSuccess = function(data) {
                // Update Gpa, major on page
                document.getElementById("gpa").innerHTML = "GPA: ".bold() + data.student.gpa;
                document.getElementById("major").innerHTML = "Major: ".bold() + data.student.major;
                
            };
            var onFailure = function() { 
                console.error('Edit failed'); 
            };

            
            // Send account info to server
            makePostRequest('/api/students/' + id, account, onSuccess, onFailure);
            

        });

    };

    /**
     * Start the app by displaying the most recent smiles and attaching event handlers.
     * @return {None}
     */
    var start = function() {

        loadProfileData();
        attachEditProfileHandler();
        
    };

    

    // PUBLIC METHODS
    return {
        start: start

    };
    
})();
