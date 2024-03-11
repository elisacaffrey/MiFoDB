Quick Start
===================
This workflow will walk you through the steps needed to go from getting your data back from a sequencing facility to having a profiled list of genomes with the mapped relative abundances.

Pre-processing
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Before being able to use the data, you will need to:

**1.** Trim any sequencing adapters so that you are left with just reads from your original sample

**2.** Remove any potential contaminating human genomes (this is less of a problem with fermented foods, but a huge deal when collecting human stool samples packed with the donors DNA)

**3.** Perform QC metrics to get a sense of the sequencing quality

For steps 1. and 2. we can use `BBTools <https://jgi.doe.gov/data-and-tools/software-tools/bbtools/>`_



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


