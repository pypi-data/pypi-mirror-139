======================
Test Cases Admonitions
======================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Specific Admonitions
====================

.. rst:directive:: attention

.. attention::
   Text

.. rst:directive:: caution

.. caution::
   Text

.. rst:directive:: danger

.. danger::
   Text

.. rst:directive:: error

.. error::
   Text

.. rst:directive:: hint

.. hint::
   Text

.. rst:directive:: important

.. important::
   Text

.. rst:directive:: note

.. note::
   Text

.. rst:directive:: tip

.. tip::
   Text

.. rst:directive:: warning

.. warning::
   Text

.. rst:directive:: seealso

.. seealso::
   Text

---------------------------------------------------------------------------------------------------------------

.. note:: This is a note admonition.
   This is the second line of the first paragraph.

   - The note contains all indented body elements
     following.
   - It includes this bullet list.

.. attention::
   Text

   .. caution::
      Text

      .. warning::
         Text

         .. note::
            Text

            .. important::
               Text

               .. error::
                  Text

                  .. note::
                     Text

                     .. admonition:: Eine Titel

                        Text

                        .. caution::
                           Text


Generic Admonition
==================

.. rst:directive:: .. admonition:: Title

.. admonition:: Title

   Text

---------------------------------------------------------------------------------------------------------------

.. admonition:: Title *with* inline **formats** and ``code``.

   Text

.. admonition:: With a very very very very very very very very very long long long long long long long long long long long long long long long long long long long title

   Text

---------------------------------------------------------------------------------------------------------------

Specific combinations
=====================

.. note::

   Text

   what
      Definition lists associate a term with a definition.

   *how*
      The term is a one-line phrase, and the definition is one or more
      paragraphs or body elements, indented relative to the term.
      Blank lines are not allowed between term and definition.

   Text

.. note::

   Text

   #. list entry I

   #. list entry II

.. tip::

   Text::

    if literal_block:
        text = 'is left as-is'
        spaces_and_linebreaks = 'are preserved'
        markup_processing = None
