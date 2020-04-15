# Word analyzer

## Description

This program analyzes the source set of words was obtained from the file (-s parameter), clear this set 
from incorrect symbols, split cleared words to lexemes, then correct them by replacing assumed incorrect words 
to right words and then will create new set of words and save it to the destination file (-d parameter).

##### Optional arguments:

```-s, --source``` - the source file containing the set of words you need to analyze. By default, it's 
"wordanalyzer/data/rockyou.txt"

```-f, --frequency``` - the dictionary ordered by frequency of word usage, which will be used to perform 
the splitting text and correcting incorrect words (if the dictionary parameter -w isn't override). By default, it's
"wordanalyzer/data/frequency_words.txt"

```-d, --destination``` - the destination file where the processed set of source words will be saved. By default, 
it's "wordanalyzer/new_words.txt"

```-c, --count``` - count of words which will be processed (set of words will be selected randomly). That is the count
that will be loaded from source file (-s parameter). By default, it's whole file.

```-e, --encoding``` - if your "source" of "frequency" file isn't "utf-8" encoding, you can change this parameter. 
That value will be passed to the function of loading data and this function will read the file with appropriate
encoding. By default, it's "utf-8".

```-t, --tree``` - in the process will be built a bk-tree which will help to correct and find similar words to any word.
This tree is based on words are ordered by frequency usage. This tree can take a long time to build. Therefore, you can
save built tree to a file or you can load the tree from the file, if it was saved before. By default, it's None.

```-similar, --similar-words``` - how many similar words will be returned by method of searching similar words. That 
value must be optimal, because very small values (1-2) specify that a word must be interpreted unambiguously, but it 
isn't reliable. Very big values (>=6) will also produce outliers, in addition to correct words. By default, it's 4.

```-dist, --distance``` - what Damerau's distance will be used to search for similar words. You can set big values, but
it will promote words very different from the original word. By default, it's 1.

```-thres, --threshold``` - how many parts will be spliced when processing and searching for a correct word. That is
the number of parts of a word that will be in turn processed to generate new correct word. By default, it's 2.

```-n, --number-corrected``` - how many corrected words will be returned after processing and correcting a word. 
You should keep in mind that one cleared word (without any incorrect symbols) will be added to the new corrected words.

```-v, --verbose``` - if it specified, the process of correcting words will be printed to stdout.

## Installation
1) You can install it to your host machine like:
    * `git clone https://gitlab.com/lpshkn/wordanalyzer.git`
    * `cd wordanalyzer`
    * run tests - `python3 setup.py test`
    * setup - `sudo python3 setup.py install`

2) You can build a docker image:
    * `git clone https://gitlab.com/lpshkn/wordanalyzer.git`
    * `cd wordanalyzer`
    * `docker build -t wordanalyzer:0.1.0 .`

## Usage

```shell script
wordanalyzer [-s <source_file>] [-d <destination_file>] [-c <count>] [-e <encoding>] [-t <tree>] [-similar <number>]
[-dist <distance>] [-thres <threshold>] [-n <number>] [-v]
```

If you built the docker image, you can run it:

```shell script
docker run -it wordanalyzer:0.1.0
```

All data files are in /data directory. To try it out, just input:

```shell script
wordanalyzer -t data/bk_tree.pickle -c 300 -v -d new_words.txt
```

## Testing:


##### Coverage
```
Name                            Stmts   Miss  Cover
---------------------------------------------------
analyzer/__init__.py                1      0   100%
analyzer/arguments_parser.py       21      0   100%
analyzer/load_data.py              16      0   100%
analyzer/methods.py                25      0   100%
analyzer/text_splitter.py          28      0   100%
analyzer/word_analyzer.py         124     21    83%
pybktree.py                        62     14    77%
strsim/__init__.py                  1      0   100%
similarity/damerau.py              34      1    97%
similarity/string_distance.py       9      3    67%
---------------------------------------------------
TOTAL                             321     39    88%
```

## Examples:

* Let's assume that the source file is `rockyou.txt`, file with frequency words is `frequency_words.txt`. So we want to
analyze just 300 words of all list and save the result to `new_words.txt`. Meanwhile, we'll build and save a bk-tree to
`bk_tree.pickle`. Then it will seem like:

  ```shell script
  wordanalyzer -s rockyou.txt -d new_words.txt -f frequency_words.txt -t bk_tree.pickle -c 300
  ```
  
  If you want to see the process, append `-v`
  
* You can load all words from `rockyou.txt`, just don't specify `-c` parameter. Suppose now, that you aren't satisfied
with the last result. You can try change any different values of `-similar`, `-dist`, `-thres`, `-n`, but it can 
both improve the result and decrease it. Absolutely, very big values promote to increase work time.

  ```shell script
  wordanalyzer -t bk_tree.pickle -similar 6 -dist 2 -thres 3 -n 5
  ```
