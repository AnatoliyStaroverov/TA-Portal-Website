var Portal = (function() {

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

        // Button to create new account
        createButton = $(".modal-footer").first().find("button");
        // Body of create new account prompt
        createBody = $(".modal-body");

        // Add on click handler for create account button
        createButton.on('click', function(e) {

            var account = {}; // Prepare the account object to send to the server

            // Collect the new account information
            account.first_name = createBody.find("#first-name").val();
            account.last_name = createBody.find("#last-name").val();
            account.email = createBody.find("#email").val();
            account.password = createBody.find("#pwd").val();
            account.student_id = createBody.find("studentid").val();
            account.space = accountSpace;

            // Determine which account to create (Student or Instructor)
            var isStudentChecked = createBody.find('#customRadio2').prop('checked');
            var isInstructorChecked = createBody.find('#customRadio').prop('checked');
            var accountType = "";

            if (isStudentChecked && !isInstructorChecked) {
                accountType = "students";
            }
            else if (!isStudentChecked && isInstructorChecked) {
                accountType = "instructors";
            }

            // Check if new account is valid
            var errorMessage = "";
            if(account.first_name.length == 0)
                errorMessage += "Empty First Name\n";
            if(account.first_name.length > 64)
                errorMessage += "First Name is too long\n";
            if(account.last_name.length == 0)
                errorMessage += "Empty Last Name\n";
            if(account.last_name.length > 64)
                errorMessage += "Last Name is too long\n";
            if(account.email.length == 0)
                errorMessage += "Empty Email\n";
            if(account.email.length > 128)
                errorMessage += "Email is too long\n";
            if(account.password.length == 0)
                errorMessage += "Empty Password\n";
            if(account.password.length > 128)
                errorMessage += "Password is too long\n";
            if(accountType == "")
                errorMessage += "Account type not selected\n";

                
            var onSuccess = function(data) {

               // Implement login, or redirect to new page
               if(accountType == "students"){
                //window.location.href = "../html/GetStudentInfo.html" + "?id=" + data.student.id.toString();
                window.location.replace("http://127.0.0.1:5000/api/studentProfile");

               
                }
                else{
                    window.location.href = "../html/GetInstructorInfo.html" + "?id=" + data.instructor.id.toString();
                }

                

                
            };
            

            var onFailure = function() { 
                console.error('create account '); 
            };

            if(errorMessage != "") {
                alert(errorMessage);
            }
            else
            {
                // Send account info to server
                makePostRequest('/api/' + accountType, account, onSuccess, onFailure);
            }

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
