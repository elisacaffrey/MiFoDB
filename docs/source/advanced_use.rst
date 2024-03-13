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
  $  wget https://storage.googleapis.com/sylph-stuff/v0.3-c1000-gtdb-r214.syldb -O gtdb_database_c1000.syldb
or
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


Functional Analysis
------------------------------



Gene Profiling
------------------------------


Adding MAGs to database
------------------------------
If you are interested in assemling metagenomes from your samples, you can calculate the same 
