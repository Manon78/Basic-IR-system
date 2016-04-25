# Basic-IR-system

This project is a very basic implementation of an information retrieval system.

At its core, it presents a user with the id numbers of the lines in which the terms queried by the user appear together.
With further work, it will return these lines in order of relevance based on tf.idf (term frequency * inverted document frequency) and the lnc.ltn weighting scheme.

This program takes a text file as input (entered in the terminal), as so:
python3 Basic_IR_system.py text_file.txt

Interactions with the user are done in the terminal.
