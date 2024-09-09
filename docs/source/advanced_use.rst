Advanced Use
============

Creating a custom MiFoDB
------------------------------
While the latest version of `MiFoDB <https://zenodo.org/records/10881265/files/MiFoDB_beta_v2_allRef.csv?download=1>`_)  includes 675 genomes (586 prokaryote, 82 eukaryote, and 7 substrate genomes), there will be a number of cases in which you might want to add custom genomes. 

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

**1. Check that the genomes of interest are not included in the original input set**: If the genomes is >95% ANI it won't have been used as a representative genomes. This is primarily a problem for eukaryotes, and less for prokaryotes. However, taxonomy might have been updated, so microbes of two different names might now be considered the same species. This step is not as important, but could save you a lot of time.

**2. Download all the reference genomes already in MiFoDB_prok or MiFoDB_euk:** These are two .zip files available on https://zenodo.org/records/10870254, named MiFoDB_beta_v2_allprokgenomes.zip

**3. Download your new reference genomes of interest from NCBI**

**4. Add your downloaded reference genomes to the MiFoDB_beta_v2_allprokgenomes directory**: You should now have all the genomes from the current database + your additional genomes. Rename the new .fasta files to end in .fa

**5. Run dRep on all genomes**: In order to prevent the inclusion of genomes with >95% ANI or with low completeness and high contamination which might confound your results, you will want to make sure you only include one representative genome for each species. 

Run `dRep <https://drep.readthedocs.io/en/latest/installation.html>`_ to identify the representative genomes from your new input directory. input_prokList_v1.txt will include the complete file paths of all the genomes included in this dRep run (current database and newly added genomes).
::

 $  dRep dereplicate -p 12 -con 10 -comp 50 --S_algorithm fastANI dRep_output_v1 -g input_prokList_v1.txt -d

**6. Make a .fasta and .stb file**: Now, make a new directory with all the winning genomes (in Wdb.csv) and concatenate them into a .fasta file:
::

 $  cat all_winning_prok_genomes/* > MiFoDB_custom_prok.fasta

Make a .stb file using `parse_stb.py <https://instrain.readthedocs.io/en/master/user_manual.html>`_:
::

 $  parse_stb.py --reverse -f all_winning_prok_genomes/* -o MiFoDB_custom_prok.stb

**7. Make a gene file**: Finally, use `prodigal <https://github.com/hyattpd/Prodigal/wiki/installation>`_ to make your new gene files:
::

 $  prodigal -i MiFoDB_custom_prok.fasta -d genes.fna -a genes.faa

These files can now be used to profile your samples.

2. Adding eukaryote genomes
++++++++++++++++++++++++++++++++++++++++++++++++++++++
Adding eukaryote genomes involves one extra step.

**1. Download all genomes**: Follow steps 1-4 in the section above, downloading MiFoDB_beta_v2_alleukgenomes.zip from https://zenodo.org/records/10870254

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

 $  cat all_substrate_genomes/* > MiFoDB_custom_sub.fasta

And finally make a .stb file using `parse_stb.py <https://instrain.readthedocs.io/en/master/user_manual.html>`_:
::

 $  parse_stb.py --reverse -f all_substrate_genomes/* -o all_substrate_genomes.stb

Adding MAGs to database
------------------------------
You can always first assemble metagenomes from your samples and then them to your database.

*Pre-processing*

For preprocessing of the raw reads, follow the same instruction as in `step-by-step <https://mifodb.readthedocs.io/en/latest/step_by_step.html>`_

**Assembly**: To assemble your MAGs, there are a number of programs that could be used, including `MegaHIT <https://github.com/voutcn/megahit>`_ (Li et al. 2015) or `metaSPAdes <https://github.com/ablab/spades>`_ (Nurk et al. 2017).To use MegaHIT, follow the `basic usage instructions <https://github.com/voutcn/megahit?tab=readme-ov-file#basic-usage>`_.
The output will include contigs ending in .contig.fa.gz

You can also use `nextflow <https://mifodb.readthedocs.io/en/latest/quick_start.html>`_ to run assembly. 

**1. Prepare an input sheet**: pointing to the preprocessing output. 

.. csv-table:: *processingInfo_v1.csv*

    sample,fastq_1,fastq_2,single_end
    EBC_087,/location/of/your/trimmed_file/EBC_087_S160_L003_R1.trim.fastq.gz,/location/of/your/file/trimmed_file/EBC_087_S160_L003_R2.trim.fastq.gz,

**2. Run assemble**:
::

$ nextflow run https://github.com/MrOlm/nf-core-genomeresolvedmetagenomics/main.nf -entry ASSEMBLE --input processingInfo_v1.csv --outdir results_assembly --assemblers "megahit" --max_memory 500GB -resume

The results will be located in a file called megahit/assembly/*.MEGAHIT.fasta.gz

You can now proceed to:
1. Incorporate these MAGs into a new database (`see Adding genomes to your database <https://mifodb.readthedocs.io/en/latest/advanced_use.html#adding-prokaryote-genomes-to-your-custom-database>`_). First, remember to get a sense of what the new bins might be, using `EukRep <https://github.com/patrickwest/EukRep>`_ (West et al. 2018) to classify whether these bins are likely prokaryotic or eukaryotic. If the reported eukaryote score is > 50% eukaryotic and the genome length is >6Mbp, the bins can be assumed to be eukaryotic. If they don't meet the criteria, they can be assumed to be prokaryotic. Proceed with either `adding them to other prokaryote genomes <https://mifodb.readthedocs.io/en/latest/advanced_use.html#adding-prokaryote-genomes-to-your-custom-database>`_, or adding them to other known `eukaryote genomes <https://mifodb.readthedocs.io/en/latest/advanced_use.html#adding-eukaryote-genomes>`_.

2. If you only want to use your MAGs, proceed to binning below.

**Binning**: Binning was performed with `MetaBAT2 <https://bitbucket.org/berkeleylab/metabat/src>`_ (Kang et al. 2019). MetaBAT2 output will include number of bins, typically starting with the sample name and ending in .fa.gz.

*1. Prepare an input sheet*: pointing to the preprocessing output. 

.. csv-table:: *binInfo_v1.csv*

    sample,assembly,group,fastq_1,fastq_2,single_end
    EBC_087,/location/of/your/assembly_file/*_MEGAHIT.fasta.gz,1,/location/of/your/trimmed_file/EBC_087_S160_L003_R1.trim.fastq.gz,/location/of/your/file/trimmed_file/EBC_087_S160_L003_R2.trim.fastq.gz,

The group column can be modified to aid in sample binning. For example, if you are processing dairy and vegetable samples, you might write dairy and vegetable to assist in sample binning, as samples might have more common genomes. 

*2. Run binning*: The nextflow bin command also allows you to classify genomes (see classify below). To do this, make sure to download `gtdbtk <https://ecogenomics.github.io/GTDBTk/commands/classify.html>`_, `tRep <https://github.com/MrOlm/tRep>`_ , and the `checkV <https://pypi.org/project/checkv/#markdown-header-checkv-database>`_ databases, and point to the appropriate files.

::

$ nextflow run https://github.com/MrOlm/nf-core-genomeresolvedmetagenomics/main.nf entry BIN --input binInfo_v1.csv --outdir results_v3 --gtdb /path/to/GTDB/gtdbtk_r207_v2_data.tar.gz --checkv_db /path/to/checkv/checkv-db-v1.2.tar.gz --trep_diamond /path/to/trep/uniref100.translated.diamond.dmnd --trep_ttable /path/to/trep/uniref100.ttable.gz -resume

*The results will be located in a file called megahit/assembly/*.MEGAHIT.fasta.gz*

**Classify**: If you already have MAGs or genomes you are interested in classifying, you can run `gtdbtk <https://ecogenomics.github.io/GTDBTk/commands/classify.html>`_, or `tRep <https://github.com/MrOlm/tRep>`_ to get taxonomic IDs.

Functional Analysis and Gene Profiling
-----------------------------------------------------
InStrain profile results are designed to easily perform functional analysis. To look for gene annotations using KEGG Orthologies (KOs), Carbohydrate-Active enZYmes (CAZymes), or Antibiotic Resistance Genes, check out `Gene Annotations <https://github.com/MrOlm/inStrain/blob/master/docs/user_manual.rst#gene-annotation>`_.

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

