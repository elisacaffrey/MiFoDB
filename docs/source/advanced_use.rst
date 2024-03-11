Advanced Use
============

Creating a custom MiFoDB
------------------------------
While the latest version of MiFoDB (`MiFoDB_beta_v2 <https://docs.google.com/spreadsheets/d/1PHRlb9YwKiwpVk8ChozBZbFYCA-VL3EXJTIPI-TI04A/edit?usp=sharing>`_)  includes 675 genomes (586 prokaryote, 82 eukaryote, and 7 substrate genomes), there will be a number of cases in which you might want to add 


work directory file-tree
+++++++++++++++++++++++++

::

  workDirectory
  ./data
  ...../checkM/
  ...../Clustering_files/
  ...../gANI_files/
  ...../MASH_files/
  ...../ANIn_files/
  ...../prodigal/
  ./data_tables
  ...../Bdb.csv  # Sequence locations and filenames
  ...../Cdb.csv  # Genomes and cluster designations
  ...../Chdb.csv # CheckM results for Bdb
  ...../Mdb.csv  # Raw results of MASH comparisons
  ...../Ndb.csv  # Raw results of ANIn comparisons
  ...../Sdb.csv  # Scoring information

Functional Analysis
------------------------------


Gene Profiling
------------------------------
