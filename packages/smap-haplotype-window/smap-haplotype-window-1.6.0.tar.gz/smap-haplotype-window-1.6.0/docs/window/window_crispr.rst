.. raw:: html

    <style> .purple {color:purple} </style>
	
.. role:: purple

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

.. _SMAPwindowcrispr:

######
CRISPR
######

A specific extension of the **SMAP haplotype-window** workflow for CRISPR data can be invoked using the optional command ``--guides``.

If CRISPR-mediated genome editing was performed by stable transformation with a CRISPR/gRNA delivery vector, then the presence of the gRNA cassette in the delivery vector may be detected in the transformed genome.
Primers can be designed on the vector sequence to amplify the gRNA sequence in the gRNA expression cassette, and Border regions can be positioned directly flanking the 20 bp gRNA sequence. The haplotype of that 'locus' that is then detected is effectively a copy of the gRNA sequence incorporated into the transformed genome. 
These primers can be included in the HiPlex primer set used to screen for the genomic target loci.
SMAP **haplotype-window** can assign gRNA vector-derived reads to the respective target loci, if the user provides a FASTA file with the target loci names as identifiers and the 20 bp gRNA as sequence.
In this way, genome-edited haplotypes at genomic target loci can be detected in parallel to the gRNAs that cause them, for any number of loci and any number of samples.

Example of gRNA sequences FASTA:

========================= =
>AT1G07650_1_gRNA_1
CTGAAGTCGCAGAACTTAAC
>AT1G07650_1_gRNA_2
TGACGAAGCTTAGAGAATTC
========================= =

Example of output file with diverse genome-edited haplotypes at genomic target loci and corresponding gRNA:
By sorting on the fourth column (**target**) in any output .tsv file, it is possible to arrange all the target loci with their corresponding gRNAs.

.. tabs::

   .. tab:: Unsorted output file
   
   #  .. csv-table:: 	  
	#     :file: .././tables/window/crispr_example_unsorted.csv
	#     :header-rows: 1
	  
   .. tab:: Sorted output file
   
	#  .. csv-table:: 	  
	#     :file: .././tables/window/crispr_example_sorted.csv
	#     :header-rows: 1
		

---------------

CRISPR Workflow
---------------

.. tabs::

   .. tab:: Primer and guide design
   
      .. image:: ../images/window/SMAP_window_design_1.png
	  
   .. tab:: Multiplex PCR per sample
   
      .. image:: ../images/window/SMAP_window_crispr_2.png
	  
   .. tab:: Multiplex amplicon pooling across all samples
   
      .. image:: ../images/window/SMAP_window_crispr_3.png
	  
   .. tab:: Illumina adapter ligation
   
      .. image:: ../images/window/SMAP_window_crispr_4.png
	  
   .. tab:: Paired-end sequencing
   
      .. image:: ../images/window/SMAP_window_crispr_5.png
	  
   .. tab:: Forward and Reverse read merging

      .. image:: ../images/window/SMAP_window_crispr_6.png

   .. tab:: Sample demultiplexing

      .. image:: ../images/window/SMAP_window_crispr_7.png

   .. tab:: Sample index and universal tail trimming  
   
      .. image:: ../images/window/SMAP_window_crispr_8.png