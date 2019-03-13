var studentform = (function() {

    // PRIVATE VARIABLES
        
    var apiUrl = 'http://127.0.0.1:5000'; //backend running on localhost 
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
     * Add event handlers for creating a new account.
     * @return {None}
     */
    var attachCreateAccountHandler = function(e) {

        var url_string = window.location.href;
        var url = new URL(url_string);
        var id = url.searchParams.get("id"); // The account id to identify the user

        // Button to create new account
        createButton = $(".button1").first();

        // Body of create new account prompt
        //createBody = $(".form1");

        // Add on click handler for create account button
        createButton.on('click', function(e) {

            var account = {}; 

            // Collect the new account information
            account.major = $("#Major1").val();
            account.gpa = $("#GPA1").val();
            //account.bio = createBody.find("#bio").val();
            //account.avaliable_data.find("#beginDate").val();
            //account.end_date.find("#endDate").val();

            account.space = accountSpace;

         


            var onSuccess = function(data) {
                //window.location.href = "../html/student_Profile.html" + "?id=" + data.student.id.toString();
                window.location.replace("http://127.0.0.1:5000/api/studentProfile");
            };
            var onFailure = function() { 
                console.error('create account failed'); 
            };

            // Send account info to server
            makePostRequest('/api/students/' + "5", account, onSuccess, onFailure);
            

        });

    };

    /**
     * Start the app by displaying the most recent smiles and attaching event handlers.
     * @return {None}
     */
    var start = function() {

        attachCreateAccountHandler();
    };



    
    // PUBLIC METHODS
    return {
        start: start
    };
    
})();
