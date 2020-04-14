# Word analyzer
## Description
This program analyzes the source set of words was obtained from the file (-s parameter), clear this set 
from incorrect symbols, split cleared words to lexemes, then correct them by replacing assumed incorrect words 
to right words and then will create new set of words and save it to the destination file (-d parameter).

##### Optional arguments:

```-s, --source``` - the source file containing the set of words you need to analyze

```-f, --frequency``` - the dictionary ordered by frequency of word usage, which will be used to perform 
the splitting text and correcting incorrect words (if the dictionary parameter -w isn't override)

```-d, --destination``` - the destination file where the processed set of source words will be saved

```-w, --words-dictionary``` - the dictionary which will be used to perform correcting incorrect words (by default, 
the same file as in -f parameter)


## Usage




## Example:


