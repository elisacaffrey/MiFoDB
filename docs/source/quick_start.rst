Quick Start
===================
This workflow will walk you through the steps needed to go from getting your data back from a sequencing facility to having a profiled list of genomes with the mapped relative abundances.
As an example, we can use reads from a sample of pikliz, a Haitian ferment with cabbage, carrots, bell peppers and Scotch bonnet peppers, produced in Montana, USA.


Pre-processing
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**Expected input: ** Raw paired end reads (ex. ending in R1.fastq.gz and R2.fastq.gz)
**Expected output: ** Trimmed paired end reads (ex. ending in _1.trim.fastq.gz and _2.trim.fastq.gz)

**1.** Download the raw reads
::
 $  wget EBC_087_S160_L003_R1.fastq.gz
 $  wget EBC_087_S160_L003_R2.fastq.gz

**2. Perform FastQC**
First, you will want to use `FastQC <https://www.bioinformatics.babraham.ac.uk/projects/fastqc/>`_ to perform quality control checks on raw sequence data.
We recommend setting up a conda environment:
::
 $  conda create -n fastqc_env python=3.8
 $  conda activate fastqc_env  

 $  conda install fastqc

Finally, create your ``output_directory`` and run fastqc on your reads:
 $  fastqc EBC_087_S160_L003_R1.fastq.gz EBC_087_S160_L003_R2.fastq.gz -o EBC_087_output_directory


A great FastQC tutorial is available here: https://genomicsaotearoa.github.io/metagenomics_summer_school/day1/ex2_quality_filtering/#loading-fastqc

**3. Perform BBTools**
Second, use BBTools to trim any sequencing adapters so that you are left with just reads from your original sample, and toemove any potential contaminating human genomes (this is less of a problem with fermented foods, but a huge deal when collecting human stool samples packed with the donors DNA) by using:

* `bbduk <https://jgi.doe.gov/data-and-tools/software-tools/bbtools/bb-tools-user-guide/bbduk-guide/>`_: for the trimming and filtering of adapters and contaminants in your reads

* `repair <https://jgi.doe.gov/data-and-tools/software-tools/bbtools/bb-tools-user-guide/repair-guide/>`_: when starting with pair-end reads, to fix paired read files that became disordered

* `bbmap <https://jgi.doe.gov/data-and-tools/software-tools/bbtools/bb-tools-user-guide/bbmap-guide/>`_: removed human reads

**#.** Save output to ``processed_reads`` directory

Profiling
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**Expected input: ** Trimmed pair-end reads (in your processed_reads directory. Should end in R1.fastq.gz and R2.fastq.gz)
**Expected output: ** .IS file output for each sample with genome profiling results




