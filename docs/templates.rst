Form Templates
==============

You can create your own form templates to use against any form in the system, providing a vast array of ways to
create, style and submit your forms.

The default `template <https://github.com/AccentDesign/wagtailstreamforms/blob/master/wagtailstreamforms/templates/streamforms/form_block.html>`_ used can be seen below:

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

.. note:: It is important here to keep the hidden fields the form will create an additional field for the form id.

Once you have created you own you will need to add it to the list of available templates. 

This is as simple as adding it to the ``WAGTAILSTREAMFORMS_FORM_TEMPLATES`` in settings:

.. code-block:: python

    # this is the defaults 

    WAGTAILSTREAMFORMS_FORM_TEMPLATES = (
        ('streamforms/form_block.html', 'Default Form Template'),
    )
