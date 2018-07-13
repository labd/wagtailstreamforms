Templates
=========

You can create your own form templates to use against any form in the system, providing a vast array of ways to
create, style and submit your forms.

The default template located at ``streamforms/form_block.html`` can be seen below:

.. literalinclude:: ../wagtailstreamforms/templates/streamforms/form_block.html

.. note:: It is important here to keep the hidden fields as the form will have some in order to process correctly.

Once you have created you own you will need to add it to the list of available templates within the form builder. 
This is as simple as adding it to the ``WAGTAILSTREAMFORMS_FORM_TEMPLATES`` in settings as below.

.. code-block:: python

    # this includes the default template in the package and an additional custom template. 

    WAGTAILSTREAMFORMS_FORM_TEMPLATES = (
        ('streamforms/form_block.html', 'Default Form Template'),  # default
        ('app/custom_form_template.html', 'Custom Form Template'),
    )

You are not required to use the default template, its only there as a guideline to what is required and provide a fully working 
package out of the box. If you dont want it just remove it from the ``WAGTAILSTREAMFORMS_FORM_TEMPLATES`` setting.

Rendering your StreamField
--------------------------

It is important to ensure the request is in the context of your page to do this iterate over your StreamField block using
wagtails ``include_block`` template tag.

.. code-block:: python

    {% load wagtailcore_tags %}

    {% for block in page.body %}
        {% include_block block %}
    {% endfor %}

DO NOT use the short form method of ``{{ block }}`` as described `here <http://docs.wagtail.io/en/latest/topics/streamfield.html#template-rendering>`_
as you will get CSRF verification failures.

Deleted forms
-------------

In the event of a form being deleted which is still in use in a streamfield the following template will be rendered
in its place:

``streamforms/non_existent_form.html``

.. literalinclude:: ../wagtailstreamforms/templates/streamforms/non_existent_form.html

You can override this by putting a copy of the template in you own project using the same 
path under a templates directory ie ``app/templates/streamforms/non_existent_form.html``. As long as the app is before
``wagtailstreamforms`` in ``INSTALLED_APPS`` it will use your template instead.

Messaging
---------

When the ``success`` or ``error`` message options are completed in the form builder and upon submission of the form
a message is sent to django's messaging framework.

You will need to add ``django.contrib.messages`` to your ``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django.contrib.messages'
        ...
    ]


To display these in your site you will need to include somewhere in your page's markup a snippet
similar to the following:

::

    {% if messages %}
    <ul class="messages">
        {% for message in messages %}
        <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
        {% endfor %}
    </ul>
    {% endif %}

Any message from the form will then be displayed.
