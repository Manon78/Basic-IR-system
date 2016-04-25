# Basic-IR-system

This project is a very basic implementation of an information retrieval system.

At its core, it presents a user with the id numbers of the lines in which the terms queried by the user appear together.
With further work, it will return these lines in order of relevance based on tf.idf (term frequency * inverted document frequency) and the lnc.ltn weighting scheme.

Prior to using this program, a line of code must be written in perl:
perl -ne '$a++;s/\s+/ $a\n/g;print $_;' tr "[:upper:]" "[:lower:]" < file.txt | sort -t ' ' -k1,1 -k2,2n -u > file_index.txt
This command takes a text file and returns an index containing the terms in the file lower-cased and the line* number on which each term appears (*lines delimitated by new-line character)

The following program takes this index as an input (entered in the terminal), as so:
python3 Basic_IR_system.py file_index.txt

Interactions with the user are done in the terminal throughout.
