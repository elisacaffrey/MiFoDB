Quick Start
===================
This workflow will walk you through the steps needed to go from getting your data back from a sequencing facility to having a profiled list of genomes with the mapped relative abundances.
As an example, we can use reads from a sample of pikliz, a Haitian ferment with cabbage, carrots, bell peppers and Scotch bonnet peppers, produced in Montana, USA.


Pre-processing
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Before being able to use the data, you will need to:

**1.** Perform QC metrics to get a sense of the sequencing quality 

**2.** Trim any sequencing adapters so that you are left with just reads from your original sample

**3.** Remove any potential contaminating human genomes (this is less of a problem with fermented foods, but a huge deal when collecting human stool samples packed with the donors DNA)

For step 1. we can use `FastQC <https://www.bioinformatics.babraham.ac.uk/projects/fastqc/>`_, which reports quality control checks on raw sequence data

For steps 2. and 3. we can use `BBTools <https://jgi.doe.gov/data-and-tools/software-tools/bbtools/>`_, a suite of tools used for DNA and RNA sequencing analysis.
We will be using two specific BBTools

`bbduk <https://jgi.doe.gov/data-and-tools/software-tools/bbtools/bb-tools-user-guide/bbduk-guide/>`_: for the trimming and filtering of adapters and contaminants in your reads

`repair <https://jgi.doe.gov/data-and-tools/software-tools/bbtools/bb-tools-user-guide/repair-guide/>`_: when starting with pair-end reads, to fix paired read files that became disordered

`bbmap <https://jgi.doe.gov/data-and-tools/software-tools/bbtools/bb-tools-user-guide/bbmap-guide/>`_: removed human reads

____________________________

**1.** Download the raw reads
::
 $  wget EBC_087_S160_L003_R1.fastq.gz
 $  wget EBC_087_S160_L003_R2.fastq.gz


Assembly
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
MegaHIT


Binning
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
MetaBAT2
EukRep

Profiling
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
InStrain


