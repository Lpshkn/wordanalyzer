# Word analyzer

## Abstract

That program can this:  

7h15myp4555w0rd754 -> this my password  

## Description

The main goal of this program consists of analyzing a list of words that you can pass to the input. 
This program has 4 modes of working and can work in multiple mode at time. These modes will be described below:

* **Count** the cost of a word: you can count the cost of each word of the word list. Counting depends on the splitting 
  a word to the several words and the counting the cost of each part. The cost of a word is a rank of this word 
  in a frequency words list.

* **Clear** a word: you can clear a word from incorrect characters(0-9, !@#$...+=_, space characters etc.).

* **Correct** a word: you can correct a word using the Damerau-Levenshtein distance. You'll need to a frequency word list,
  because that distance will be calculated depending on this list of words.
  
* **Select** the base parts of a word: you can split the word to the several parts and use stemming to convert them. 
  Thus, you will get the base parts of this word.

Of course, you can save all results into the files that you can specify for each mode. If you just use a mode, 
but don't specify a file, results will be printed in the stdout.

## Arguments:

```-s, --source``` - the source file containing a set of words you need to analyze. Note, if you specify `-w` option, 
this option won't be considered, because of the `-w` option has a higher priority.

```-w, --words``` - the input list of words which you need to process. If it's specified, the source file containing 
a list of words will be ignored.

```-f, --frequency``` - the dictionary ordered by the frequency of word usage, which will be used to perform 
the splitting text and correcting wrong words. This option is necessary and should be specified.

```-c, --count``` - a number of words which will be processed (a set of words will be selected randomly). That is the count
that will be loaded from a source file (-s parameter). By default, it's all words.

```-e, --encoding``` - if your "source" of "frequency" file isn't "utf-8" encoding, you can change this parameter. 
That value will be passed to the function of loading data and this function will read the file with appropriate
encoding. By default, it's "utf-8".

```-t, --tree``` - in process will be built a bk-tree which will help to correct and find similar words to any word.
This tree is based on the words ordered by the frequency usage. Building the tree can take some time. Therefore, you can
save built tree to a file or you can load the tree from the file, if it was saved before. By default, it's None.

```-similar, --similar-words``` - how many similar words will be returned by the method of searching similar words. That 
value must be optimal, because very small count of values (1-2) specifies that the word must be interpreted unambiguously, but it 
isn't reliable. Very big values (>=6) will also produce outliers, in addition to correct words. By default, it's 4.

```-dist, --distance``` - what Damerau's distance will be used to search for similar words. You can set a big value, but
it will promote words very different from the original word. By default, it's 1.

```-thres, --threshold``` - how many parts will be spliced when processing and searching for a correct word. That is
the number of parts of a word that will be in turn processed to generate new correct word. By default, it's 2.

```-n, --number-corrected``` - how many corrected words will be returned after processing and correcting a word. 
You should keep in mind that one cleared word (without any incorrect symbols) will be added to the new corrected words.

```-cost, --total-cost``` - one of 4 mode to count the total cost of a word. You can specify it without any file 
and results will be printed in the stdout. But if you will specify a filename, all results will be saved into this file.

```-clr, --clear-word``` - one of 4 modes to clear words. You can specify it without any file and results 
will be printed in the stdout. But if you will specify a filename, all results will be saved into this file.

```-correct, --correct``` - one of 4 modes to correct words. You can specify it without any file and results 
will be printed in the stdout. But if you will specify a filename, all results will be saved into this file.

```-basic, --base-words``` - one of 4 modes to get the base parts of a word. You can specify it without any file 
and results will be printed in the stdout. But if you will specify a filename, all results will be saved into this file.

```-v, --verbose``` - if it specified, the process of analyzing words will be more detailed. 

## Installation
Before installing, you should install the requirements (it you don't use docker or setup.py):  
```shell script
pip3 install -r requirements.txt
```
  
There are 3 ways to install this program, you can choose any way that suits you:

1) You can clone this repository and just run the main.py module:
    * `git clone https://gitlab.com/lpshkn/wordanalyzer.git`
    * `cd wordanalyzer`
    * `python3 main.py [OPTIONS]`
2) You can install it to your host machine:
    * `git clone https://gitlab.com/lpshkn/wordanalyzer.git`
    * `cd wordanalyzer`
    * `sudo python3 setup.py install`
    * `wordanalyzer [OPTIONS]`

3) You can build a docker image:
    * `git clone https://gitlab.com/lpshkn/wordanalyzer.git`
    * `cd wordanalyzer`
    * `docker build -t wordanalyzer:1.0.0 .`

## How To Use:

*NOTE*: If you use Docker, just run:
```shell script
docker run -it wordanalyzer:1.0.0
```
Then you may run any commands.

#### Required parameters

To use this program, you need to know, that there are some necessary options. Therefore, the next rules help you:
1) At first, you need to specify a list of words that you want process. You may do it using `-s` option to specify 
   a file where the list is or using `-w` option to specify space-separated words directly in the command line. As like:
   `-s source.txt` or `-w word1 word2 ... wordN`
   
2) At second, you must specify a frequency dictionary (list of words ordered by frequency usage) using `-f` parameter:
   `-f frequency.txt`
   
3) At third, you must choose a mode that you want use. All modes were described above. You can use several modes at time.
   Note, that you can save results of each mode in an individual file or even one file. If you specify only mode without
   any file, results will be printed in stdout. 
   
   For example:  
   `-clr file.txt -correct file.txt -basic -cost` - this saves results of clearing and correcting words into the file.txt, 
   results of selecting the base parts and counting the cost will be printed in stdout
   
   *NOTE*: you can specify a filename as "STDOUT" and results will be printed in stdout:  
   `-clr file.txt -correct file.txt -basic STDOUT -cost STDOUT`
   
So, the usage of this program is extremely easy using the next formula:
```shell script
wordanalyzer -w words/-s filename -f frequency_file -clr/-cost/-correct/-basic [file]
```

#### Optional parameters

To get more appropriate results for your purpose, you can configure processing as you wish. 
For this there are some optional parameters.

1) Suppose, you have a very large list of words and you need process some sample of it. You may use `-c` parameter:
   `-c 300` - this processes a list of 300 words which will be selected randomly of your list.
   
2) Maybe your file has incorrect encoding and can't be processed. You may specify an encoding using `-e` parameter.  
   For example: `-e "utf-8"`.

3) Suppose, you aren't satisfied by results. You can try to configure the process using configuration values: 
   `-similar`, `-dist`, `-thres`, `-n`. Just try to pass them different values and check results.  
   For example: `-similar 3 -dist 4 -thres 2 -n 5`
   
4) To decrease the preparatory time you can save a bk-tree that will be built when program starts, using `-t` parameter. 
   In next time, this tree will be loaded from the file, if you specify `-t` again.  
   For example: `-t tree.pickle`
   
5) If you need more detailed report of processing you may specify `-v` parameter. So, when processing you will get 
   a text in the files that you specified for modes or in the stdout.  
   
   For example, if you specify `-clr file.txt -correct file.txt -cost file.txt -basic -v`, you will get the next text: 
   `word: ***, cost: ***, cleared word: ***, corrected word: ***` - in the file and `word: ***, base words: ***` in the stdout.

## Just try it!
To realize it, just run one of these command:

```shell script
wordanalyzer -s ./data/short_rockyou.txt -f ./data/frequency_words.txt -c 300 -clr clear.txt -cost clear.txt -correct -basic -v
```

```shell script
wordanalyzer -w 7h15myp4555w0rd754 -f ./data/frequency_words.txt -correct -v
```

## Testing:
##### Coverage
```
Name                        Stmts   Miss  Cover 
-----------------------------------------------
analyzer/__init__.py            1      0   100%
analyzer/bk_tree.py            42      0   100%
analyzer/configurator.py      129     19    85%   
analyzer/load_data.py          20      0   100%
analyzer/methods.py            85      4    95%   
analyzer/text_splitter.py      28      0   100%
analyzer/word_analyzer.py     166     62    63% 
-----------------------------------------------
TOTAL                         471     85    82%
```

## Examples:

* Let's assume that the source file is `rockyou.txt`, file with frequency words is `frequency_words.txt`. So we want to
clear, correct and count cost of just 300 words of all list and save the result to `new_words.txt`. 
Meanwhile, we'll build and save a bk-tree to `bk_tree.pickle`. Also, we want see more detailed information. 
Then it will seem like:

  ```shell script
  wordanalyzer -s rockyou.txt -f frequency_words.txt -t bk_tree.pickle -c 300 -clear new_words.txt \
  -correct new_words.txt -cost new_words.txt -v
  ```
    
   You can load all words from `rockyou.txt`, just don't specify `-c` parameter.
   
* Suppose now, that you want get only a list of corrected words, just write:
  ```shell script
  wordanalyzer -s rockyou.txt -f frequency_words.txt -t bk_tree.pickle -correct output.txt
  ```
  
  This way works with any mode.
