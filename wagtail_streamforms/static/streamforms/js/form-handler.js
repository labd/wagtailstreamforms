function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function showSuccess(form, message) {
    form.replaceWith('<p class=\'success-msg\'>' + message + '</p>');
}

function showFieldErrors(form, errors) {
    form.find('div.field-row').removeClass('has-error');
    form.find('p.error-msg').remove();
    for (var k in errors){
        var fields = form.find('[name="' + k + '"]');
        if (fields.length > 0) {
            var field = fields[0];
            $(field).closest('div.field-row').addClass('has-error');
            $(field).closest('div.field-row').append('<p class=\'error-msg\'>' + errors[k] + '</p>');
        }
    }
}

function resetCapcha() {
    if (typeof(grecaptcha) != "undefined") {
        grecaptcha.reset();
    }
}

$(document).on('submit', "form[id^='streamforms_']", function(e) {
    e.preventDefault();

    var $form = $(e.target);
    var action = $form.attr('action');
    var data = $form.serializeArray();

    $.post(action, data, function(data) {
        showSuccess($form, data.message);
        resetCapcha();
    }).fail(function(err) {
        showFieldErrors($form, err.responseJSON.detail);
        resetCapcha();
    });
});