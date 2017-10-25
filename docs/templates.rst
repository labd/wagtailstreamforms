Form Templates
==============

You can create your own form templates to use against any form in the system, providing a vast array of ways to
create, style and submit your forms.

The default template located at ``streamforms/form_block.html`` can be seen below:

.. code-block:: html

    <h2>{{ value.form.name }}</h2>
    <form action="{{ value.form_action }}" method="post" novalidate>
        {% csrf_token %}
        {% for hidden in form.hidden_fields %}{{ hidden }}{% endfor %}
        {% for field in form.visible_fields %}
            {% include 'streamforms/partials/form_field.html' %}
        {% endfor %}
        <input type="submit" value="{{ value.form.submit_button_text }}">
    </form>

.. note:: It is important here to keep the hidden fields as the form will have some in order to process correctly.

Once you have created you own you will need to add it to the list of available templates. 

This is as simple as adding it to the ``WAGTAILSTREAMFORMS_FORM_TEMPLATES`` in settings:

.. code-block:: python

    # this is the defaults 

    WAGTAILSTREAMFORMS_FORM_TEMPLATES = (
        ('streamforms/form_block.html', 'Default Form Template'),
    )

Deleted forms
-------------

In the event of a form being deleted which is still in use in a streamfield the following template will be rendered
in its place:

``streamforms/non_existent_form.html``

.. code-block:: html

    <p>Sorry, this form has been deleted.</p>

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
