# Xlassify

Fast and accurate taxonomic classification of bacteria genomes is a key step in human gut microbiome analysis. Here we propose Xlassify, an alignment-free deep-learning model that is specifically trained to classify human gut bacteria.

Xlassify demonstrated 98% accuracy in UHGG genomes dataset and \~90% accuracy on an independent testset of 76 gut bacterial genomes isolated from healthy Chinese individuals. Better than alignment-based methods such as GTDBTk, Xlassify requires only <4GB of memory and reaches thirty-second-per-genome speed on a single CPU.
