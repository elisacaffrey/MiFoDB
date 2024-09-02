Quick Start
===================
Another way to work through this workflow is by using nextflow, a workflow management system. `Matt Olm <https://github.com/MrOlm/nf-genomeresolvedmetagenomics>`_ has developed a nextflow pipeline to perform genome resolved metagenomics, which includes all steps outlined in the `step-by-step <https://mifodb.readthedocs.io/en/latest/step_by_step.html>`_ guide. 

To run nextflow, you must first install `nextflow <https://www.nextflow.io/docs/latest/install.html#install-nextflow>`_, following the outlined instructions.
Instructions are also available `here <https://github.com/MrOlm/nf-genomeresolvedmetagenomics?tab=readme-ov-file#quick-start>`_.

We can use reads from a sample of pikliz, a Haitian ferment with cabbage, carrots, bell peppers and Scotch bonnet peppers, produced in Montana, USA.

Pre-processing with nextflow
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**1. Download your reads**

**2. Prepare your input file**: this will include 4 columns called sample, fastq_1, fastq_2, and single_end. In this case, single_end is left blank.

.. csv-table:: *basicInfo_v1.csv*

    sample,fastq_1,fastq_2,single_end
    EBC_087,/location/of/your/file/raw_reads/EBC_087_S160_L003_R1.fq.gz,/location/of/your/file/raw_reads/EBC_087_S160_L003_R2.fq.gz,
::

If you are pre-processing multiple files at once, you can add one sample to each line

**3. Run preprocessing:** Once nextflow is installed and the basicInfo.csv is pointing to the right location of the file, run:

::

$ nextflow run https://github.com/MrOlm/nf-genomeresolvedmetagenomics -entry PREPROCESSREADS --input basicInfo_v1.csv -with-report v1 --outdir results_v1/


Note:common errors include pointing to the incorrect location, or accidentally including additional empty lines in your .csv file. Additionally, depending on how the .csv file is, a byte order mark (BOM) might need to be removed before running. To do that, in your terminal in the directory with the basicInfo.csv file run:
::

$ vi -c ":set nobomb" -c ":wq" basicInfo_v1.csv

.. results::

    The resulting trimmed files, ending in .trim.fastq.gz will be in results_v1/fastp/*.trim.fastq.gz
    Read metrics will be included in results_v1/basicinfo/basic_info_final.csv

Profile with nextflow
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**1. Prepare your input file**: you will now make a new input file, pointing to the processed results your just generated. 


::
nextflow run /home/mattolm/user_data/Nextflow/nf-core-genomeresolvedmetagenomics/main.nf -entry PROFILE --input 08202024_processingInfo_v2.csv -with-report report.html --outdir results_prok_v1 --fasta s3://sonn-highavail/databases/MiFoDB/MiFoDB_beta/MiFoDB_beta_v3/MiFoDB_beta_v3_prok.fasta --stb_file s3://sonn-highavail/databases/MiFoDB/MiFoDB_beta/MiFoDB_beta_v3/MiFoDB_beta_v3_prok.stb --genes_file s3://sonn-highavail/databases/MiFoDB/MiFoDB_beta/MiFoDB_beta_v3/MiFoDB_beta_v3_prok.genes.fna --instrain_profile_args " --database_mode --skip_plot_generation"

Then, run with new euk database:
nextflow run /home/mattolm/user_data/Nextflow/nf-core-genomeresolvedmetagenomics/main.nf -entry PROFILE --input 08202024_processingInfo_v2.csv -with-report report_euk.html --outdir results_euk_v1 --fasta s3://sonn-highavail/databases/MiFoDB/MiFoDB_beta/MiFoDB_beta_v3/MiFoDB_beta_vhm_v3_euk.fasta --stb_file s3://sonn-highavail/databases/MiFoDB/MiFoDB_beta/MiFoDB_beta_v3/MiFoDB_beta_vhm_v3_euk.stb --instrain_profile_args " --database_mode --skip_plot_generation"

And finally run with new substrate bd:
nextflow run https://github.com/MrOlm/nf-genomeresolvedmetagenomics -entry PROFILE --input 08202024_processingInfo_v2.csv -with-report report_sub_v1.html --outdir results_sub_v1 --fasta s3://sonn-highavail/databases/FeFoDB/substrate_genomes.fasta --stb_file s3://sonn-highavail/databases/FeFoDB/substrate_genomes.stb --instrain_profile_args " --database_mode --skip_plot_generation" --coverm
