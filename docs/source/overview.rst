Overview
===================

The MiFoDB Workflow
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. figure:: GitHub.png
  :width: 400px
  :align: center
``The above figure shows a visual representation of the MiFoDB workflow, including pre-processing, assembly, binning, and alignment-based profiling.``


Glossary & FAQ
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Glossary of terms used in MiFoDB
------------------------------------

.. note::
  This glossary is meant to give a conceptual overview of the terms used in MiFoDB. For a more detailed overview of these concepts, see the `InStrain Glossary <https://instrain.readthedocs.io/en/latest/overview.html#glossary-faq>`_.

.. glossary::
ANI
  Average nucleotide identity

scaffold-to-bin file
  A .txt file with two columns where the first column is the scaffold name and the second column is the name of the genome the scaffold belongs to.
  Can be created using the script `parse_stb.py <https://github.com/MrOlm/drep/blob/master/helper_scripts/parse_stb.py>`_ that comes with the program
  ``dRep``  See :doc:`example_output` for more info

FAQ
------------------------------------
*Why use alignment-based profiling?*
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


*What an I do with MiFoDB results?*
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

*Why do I not have <100% samples mapped?*
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
