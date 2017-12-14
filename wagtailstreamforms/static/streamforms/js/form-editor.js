/**
 * taken from wagtailadmin/js/page-editor.js
 *
 * TODO: one day change name for title in form model then we can delete this file
 */

$(function() {
    var slugFollowsTitle = false;

    $('#id_name').on('focus', function() {
        /* slug should only follow the title field if its value matched the title's value at the time of focus */
        var currentSlug = $('#id_slug').val();
        var slugifiedTitle = cleanForSlug(this.value, true);
        slugFollowsTitle = (currentSlug == slugifiedTitle);
    });

    $('#id_name').on('keyup keydown keypress blur', function() {
        if (slugFollowsTitle) {
            var slugifiedTitle = cleanForSlug(this.value, true);
            $('#id_slug').val(slugifiedTitle);
        }
    });
});