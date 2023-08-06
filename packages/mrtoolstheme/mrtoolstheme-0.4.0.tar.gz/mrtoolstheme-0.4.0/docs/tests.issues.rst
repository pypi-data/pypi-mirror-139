======================
Test Cases from Issues
======================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Issues #1: ``code-block`` in ``admonition``
===========================================

:Link: https://gitlab.com/anatas_ch/pyl_mrtoolstheme/-/issues/1
:Fixed: 0.2.0

.. code-block:: rest
    :caption: Test Case

    .. Note:: Never use ``l``, ``O``, or ``I`` single letter names as these can be mistaken
              for ``1`` and ``0``, depending on typeface:

        .. code-block:: python
            :caption: Python

            O = 2    # This may look like you're trying to reassign 2 to zero

---------------------------------------------------------------------------------------------------------------

.. Note:: Never use ``l``, ``O``, or ``I`` single letter names as these can be mistaken for ``1`` and ``0``,
          depending on typeface:

          .. code-block:: python
              :caption: Python

              O = 2    # This may look like you're trying to reassign 2 to zero


Issues #2: Text as code formatted in ``code-block`` ``caption``
===============================================================

:Link: https://gitlab.com/anatas_ch/pyl_mrtoolstheme/-/issues/2
:Fixed: 0.3.0

.. code-block:: rest
    :caption: Test Case

    .. code-block:: json
       :caption: ``Some as code formated text`` and some normal text!

       {
           "testcase": "issues 2"
       }

---------------------------------------------------------------------------------------------------------------

.. code-block:: json
   :caption: ``Some as code formated text`` and some normal text!

   {
       "testcase": "issues 2"
   }
