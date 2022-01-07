from wagtailstreamforms.models import Form


def get_form_instance_from_request(request):
    """Get the form class from the request."""

    form_id = request.POST.get("form_id")
    if form_id and form_id.isdigit():
        try:
            return Form.objects.get(pk=int(form_id))
        except Form.DoesNotExist:
            pass
    return None
