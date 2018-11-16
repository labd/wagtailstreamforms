Submission Methods
==================

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

.. literalinclude:: ../wagtailstreamforms/wagtail_hooks.py
   :pyobject: process_form

Supporting ajax requests
~~~~~~~~~~~~~~~~~~~~~~~~

The only addition here from the basic example is just the  ``if request.is_ajax:`` and the ``JsonResponse`` parts.

We are just making it respond with this if the request was ajax.

.. code-block:: python

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

                    # insert code to serve page if not ajax (as original)

                else:
                    # if the request is_ajax then return an error message and the form errors
                    if request.is_ajax():
                        return JsonResponse({
                            'message': form_def.error_message or 'error',
                            'errors': form.errors
                        })

                    # insert code to serve page if not ajax (as original)

Add some javascript somewhere to process the form via ajax:

::

    <form id="id_streamforms_{{ form.initial.form_reference }}">...</form>

    <script>
        $("#id_streamforms_{{ form.initial.form_reference }}").submit(function(e) {
          e.preventDefault();
          var data = new FormData($(this).get(0));
          $.ajax({
              type: "POST",
              url: ".",
              data: data,
              processData: false,
              contentType: false,
              success: function(data) {
                  // do something with data
                  console.log(data);
              },
              error: function(data) {
                  // do something with data
                  console.log(data);
              }
          });
        });
    </script>