# Tokenization for language processing

This package contains some generic configurable tools allowing to cut a string in sub-parts (cf. [Wikipedia](https://en.wikipedia.org/wiki/Lexical_analysis#Tokenization)), called `Token`, and to group them into sequences called `Tokens`. A `Token` is a sub-string from a parent string (say the initial complete text), with associated ranges of non-overlaping characters. The number of associated ranges is arbitrary. A `Tokens` is a collection of `Token`. These two classes allow to associate to any `Token` a collection of attributes in a versatile way, and to pass these attributes from one object to the next one while cutting `Token` into sub-parts (collected as `Tokens`) and eventually re-merging them into larger `Token`.

`Token` and `Tokens` classes allow basic tokenization of text, such as word splitting, n-gram splitting, char-gram splitting of arbitrary size. In addition, it allows to associate several non-overlapping sub-strings into a given `Token`, and to associate arbitrary attributes to these parts. One can compare two different `Token` objects in terms of their attributes and/or ranges. One can also apply basic mathematical operations and logic to them (+,-,*,/) corresponding to the union, difference, intersection and symmetric difference implemented by Python set ; here the sets are the ranges of position from the parent string.

## Depositories, and online documentation

The different sources of informations for this packages are : 
 
 - the official Python Package Installation (PyPI) repository is on [https://pypi.org/project/tokenspan](https://pypi.org/project/tokenspan)
 - the official git repository is on [https://framagit.org/nlp/tokenspan](https://framagit.org/nlp/tokenspan)
 - the official documentation is on [https://nlp.frama.io/tokenspan/](https://nlp.frama.io/tokenspan/)
 

## Philosophy of this library

In `tokenspan`, one thinks of a string as a collection of integers: the position of each character in the string. For instance

```python
'Simple string for demonstration and for illustration.' # the parent string
'01234567891123456789212345678931234567894123456789512' # the positions

'       string                       for illustration ' # the Span span1
'       789112                       678 412345678951 ' # the ranges

'Simple                                               ' # the Span span2
'012345                                               ' # the ranges
```

To define the `Span` `'string for illustration'` consists in selecting the positions `[range(7,13),range(36,39),range(40,52)]` from the parent string, and the `Span` `'simple'` is defined by the positions `[range(0,6),]`. 

In addition, one can see the above ranges as sets of positins. Then it is quite easy to perform some basic operations on the `Span`, for instance the addition of two `Span`

```python
str(span1 + span2) = 'Simple string for illustration'
```

is interpreted as the union of their relative sets of positions.

In addition to these logical operations, there are a few utilities, like the possibility to split or slice a `Span` into `Span` objects, as long as their are all related to the same parent string.

## Basic example

Below we give a simple example of usage of the `Token` and `Tokens` classes.

```python
import re
from tokenspan import Span

string = 'Simple string for demonstration and for illustration.'
initial_span = Span(string)

# char-gram generation
chargrams = initial_span.slice(0,len(initial_span),3)
str(chargrams[2])
# return 'mpl'

# each char-gram conserves a memory of the initial string
chargrams[2].string
# return 'Simple string for demonstration and for illustration.'

cuts = [range(r.start(),r.end()) for r in re.finditer(r'\w+',string)]
spans = initial_span.split(cuts)
# this returns a list of Span objects

# spans conserve the cutted parts
interesting_spans = spans[1::2]
# so one has to take only odd elements

# an other possibility to keep only the words is to construct it explicitly
spans = Span(string, ranges=cuts)

# n-gram construction
ngram = [Span(string, ranges=[r1,r2]) for r1, r2 in zip(spans.ranges[:-1],
                                                        spans.ranges[1:])]
ngram[2]
# return Span('for demonstration', [(14,17),(18,31)])
str(ngram[2])
# return 'for demonstration'
ngram[2].ranges
# return [range(14, 17), range(18, 31)]
ngram[2].subSpans
# return the Span instances composed of span 'for' and span 'demonstration'

# are the two 'for' Token the same ?
interesting_spans[2] == interesting_spans[-2]
# return False, because they are not at the same position

# basic operations among Token
for_for = interesting_spans[2] + interesting_spans[-2]
str(for_for)
# return 'for for'
for_for.ranges
# return [range(14, 17), range(36, 39)]
for_for.string
# return 'Simple string for demonstration and for illustration.'
# to check the positions of the two 'for' Token : 
#        '01234567890...456...01234567890.....67890............'

# also available : 
# span1 + span2 : union of the sets of span1.ranges and span2.ranges
# span1 - span2 : difference of span1.ranges and span2.ranges
# span1 * span2 : intersection of span1.ranges and span2.ranges
# span1 / span2 : symmetric difference of span1.ranges and span2.ranges

```

Other examples can be found in the [documentation](https://nlp.frama.io/tokenspan/).

## Comparison with other Python libraries

A comparison with some other NLP librairies (nltk, gensim, spaCy, gateNLP, ...) can be found in the [documentation](https://nlp.frama.io/tokenspan/comparison_other_libraries.html)

## Installation

Simply run 

```bash
pip install tokenspan
```

should install the library from Python Package Index (PIP). The official repository is on https://framagit.org/nlp/tokenspan. To install the package from the repository, run the following command lines 

```bash
git clone https://framagit.org/nlp/tokenspan.git
cd tokenspan/
pip install .
```

Once installed, one can run some tests using

```bash
cd tests/
python3 -m unittest -v
```

(verbosity `-v` is an option).

## Versions

See [CHANGES file](CHANGES.md) in this folder.

## About us

Package developped for Natural Language Processing at IAM : Unité d'Informatique et d'Archivistique Médicale, Service d'Informatique Médicale, Pôle de Santé Publique, Centre Hospitalo-Universitaire (CHU) de Bordeaux, France.

You are kindly encouraged to contact the authors by issue on the [official repository](https://framagit.org/nlp/tokenspan/-/issues/), and to propose ameliorations and/or suggestions to the authors, via issue or merge requests.

Last version : Jan 20, 2022