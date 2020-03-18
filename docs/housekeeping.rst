Housekeeping
============

Removing old form submissions
-----------------------------

There is a management command you can use to remove submissions that are older than the
supplied number of days to keep.

.. code-block:: bash

    python manage.py prunesubmissions 30

Where ``30`` is the number of days to keep before today. Passing ``0`` will keep today's submissions only.

Or to run the command from code:

.. code-block:: python

    from django.core.management import call_command

    call_command('prunesubmissions', 30)
