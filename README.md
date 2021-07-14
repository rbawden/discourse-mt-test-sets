# DiscEvalMT: Contrastive test sets for the evaluation of discourse in machine translation (v2)

cf. [Evaluating Discourse Phenomena in Neural Machine Translation](https://www.aclweb.org/anthology/N18-1118)

For machine translation to tackle discourse phenomena, models must have access to extra-sentential linguistic context. There has been recent interest in modelling context in neural machine translation, but models have been principally evaluated with standard automatic metrics, poorly adapted to evaluating discourse phenomena. The aim of our article "Evaluating Discourse Phenomena in Neural Machine Translation" was to provide an alternative form of evaluation, specifically targeting discourse phenomena and the need for context beyond the level of the sentence.

The test sets, for English-to-French translation can be found in this repository. They comprise hand-crafted examples that are inspired by similar examples in the parallel corpus OpenSubtitles2016 (in terms of vocabulary usage, style and syntactic formulation).

## News

- 14/07/2021 - v2 of the dataset is out. This version corrects a slight imbalance in the pronoun types of the anaphora set (example #40 has been modified to correct this)

## Overview of the test sets

There are two separate test sets:
1) Anaphora test set, containing examples whereby an anaphoric reference can only be translated correctly into French if its antecedent (situated in the previous sentence) is correctly retrieved.
2) Lexical choice test set, containing examples other than anaphora where word choice is determined by a choice in the previous sentence. These word choices can concern lexical disambiguation (e.g. 'mole' meaning a spy, a skin blemish or the animal) or lexical cohesion phenomena, such as repetition of a specific item where a synonym would not be appropriate.

The test sets are encoded in [json format](https://json.org/)

The lexical choice test set has been translated into Czech and extended by Josef Jon. Check out this test set [here](https://github.com/cepin19/discourse-test-set).

## An example: Use of context for disambiguation

The sets are designed to test the models’ ability to exploit previous source and/or target sentences. Each example consists of a current source sentence in English and its translation in French. The source sentence contains a word or phrase that is ambiguous with respect to its translation in French, and the only way of knowing the correct translation is by looking at the context of the previous sentence (either the source sentence or the target sentence or both).

E.g. concerning the ambiguity of the translation of "mole" in French

Given the sentence "We'll have to get rid of that mole.", there are several possible translations in French, including:

* "Il va falloir enlever ce grain de beauté." (i.e. we will need to (surgically) remove the skin blemish)
* "Il va falloir se débarasser de cette taupe." (i.e. will need to get rid of this spy/animal)

Each translation will be correct in a given context, but incorrect in another context. 

Given the contexts:

*  "Could it be anything serious, Doctor?", "Est-ce que c'est grave, Docteur ?",
*  "Things could start to get dangerous if the ministers find out.", "Les choses pourraient devenir dangereuses si les ministres apprenaient ça."

the first translation is correct in the first context and incorrect in the second, and the second translation is correct in the second context and incorrect in the first. Given the preceding sentence, there is a single correct translation and an incorrect one. The sets are composed of these contrastive pairs of correct vs. incorrect translations given a context. 

## How to use the test sets

The test sets can be used to evaluate machine translation models: if models provide scores for competing translations, given the preceding context, the model's ability to exploit context can be judged on its ability to correctly discriminate between a correct translation given the context and an incorrect one. 

A model does better if it provides a better score for a correct translation in its correct context and does worse if it provides a better score for a translation in its incorrect context. The test sets are balanced such that each translation appears the same number of times in a correct context as an incorrect one, such that a non-contextual baseline model would achieve 50% accuracy on the test sets.

1. Extract sentences from .json files (previous context in separate file from current sentence):<br>
   `python3 json2rawtext.py anaphora.json anaphora OUTPUT_DIR`<br>
   `python3 json2rawtext.py lexical-choice.json lexical-choice OUTPUT_DIR`

2. Preprocess files using appropriate preprocessing for your model

3. Score all translations using your MT model and produce one score per translation

4. Evaluate the scores:<br>
   `python3 scripts/evaluate.py anaphora.json anaphora SCORE_FILE` <br>
   `python3 scripts/evaluate.py lexical-choice.json lexical_choice SCORE_FILE`

## Acknowledgments

If you use this test set, please cite
```
@inproceedings{bawden-etal-2018-evaluating,
    title = "Evaluating Discourse Phenomena in Neural Machine Translation",
    author = "Bawden, Rachel and Sennrich, Rico and Birch, Alexandra and Haddow, Barry",
    booktitle = {{Proceedings of the 2018 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers)}},
    month = jun,
    year = "2018",
    address = "New Orleans, Louisiana",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/N18-1118",
    doi = "10.18653/v1/N18-1118",
    pages = "1304--1313"
}
```

## Licence

The test sets are distributed under a CC BY-NC-SA 4.0 licence.



