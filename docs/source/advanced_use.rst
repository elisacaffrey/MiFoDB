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

.. csv-table:: genome_info.tsv

  genome,coverage,breadth,nucl_diversity,length,true_scaffolds,detected_scaffolds,coverage_median,coverage_std,coverage_SEM,breadth_minCov,breadth_expected,nucl_diversity_rarefied,conANI_reference,popANI_reference,iRep,iRep_GC_corrected,linked_SNV_count,SNV_distance_mean,r2_mean,d_prime_mean,consensus_divergent_sites,population_divergent_sites,SNS_count,SNV_count,filtered_read_pair_count,reads_unfiltered_pairs,reads_mean_PID,reads_unfiltered_reads,divergent_site_count
 C-03.Ssa-BR.fna,1.686020547,0.049164091,0.004595774,1896140,182,86,0,69.19478668,0.050739639,0.011300326,0.774346839,0.000140703,0.986372334,o.988145797,,FALSE,242,39.69008264,0.951699521,0.999845137,292,254,252,165,15171,15417,0.981642137,36199,417 
 EBC_086.5.fna,1.596317454,0.049848898,0.006035971,2377866,79,52,0,19.94120243,0.012974942,0.028909535,0.755746415,0.002048653,0.979081506,0.984682077,,FALSE,1337,56.69334331,0.637899652,0.9941014,1438,1053,1040,825,17829,19210,0.969968582,48221,1865
 FS03_2016_noduplicates_bin.6.fna,1.191514863,0.041940437,0.004574618,2543035,344,186,0,21.96261861,0.013962518,0.008234649,0.650799011,0.001974379,0.966286233,0.96981997,,FALSE,393,68.18320611,0.596979301,0.989440015,706,632,628,185,14188,15687,0.965486302,39649,813
 FS47_2017_noduplicates_bin.5.fna,1.907346578,0.52567291,0.001377854,1594307,35,35,1,2.642570054,0.002097472,0.150077745,0.814404746,0,0.984235383,0.984339867,,FALSE,,,,,3772,3747,3743,181,13496,13639,0.978569696,31713,3924

Which can be used to calculate the total abundance. Examples on how to do that is included in `example output <https://mifodb.readthedocs.io/en/latest/example_output.html>`_.
