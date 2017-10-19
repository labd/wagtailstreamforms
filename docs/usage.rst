Basic Usage
===========

Just add the ``wagtailstreamforms.blocks.WagtailFormBlock()`` in any of your streamfields:

.. code-block:: python

    body = StreamField([
        ...
        ('form', WagtailFormBlock())
        ...
    ])

And you are ready to go.