Form Submission Methods
=======================

Form submissions are handled by the means of a wagtail ``before_serve_page`` hook. The built in hook at
``wagtailstreamforms.wagtail_hooks.process_form`` looks for a form in the post request,
and either:

* processes it redirecting back to the current page or defined page in the form setup.
* or renders the current page with any validation error.

If no form was posted then the page serves in the usual manner.

.. note:: Currently the hook expects the form to be posting to the same page it exists on.

.. _rst_provide_own_submission:

Providing your own submission method
------------------------------------

If you do not want the current hook to be used you need to disable it by setting the
``WAGTAILSTREAMFORMS_ENABLE_FORM_PROCESSING`` to ``False`` in your settings:

.. code-block:: python

    WAGTAILSTREAMFORMS_ENABLE_FORM_PROCESSING = False

With this set no forms will be processed of any kind and you are free to process them how you feel fit.

A basic hook example
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from django.contrib import messages
    from django.shortcuts import redirect
    from django.template.response import TemplateResponse

    from wagtail.core import hooks
    from wagtailstreamforms.utils import get_form_instance_from_request


    @hooks.register('before_serve_page')
    def process_form(page, request, *args, **kwargs):
        """ Process the form if there is one, if not just continue. """

        if request.method == 'POST':
            form_def = get_form_instance_from_request(request)

            if form_def:
                form = form_def.get_form(request.POST, request.FILES, page=page, user=request.user)
                context = page.get_context(request, *args, **kwargs)

                if form.is_valid():
                    # process the form submission
                    form_def.process_form_submission(form)

                    # create success message
                    if form_def.success_message:
                        messages.success(request, form_def.success_message, fail_silently=True)

                    # redirect to the page defined in the form
                    # or the current page as a fallback - this will avoid refreshing and submitting again
                    redirect_page = form_def.post_redirect_page or page

                    return redirect(redirect_page.get_url(request), context=context)

                else:
                    # update the context with the invalid form and serve the page
                    # IMPORTANT you must set these so that the when the form in the streamfield is
                    # rendered it knows that it is the form that is invalid
                    context.update({
                        'invalid_stream_form_reference': form.data.get('form_reference'),
                        'invalid_stream_form': form
                    })

                    # create error message
                    if form_def.error_message:
                        messages.error(request, form_def.error_message, fail_silently=True)

                    return TemplateResponse(
                        request,
                        page.get_template(request, *args, **kwargs),
                        context
                    )

Supporting ajax requests
~~~~~~~~~~~~~~~~~~~~~~~~

The only addition here from the basic example is just the  ``if request.is_ajax:`` and the ``JsonResponse`` parts.

We are just making it respond with this if the request was ajax.

.. code-block:: python

    from django.contrib import messages
    from django.http import JsonResponse
    from django.shortcuts import redirect
    from django.template.response import TemplateResponse

    from wagtail.core import hooks
    from wagtailstreamforms.utils import get_form_instance_from_request


    @hooks.register('before_serve_page')
    def process_form(page, request, *args, **kwargs):
        """ Process the form if there is one, if not just continue. """

        if request.method == 'POST':
            form_def = get_form_instance_from_request(request)

            if form_def:
                form = form_def.get_form(request.POST, request.FILES, page=page, user=request.user)
                context = page.get_context(request, *args, **kwargs)

                if form.is_valid():
                    # process the form submission
                    form_def.process_form_submission(form)

                    # if the request is_ajax then just return a success message
                    if request.is_ajax():
                        return JsonResponse({'message': form_def.success_message or 'success'})

                    # create success message
                    if form_def.success_message:
                        messages.success(request, form_def.success_message, fail_silently=True)

                    # redirect to the page defined in the form
                    # or the current page as a fallback - this will avoid refreshing and submitting again
                    redirect_page = form_def.post_redirect_page or page

                    return redirect(redirect_page.get_url(request), context=context)

                else:
                    # if the request is_ajax then return an error message and the form errors
                    if request.is_ajax():
                        return JsonResponse({
                            'message': form_def.error_message or 'error',
                            'errors': form.errors
                        })

                    # update the context with the invalid form and serve the page
                    # IMPORTANT you must set these so that the when the form in the streamfield is
                    # rendered it knows that it is the form that is invalid
                    context.update({
                        'invalid_stream_form_reference': form.data.get('form_reference'),
                        'invalid_stream_form': form
                    })

                    # create error message
                    if form_def.error_message:
                        messages.error(request, form_def.error_message, fail_silently=True)

                    return TemplateResponse(
                        request,
                        page.get_template(request, *args, **kwargs),
                        context
                    )

The template for the form might look like:

::

    <h2>{{ value.form.title }}</h2>
    <form action="{{ value.form_action }}" method="post" id="id_streamforms_{{ form.initial.form_id }}" novalidate>
        {% csrf_token %}
        {% for hidden in form.hidden_fields %}{{ hidden }}{% endfor %}
        {% for field in form.visible_fields %}
            {% include 'streamforms/partials/form_field.html' %}
        {% endfor %}
        <input type="submit" value="{{ value.form.submit_button_text }}">
    </form>
    <script>
        $("#id_streamforms_{{ form.initial.form_id }}").submit(function(e) {
            $.ajax({
                type: "POST",
                url: ".",
                data: $(this).serialize(),
                success: function(data) {
                    // do something with data
                    console.log(data);
                },
                error: function(data) {
                    // do something with data
                    console.log(data);
                }
            });
            e.preventDefault();
        });
    </script>