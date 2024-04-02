Quick Start
===================
This workflow will walk you through the steps needed to go from getting your data back from a sequencing facility to having a profiled list of genomes.
Once the profiles are preprocessed, you will be able to choose whether to run them against the prokaryote database, eukaryote database, substrate database, or all three and then combine the results.
As an example, we can use reads from a sample of pikliz, a Haitian ferment with cabbage, carrots, bell peppers and Scotch bonnet peppers, produced in Montana, USA.


Pre-processing
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Expected input:** Raw paired end reads (ex. ending in R1.fastq.gz and R2.fastq.gz)

**Expected output:** Trimmed paired end reads (ex. ending in _1.trim.fastq.gz and _2.trim.fastq.gz)

**1. Download the example raw reads**
::

 $  wget -P Data http://sra-download.ncbi.nlm.nih.gov/srapub/SRR28502160

**2. Perform FastQC**

Use `FastQC <https://www.bioinformatics.babraham.ac.uk/projects/fastqc/>`_ to perform quality control checks on raw sequence data.
We recommend setting up a conda environment:
::

 $  conda create -n preprocess_env python=3.8
 $  conda activate preprocess_env  

 $  conda install fastqc

Finally, create your ``output_directory`` and run fastqc on your reads:
::

 $  fastqc EBC_087_S160_L003_R1.fastq.gz EBC_087_S160_L003_R2.fastq.gz -o EBC_087_output_directory

*this process should take ~5-7min/sample*

The output for this step includes .html files with QC information for each read, and .fastqc.zip files with basic sequencing statistics.

For more FastQC information, visit their `website <https://www.bioinformatics.babraham.ac.uk/projects/fastqc/>`_.

**3. Perform BBTools**

Use BBTools to trim any sequencing adapters so that you are left with just reads from your original sample and remove any potential contaminating human genomes (this is less of a problem with fermented foods, but a huge deal when collecting human stool samples packed with the donors DNA) by using:

* `bbduk <https://jgi.doe.gov/data-and-tools/software-tools/bbtools/bb-tools-user-guide/bbduk-guide/>`_: for the trimming and filtering of adapters and contaminants in your reads

* `repair <https://jgi.doe.gov/data-and-tools/software-tools/bbtools/bb-tools-user-guide/repair-guide/>`_: when starting with pair-end reads, to fix paired read files that became disordered

* `bbmap <https://jgi.doe.gov/data-and-tools/software-tools/bbtools/bb-tools-user-guide/bbmap-guide/>`_: removed human reads

First, install BBtools following instructions on their `installation guide <https://jgi.doe.gov/data-and-tools/software-tools/bbtools/bb-tools-user-guide/installation-guide/>`_. Make sure to make bbmap executable by adding the path to your ~/.bashrc.

Next, run:
::

 $  bbduk.sh in1=EBC_087_S160_L003_R1.fastq.gz in2=EBC_087_S160_L003_R2.fastq.gz out1=EBC_087_bbduk_1.fastq.gz out2=EBC_087_bbduk_2.fastq.gz ref=$ADAPTERS ktrim=r k=23 mink=11 hdist=1 tpe tbo &> EBC_087.bbduk.log

 $  repair.sh in=EBC_087_bbduk_1.fastq.gz in2=EBC_087_bbduk_2.fastq.gz out=EBC_087_repair_1.fastq.gz out2=EBC_087_repair_2.fastq.gz

Finally, prepare the human reference genome, and then run bbmap:
::

 $  bbmap.sh ref=hg38.fa
 $  bbmap.sh in=EBC_087_repair_1.fastq.gz in2=EBC_087_repair_2.fastq.gz out=EBC_087_trim_1.fastq.gz out2=EBC_087_trim_2.fastq.gz ref=hg38.fa nodisk

**4.** Save output to ``processed_reads`` directory

Profiling
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**Expected input:** Trimmed pair-end reads (in your processed_reads directory. Should end in R1.fastq.gz and R2.fastq.gz)

**Expected output:** .IS file output for each sample with genome profiling results

**1. Set up your environment**
::

 $  mamba create -n instrain_env -c bioconda instrain
 $  conda activate instrain_env

Install instrain
::

 $  pip install instrain

Install samtools to create your .bam file from the reference .fasta
::

 $  conda install -c bioconda bowtie2 samtools

For more information on installation, visit `inStrain <https://instrain.readthedocs.io/en/latest/installation.html>`_ or Bowtie2 `<https://bowtie-bio.sourceforge.net/bowtie2/manual.shtml>`_

**2. Download the reference databases**

For each database (prokaryote, eukaryote, or substrate), download the .fasta and .stb file.

*for prokaryote, make sure to also download the .genes file*

**3. Make your .bam file**

You only have to do this once for each database version. Make sure to always use the .bam file made from the same version of the database .fasta file.
::

 $  bowtie2-build MiFoDB_beta_v2_prok.fasta MiFoDB_prok_v2_index
 $  bowtie2 -x MiFoDB_prok_v2_index -1 EBC_087_S160_L003_R1.fastq.gz -2 EBC_087_S160_L003_R2.fastq.gz -S EBC_087_aligned_reads.sam

Finally, you will need to convert the SAM file to a BAM file and index the sorted BAM
::

 $  samtools view -Sb EBC_087_aligned_reads.sam > EBC_087_aligned_reads.bam
 $  samtools sort EBC_087_aligned_reads.bam -o EBC_087_sort_aligned_reads.bam
 $  samtools index EBC_087_sort_aligned_reads.bam
 $  bowtie2 -p 10 -x MiFoDB_prok_v2_index -1 EBC_087_S160_L003_R1.fastq.gz -2 EBC_087_S160_L003_R2.fastq.gz -S EBC_087_aligned_reads.sam)  2>bowtie2.EBC_087.log

**3. Run inStrain**

Now that you have your .bam, .fasta, .stb files and inStrain installed, you can run inStrain profile
::

 $  inStrain profile EBC_087_sort_aligned_reads.bam MiFoDB_beta_v2_prok.fasta -o EBC_087.IS -p 6 -g genesfile.fasta --stb_file MiFoDB_beta_v2_prok.stb --genes_file MiFoDB_beta_v2_prok.genes.fna --instrain_profile_args --database_mode

The output will be a .IS file, with a number of .tsv file. We will be most interested in genome_info.tsv (example below), which includes all mapping information. For interpretation and analysis, see `example output <https://mifodb.readthedocs.io/en/latest/example_output.html>`_.

.. csv-table:: genome_info.tsv

genome,coverage,breadth,nucl_diversity,length,true_scaffolds,detected_scaffolds,coverage_median,coverage_std,coverage_SEM,breadth_minCov,breadth_expected,nucl_diversity_rarefied,conANI_reference,popANI_reference,iRep,iRep_GC_corrected,linked_SNV_count,SNV_distance_mean,r2_mean,d_prime_mean,consensus_divergent_sites,population_divergent_sites,SNS_count,SNV_count,filtered_read_pair_count,reads_unfiltered_pairs,reads_mean_PID,reads_unfiltered_reads,divergent_site_count
   C-03.Ssa-BR.fna,1.686020547,0.049164091,0.004595774,1896140,182,86,0,69.19478668,0.050739639,0.011300326,0.774346839,0.000140703,0.986372334,o.988145797,,FALSE,242,39.69008264,0.951699521,0.999845137,292,254,252,165,15171,15417,0.981642137,36199,417 
 EBC_086.5.fna,1.596317454,0.049848898,0.006035971,2377866,79,52,0,19.94120243,0.012974942,0.028909535,0.755746415,0.002048653,0.979081506,0.984682077,,FALSE,1337,56.69334331,0.637899652,0.9941014,1438,1053,1040,825,17829,19210,0.969968582,48221,1865
 FS03_2016_noduplicates_bin.6.fna,1.191514863,0.041940437,0.004574618,2543035,344,186,0,21.96261861,0.013962518,0.008234649,0.650799011,0.001974379,0.966286233,0.96981997,,FALSE,393,68.18320611,0.596979301,0.989440015,706,632,628,185,14188,15687,0.965486302,39649,813
 FS47_2017_noduplicates_bin.5.fna,1.907346578,0.52567291,0.001377854,1594307,35,35,1,2.642570054,0.002097472,0.150077745,0.814404746,0,0.984235383,0.984339867,,FALSE,,,,,3772,3747,3743,181,13496,13639,0.978569696,31713,3924
