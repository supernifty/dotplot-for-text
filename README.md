
Dot plot for text
=================
Generate dot plots using arbitrary text input.

Background
----------
Dot plots are a visualization tool often used in bioinformatics to compare genomic sequences.
In particular, this technique is useful for finding repeated or nearly repeated subsequences.

Similarly, this can be applied to arbitrary text to find similar pieces of text in two documents.

Usage
-----
python plot.py [options] < filename

Options
-------
- -k: k-mer size to use
- -w: use True to compare using words instead of characters
- -m: max image size
- -r: reference to compare against (if not specified, file is compared against itself)
- -a: display longest repeat

Examples
--------
- python dotplot/plot.py < data/sample.txt
- python dotplot/plot.py -k 4 -w True -a 1 -r data/sample.txt < data/sample.txt

TODO
----
- annotate long repeats
- tests

