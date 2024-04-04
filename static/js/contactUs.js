$(document).on('submit', '#contact-form', function (e) {
    e.preventDefault();
    console.log("Submitted ...");

    let full_name = $("#full_name").val();
    let email = $("#email").val();
    let phone = $("#phone").val();
    let subject = $("#subject").val();
    let message = $("#message").val();

    // Get CSRF token value
    let csrfToken = $("input[name=csrfmiddlewaretoken]").val();

    let data = {
        'full_name': full_name,
        'email': email,
        'phone': phone,
        'subject': subject,
        'message': message,
        'csrfmiddlewaretoken': csrfToken, // Include CSRF token in the data
    }

    $.ajax({
        type: "POST",
        url: "/ajax_contact_form",
        data: data,
        dataType: "json",

        beforeSend: function (data) {
            console.log("Sending data to server...");
        },

        success: function (response) {
            console.log("Sent data to server...");
            console.log(response.data.message);
            $("#contact-form").hide();
            $("#iframe").hide();
            $("#message_response_container").removeClass("hidden");
            $("#message_response").html(response.data.message);
        }
    });

})