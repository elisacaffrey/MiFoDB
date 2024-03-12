Overview
===================

The MiFoDB Workflow
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. figure:: GitHub.png
  :width: 400px
  :align: center
*The above figure shows a visual representation of the MiFoDB workflow, including pre-processing, assembly, binning, and alignment-based profiling.*


Glossary & FAQ
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Glossary of terms used in MiFoDB
------------------------------------

.. note::
  This glossary is meant to give a conceptual overview of the terms used in MiFoDB. For a more detailed overview of these concepts, see the `InStrain Glossary <https://instrain.readthedocs.io/en/latest/overview.html#glossary-faq>`_.

.. glossary::
ANI
  Average nucleotide identity

scaffold-to-bin file
  A .txt file with two columns where the first column is the scaffold name and the second column is the name of the genome the scaffold belongs to.
  Can be created using the script `parse_stb.py <https://github.com/MrOlm/drep/blob/master/helper_scripts/parse_stb.py>`_ that comes with the program
  ``dRep``  See :doc:`example_output` for more info

FAQ
------------------------------------
*Why use alignment-based profiling?*
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
There are three main methods currently used for metagenome profiling, each with advantages and disadvantages.

**1. Marker based** 

Marker based methods (i.e. MetaPhlan4) make use of gene markers identified for a vast number of reference genomes to quickly profile metagenomic samples. These methods are some of the most common, and show high accuracy for specific markers. However, based on the number of markers identified for each genome in the sample, might result in poor ientification of genomes, leading to higher false-positive rates. In addition, a marker-based method only allows for the identification of genomes with established markers, not allowing for  novel genome identification. In addition, data is generally reported as relative abundance on mapped genomes, which does not present a clear picture of how many genomes is the sample remain unknown.

**2. K-mer based** 

K-mer based methods (i.e. Clark, Kraken, Kaiju) use short exact matching substrings of fixed-length k in a genome or protein sequence, and map them to a reference database of genome or protein sequence indexes identified from a dataset. This method is very fast, but can lead to lower profiling accuracy at lower taxonomic lengths (share larger k-mer regions). These might result in higher-false positive rates. In addition, 

**3. Alignment based** 

Alignment based methods (i.e. InStrain) use a database to directly match sample reads to a genome reference database, while taking SNPs into account. While this results in high-accuracy and low false-positive rates, this method is more computationally intensive than marker based and k-mer based methods. However, reults from aligmnet based profiling can be easily used for functional analysis, strain tracking, and gene profiling. In addition, reporting of unmapped and low quality reads give a clear picture of how much of the sample is accurately profiled, and allows for the identification of novel genomes. For more information about inStrain, check out the Important concepts on the `inStrain page <https://instrain.readthedocs.io/en/latest/important_concepts.html>`_.

*What an I do with MiFoDB results?*
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
MiFoDB are incorporated into the  `inStrain workflow <https://instrain.readthedocs.io/en/latest/example_output.html#instrain-profile>`_. Output files include ``genome_info.tsv``. For example:

.. csv-table:: genome_info.tsv

  genome,coverage,breadth,nucl_diversity,length,true_scaffolds,detected_scaffolds,coverage_median,coverage_std,coverage_SEM,breadth_minCov,breadth_expected,nucl_diversity_rarefied,conANI_reference,popANI_reference,iRep,iRep_GC_corrected,linked_SNV_count,SNV_distance_mean,r2_mean,d_prime_mean,consensus_divergent_sites,population_divergent_sites,SNS_count,SNV_count,filtered_read_pair_count,reads_unfiltered_pairs,reads_mean_PID,reads_unfiltered_reads,divergent_site_count

  C-03.Ssa-BR.fna,1.686020547,0.049164091,0.004595774,1896140,182,86,0,69.19478668,0.050739639,0.011300326,0.774346839,0.000140703,0.986372334,0.988145797,,FALSE,242,39.69008264,0.951699521,0.999845137,292,254,252,165,15171,15417,0.981642137,36199,417
 
 EBC_086.5.fna,1.596317454,0.049848898,0.006035971,2377866,79,52,0,19.94120243,0.012974942,0.028909535,0.755746415,0.002048653,0.979081506,0.984682077,,FALSE,1337,56.69334331,0.637899652,0.9941014,1438,1053,1040,825,17829,19210,0.969968582,48221,1865
FS03_2016_noduplicates_bin.6.fna,1.191514863,0.041940437,0.004574618,2543035,344,186,0,21.96261861,0.013962518,0.008234649,0.650799011,0.001974379,0.966286233,0.96981997,,FALSE,393,68.18320611,0.596979301,0.989440015,706,632,628,185,14188,15687,0.965486302,39649,813
FS47_2017_noduplicates_bin.5.fna,1.907346578,0.52567291,0.001377854,1594307,35,35,1,2.642570054,0.002097472,0.150077745,0.814404746,0,0.984235383,0.984339867,,FALSE,,,,,3772,3747,3743,181,13496,13639,0.978569696,31713,3924




*Why do I not have <100% samples mapped?*
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
