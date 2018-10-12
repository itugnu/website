function submitLang() {
  document.getElementById("languageForm").submit();
}

$(document).ready(
    $('#contactForm').submit(function (event) {
        event.preventDefault();
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        // Disable send button
        var send_button = $('#sendMessageButton');
        send_button.prop("disabled", true);
        // Get form values
        var name = $("input#name").val();
        var email = $("input#email").val();
        var phone = $("input#phone").val();
        var message = $("textarea#message").val();
        // Send data
        $.ajax({
            url: "/contact/",
            type: "POST",
            dataType: "json",
            data: {
              "name": name,
              "phone": phone,
              "email": email,
              "message": message
            },
            cache: false,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function() {
                var result_box = $('#success');
                result_box.html("<div class='alert alert-success'>");
                result_box.find('> .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;").append("</button>");
                result_box.find('> .alert-success').append("<strong>Your message has been sent. </strong>");
                result_box.find('> .alert-success').append('</div>');
                $('#contactForm').trigger("reset");
            },
            error: function(data) {
                var response = $.parseJSON(data.responseText).message;
                var result_box = $('#success');
                result_box.html("<div class='alert alert-danger'>");
                result_box.find('> .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;").append("</button>");
                result_box.find('> .alert-danger').append($("<strong>").text(response));
                result_box.find('> .alert-danger').append('</div>');
                $('#contactForm').trigger("reset");
            },
            complete: function() {
                // Enable send button again
                setTimeout(function() {
                    send_button.prop("disabled", false);
                }, 1000);
            }
        });
    })
);
$(document).ready(
  $('input#name').focus(function() {
    $('#success').html('');
  })
);
$(document).ready(
    $('.lecture-register-button').on("click", function (e) {
        e.preventDefault();
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $(this).prop("disabled", true);
        var result_box = $($(this).data("result-box"));
        var lecture = $(this).data("lecture");
        // Send data
        $.ajax({
            url: "/lecture/register/",
            type: "POST",
            dataType: "json",
            data: {
              "lecture": lecture
            },
            cache: false,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(data) {
                var response = data;
                result_box.html("<div class='alert alert-success'>");
                result_box.find('> .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;").append("</button>");
                if (response.code === 'external_form') {
                    var registration_anchor = "<a href='" + response.url + "' target='_blank'>" + response.message + "</a>";
                    result_box.find('> .alert-success').append(registration_anchor);
                    setTimeout(function() {
                        window.location.href = response.url;
                        }, 3000
                    );
                } else {
                    result_box.find('> .alert-success').append($("<strong>").text(response.message));
                }
                result_box.find('> .alert-success').append('</div>');
            },
            error: function(data) {
                var response = $.parseJSON(data.responseText);
                result_box.html("<div class='alert alert-danger'>");
                result_box.find('> .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;").append("</button>");
                result_box.find('> .alert-danger').append($("<strong>").text(response.message));
                if (response.code === 'duplicate_registration_with_external_form') {
                  var registration_anchor = "<a href='" + response.url + "' target='_blank'>" + GLOBAL_DJANGO_VARS.external_form + "</a>";
                  result_box.find('> .alert-danger').append(registration_anchor);
                }
                result_box.find('> .alert-danger').append('</div>');
                if (response.code === 'login_required') {
                    setTimeout(function() {
                        window.location.href = GLOBAL_DJANGO_VARS.login_url;
                        }, 1000
                    );
                }
            }
        });
        return false;
    })
);
