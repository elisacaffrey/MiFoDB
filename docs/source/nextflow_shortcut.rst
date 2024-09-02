


Pre-processing *SHORTCUT*
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
If instead of performing each step you want to only run one command, you can always use nextflow, a workflow management system. Matt Olm has developed a nextflow pipeline to perform genome resolved metagenomics, which includes all steps outlined above. In order to run nextflow
::

$ nextflow run https://github.com/MrOlm/nf-genomeresolvedmetagenomics -entry PREPROCESSREADS --input 08202024_basicInfo_v1.csv -with-report v1 --outdir results_v1/
