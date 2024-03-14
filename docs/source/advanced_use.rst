Advanced Use
============

Creating a custom MiFoDB
------------------------------
While the latest version of MiFoDB (`MiFoDB_beta_v2 <https://docs.google.com/spreadsheets/d/1PHRlb9YwKiwpVk8ChozBZbFYCA-VL3EXJTIPI-TI04A/edit?usp=sharing>`_)  includes 675 genomes (586 prokaryote, 82 eukaryote, and 7 substrate genomes), there will be a number of cases in which you might want to add custom genomes. 

There are a few recommended ways of doing this, depending on genome type. 

1. Identifying genomes of interest to add to MiFoDB
++++++++++++++++++++++++++++++++++++++++++++++++++++++
Identification of unmapped prokaryote genomes missing from the database can easily be done using `sylph <https://github.com/bluenote-1577/sylph>`_, an ultrafast metagenomic profiler for metagenomic shotgun samples based on a pre-sketched GTDB r214 database. GTDB (`Genome Taxonomic Database <https://gtdb.ecogenomic.org/>`_) is a database which uses RefSeq and GenBank genomes to standardize microbial taxonomy, while incorporating independent quality control checks. For more information about GTDB, `see their website <https://gtdb.ecogenomic.org/about>`_. 

The sylph output returns a list of identified microbes and their abundance. Comparing the sylph output to the MiFoDB output will allow for the identification of microbes not included in the current MiFoDB database. In addition, for ease of use we recommend filtering sylph results to only incorporate microbes with a reported abundance >1% and/or reported presence in more than one sample.

Details on the use of sylph can be found on their page `Taxonomic profiling with the GTDB‐R214 database <https://github.com/bluenote-1577/sylph/wiki/Taxonomic-profiling-with-the-GTDB%E2%80%90R214-database>`_, summarized here:

**1. We recommend create a sylph environment using** 
::

  $  conda create -n sylph_env python=3.8
  $  conda activate sylph_env

Select a database (see sylph documentation for appropriate selection)
::
 $  wget https://storage.googleapis.com/sylph-stuff/v0.3-c1000-gtdb-r214.syldb -O gtdb_database_c1000.syldb
 $  wget https://storage.googleapis.com/sylph-stuff/v0.3-c200-gtdb-r214.syldb -O gtdb_database_c200.syldb

For questions about sylph, contact the sylph authors. 

**2. Prepare the sylph sketch of your genome**
::
 $  sylph sketch -1 EBC_087_1.trim.fastq.gz -2 EBC_087_2.trim.fastq.gz

**3. Finally, use sylph to profile**
::
 $  sylph profile gtdb_database_c200.syldb *.sylsp -t 10 > EBC_087_sylphprofile.tsv

You can now identify any microbes that are not in MiFoDB that you might be interested in adding to a custom database.



1. Adding prokaryote genomes to your custom database
++++++++++++++++++++++++++++++++++++++++++++++++++++++

Once you have identified your genomes of interest:

**1. Download reference genomes from NCBI**

**2. Run dRep on all genomes**: In order to prevent the inclusion of genomes with >95% ANI or with low completeness and high contamination which might confound your results, you will want to make sure you only include one representative genome for each species. 

Download all representative prokaryote genomes used in the final MiFoDB here. Then download any genomes of interest and add them to the directory. Finally, run `dRep <https://drep.readthedocs.io/en/latest/installation.html>`_ to identify the representative genomes. input_prokList_v1.txt will include the complete file paths of all the genomes included in this dRep run (current database and newly added genomes).
::
 $  dRep dereplicate -p 12 -con 10 -comp 50 --S_algorithm fastANI dRep_output_v1 -g input_prokList_v1.txt -d

**3. Make a .fasta and .stb file**: Now, make a new directory with all the winning genomes (in Wdb.csv) and concatenate them into a .fasta file:
::
 $  cat all_winning_prok_genomes/* > MiFoDB_custom_prok.fasta

Make a .stb file using `parse_stb.py <https://instrain.readthedocs.io/en/master/user_manual.html>`_:
::
 $  parse_stb.py --reverse -f all_winning_prok_genomes/* -o MiFoDB_custom_prok.stb

**3. Make a gene file**: Finally, use `prodigal <https://github.com/hyattpd/Prodigal/wiki/installation>`_ to make your new gene files:
::
 $  prodigal -i MiFoDB_custom_prok.fasta -d genes.fna -a genes.faa

These files can now be used to profile your samples.

2. Adding eukaryote genomes
++++++++++++++++++++++++++++++++++++++++++++++++++++++
Adding eukaryote genomes involves one extra step.

**1. Download all genomes**: Download current MiFoDB eukaryote genomes and genomes of interest from NCBI, and add them to the same directory (ex. input_custom_euk_genomes) 

**2. Use EukCC to calculate completeness and contamination**: dRep requires completeness and contamination scores which it cannot calculate for eukaryotes. We will use `Eukcc <https://eukcc.readthedocs.io/en/latest/index.html>`_ (Saary et al. 2020) to calculate eukaryote completeness and contamination. We recommend using the docker container.
::
 $  docker run -it \
  -v MiFoDB_beta_v2_euk_renamed/:/data/ \
  -v eukcc2_db_ver_1.1:/db/ \
  -v MiFoDB_beta_v1_eukcc_v1:/MiFoDB_beta_v1_eukcc_v1 \
  quay.io/microbiome-informatics/eukcc:latest \
  folder --out MiFoDB_beta_v1_eukcc_v1 --threads 8 \
  /data/ --db /db/

With the results, make a new .csv file with the completeness and contamination to input into dRep. The input file should look like this, with the same headings:

.. csv-table:: genome_info.tsv

  genome,completeness,contamination
  C-R02.bin.8.fa,98.76,0
  C-R03.bin.1.fa,96.27,0
  C-R03.bin.3.fa,95.24,0.21
  C-R04.bin.2.fa,81.99,0

**3. Now, run dRep**: where input_eukList_v1.txt contains the complete path to the eukaryote genomes
::
 $  dRep dereplicate -p 12 -con 100 -comp 50 --S_algorithm fastANI dRep_output_euk_v1 -g input_eukList_v1.txt -d --genomeInfo genome_info.csv --contamination_weight 0

``Note that the threshold for completeness and contamination differ from prokaryotes. This was done after noticing that some high quality reference genomes had high contamination rate, potentially due some diploid eukaryote genomes. Contamination weight is thus set to 0 minimum.``

**3. Finally, proceed as with prokaryotes, making a .fasta and .stb file**: prodigal is not suited for eukaryote gene calling, so do not make a gene file. 

``When running inStrain profile, if no reads in the sample map to eukaryotic genomes in the database, it will report that inStrain has failed. That could be expected depending on the sample, so the error can be ignored.``

3. Adding substrate genomes
++++++++++++++++++++++++++++++++++++++++++++++++++++++
Adding substrate genomes involves fewer steps. 

**1. Download substrate genomes of interest** 

**2. Make a .fasta and .stb file**: Now, make a new directory with all the winning genomes (in Wdb.csv) and concatenate them into a .fasta file:
::
 $  cat all_winning_prok_genomes/* > MiFoDB_custom_prok.fasta

And finally make a .stb file using `parse_stb.py <https://instrain.readthedocs.io/en/master/user_manual.html>`_:
::
 $  parse_stb.py --reverse -f all_winning_prok_genomes/* -o MiFoDB_custom_prok.stb

Adding MAGs to database
------------------------------
You can always first assemble metagenomes from your samples and then them to your database.

*Pre-processing*

For preprocessing of the raw reads, follow the same instruction as in `quick start <https://mifodb.readthedocs.io/en/latest/quick_start.html#pre-processing>`_.

**Assembly**: To assemble your MAGs, there are a number of programs that could be used, including `MegaHIT <https://github.com/voutcn/megahit>`_ (Li et al. 2015) or `metaSPAdes <https://github.com/ablab/spades>`_ (Nurk et al. 2017).To use MegaHIT, follow the `basic usage instructions <https://github.com/voutcn/megahit?tab=readme-ov-file#basic-usage>`_.
The output will include contigs ending in .contig.fa.gz

**Binning**: Binning was performed with `MetaBAT2 <https://bitbucket.org/berkeleylab/metabat/src>`_ (Kang et al. 2019). MetaBAT2 output will include number of bins, typically starting with the sample name and ending in .fa.gz.

**Classify**: To get a sense of what the new bins might be, first use `EukRep <https://github.com/patrickwest/EukRep>`_ (West et al. 2018) to calssify whether these bins are likely prokaryotic or eukaryotic. If the reported eukaryote score is > 50% eukaryotic and the genome length is >6Mbp, the bins can be assumed to be eukaryotic. If they don't meet the criteria, they can be assumed to be prokaryotic. 

To assign taxonomy to any prokaryotic bins, you can run  `gtdbtk classify <https://ecogenomics.github.io/GTDBTk/commands/classify.html>`_ . To assign taxonomy to any eukaryotic bins, try using `tRep <https://github.com/MrOlm/tRep>`_ instead to get a potential ID.

Or, you can skip classification at this step and incorporate the bins at the respecive "Adding Genomes to Your Custom Database" step above and proceed with downstream dRep analysis. 

Functional Analysis and Gene Profiling
------------------------------
inStrain profile results are designed to easily perform functional analysis. To look for gene annotations using KEGG Orthologies (KOs), Carbohydrate-Active enZYmes (CAZymes), or Antibiotic Resistance Genes, check out `Gene Annotations <https://github.com/MrOlm/inStrain/blob/master/docs/user_manual.rst#gene-annotation>`_.

Strain Tracking
------------------------------
In order to perform strain level comparisons and identify shared strains (99.999% popANI), we can use the IS results from instrain profile and the .stb file. More information on inStrain compare  `here <https://instrain.readthedocs.io/en/master/tutorial.html#compare>`_. 

The instraincompare.csv file includes the complete path to the IS directory for each sample:

.. csv-table:: instraincompare.tsv

   sample,IS_loc,group
   EBC_009,/complete/path/to/sample/EBC_009.IS,1
   EBC_010,/complete/path/to/sample/EBC_010.IS,1
   EBC_011,/complete/path/to/sample/EBC_011.IS,1
   EBC_012,/complete/path/to/sample/EBC_012.IS,1

Then run:
::
 $  inStrain compare -i instraincompare.csv -o instraincompared_IS_results/ -p 6 -s MiFoDB_beta_v2_prok.stb

