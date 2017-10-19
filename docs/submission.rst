Form Submission
===============

Form submissions are handled by the means of a wagtail ``before_serve_page`` hook. The built in hook at
``wagtailstreamforms.wagtail_hooks.process_form`` looks for a form in the post request,
and either processes it redirecting back to the current page or just renders the page with
any validation errors if there are any.

If no form was posted then the page serves in the usual manner.

.. note:: Currently the hook expects the form to be posting to the same page it exists on.

Providing your own submission method
------------------------------------

If you do not want the current hook to be used you need to disable it by setting the
``WAGTAILSTREAMFORMS_ENABLE_FORM_PROCESSING`` to ``False`` in your settings:

.. code-block:: python

    WAGTAILSTREAMFORMS_ADMIN_MENU_LABEL = False

With this set no forms will be processed of any kind and you are free to process them how you feel fit.

* Your own hook
* A page mixin
* A view in django

An example of a hook:

.. code-block:: python

    from django.contrib import messages
    from django.shortcuts import redirect
    from django.template.response import TemplateResponse

    from wagtail.wagtailcore import hooks
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

                    # redirect to current page - this will avoid refreshing and submitting again
                    return redirect(page.get_url(request), context=context)

                else:
                    # update the context with the invalid form and serve the page
                    # IMPORTANT you must set these so that the when the form in the streamfield is
                    # rendered it knows that it is the form that is invalid
                    context.update({
                        'invalid_stream_form_reference': form.data.get('form_reference'),
                        'invalid_stream_form': form
                    })

                    return TemplateResponse(
                        request,
                        page.get_template(request, *args, **kwargs),
                        context
                    )
