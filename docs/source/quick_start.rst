Quick Start
===================
Another way to work through this workflow is by using nextflow, a workflow management system. `Matt Olm <https://github.com/MrOlm/nf-genomeresolvedmetagenomics>`_ has developed a nextflow pipeline to perform genome resolved metagenomics, which includes all steps outlined in `Quick Start <. In order to run nextflow, you must first install `nextflow <https://www.nextflow.io/docs/latest/install.html#install-nextflow>`_, following the outlined instructions.

This workflow will walk you through the steps needed to go from getting your data back from a sequencing facility to having a profiled list of genomes.
Once the profiles are preprocessed, you will be able to choose whether to run them against the prokaryote database, eukaryote database, substrate database, or all three and then combine the results.

As an example, we can use reads from a sample of pikliz, a Haitian ferment with cabbage, carrots, bell peppers and Scotch bonnet peppers, produced in Montana, USA.

Pre-processing *STEP-BY-STEP*
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



Pre-processing *SHORTCUT*
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
If instead of performing each step you want to only run one command, you can always use nextflow, 
::

$ nextflow run https://github.com/MrOlm/nf-genomeresolvedmetagenomics -entry PREPROCESSREADS --input 08202024_basicInfo_v1.csv -with-report v1 --outdir results_v1/
