Advanced Use
============

Creating a custom MiFoDB
------------------------------
While the latest version of MiFoDB (`MiFoDB_beta_v2 <https://docs.google.com/spreadsheets/d/1PHRlb9YwKiwpVk8ChozBZbFYCA-VL3EXJTIPI-TI04A/edit?usp=sharing>`_)  includes 675 genomes (586 prokaryote, 82 eukaryote, and 7 substrate genomes), there will be a number of cases in which you might want to add custom genomes. 

There are a few recommended ways of doing this, depending on genome type. 

1. Identifying and adding prokaryote genomes
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



2. Adding eukaryote genomes
++++++++++++++++++++++++++++++++++++++++++++++++++++++

3. Adding substrate genomes
++++++++++++++++++++++++++++++++++++++++++++++++++++++


Functional Analysis
------------------------------



Gene Profiling
------------------------------


Adding MAGs to database
------------------------------
MiFoDB is based on inStrain profiling, so output will be the same as described in  `inStrain profile <https://instrain.readthedocs.io/en/latest/example_output.html#instrain-profile>`_. For every sample, there will be a number of inStrain output files (`detailed here <https://instrain.readthedocs.io/en/latest/example_output.html#instrain-profile>`_), but the most important output files is ``genome_info.tsv``. For example:



Which can be used to calculate the total abundance. Examples on how to do that is included in `example output <https://mifodb.readthedocs.io/en/latest/example_output.html>`_.
