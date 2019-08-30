#! encoding: utf8
import re
import argparse
import json

import os

def open_file(fname):
    if ".gz" in fname: fp = gzip.open(fname, "rt")
    else: fp = open(fname, "r")
    return fp


def has_tuple(pair, diffs):
    return pair in diffs


def has_regex_tuple(regex_pair, diffs):
    for pair in diffs:
        if re.match(regex_pair[0], pair[0]) and re.match(regex_pair[1], pair[1]):
            return True
    return False



def scores2analysis_lexical_choice(score_file, testjson):
    tfp = open_file(score_file)
    test = json.load(open(testjson))
    
    # analyse different types of examples
    analysis = {"numcorrect": 0,
                "numincorrect":0,
                "repet-numcorrect":0,
                "repet-numincorrect":0,
                "disambig-numcorrect":0,
                "disambig-numincorrect":0,
                "repet, disambig-numcorrect":0,
                "repet, disambig-numincorrect":0,
                "whole_examples_correct": []}

    # go through blocks of examples
    for exampleblock in sorted([int(x) for x in test.keys()]):
        numexamplescorrect = 0 # how many correct in a block

        # individual examples
        for example in test[str(exampleblock)]["examples"]:

            # source and contrastive translations
            src=example["src"]
            trg_correct=example["trg"]["correct"]
            trg_incorrect=example["trg"]["incorrect"]

            # type of example (repet, disambig)
            if "type" in test[str(exampleblock)]:
                type_coh=test[str(exampleblock)]["type"]
            else:
                type_coh=None
            if type_coh not in ["repet", "disambig", "repet, disambig", None]:
                exit(str(type_coh)+" is not a real type")
                
            # get one score for each translation (first correct, then contrastive)
            score_correct = float(tfp.readline().strip())
            score_incorrect=float(tfp.readline().strip())

            # lower is better, compare the scores
            if score_correct < score_incorrect:
                analysis["numcorrect"]+=1
                numexamplescorrect+=1
            else:
                analysis["numincorrect"]+=1

            # separate by type of phenomenon
            if type_coh is not None:
                if score_correct < score_incorrect:
                    analysis[type_coh+"-numcorrect"]+=1
                else:
                    analysis[type_coh+"-numincorrect"]+=1

        
        #if numexamplescorrect != 1:
        #    print(exampleblock, 'numexamplescorrect = ', numexamplescorrect)
                           
        # are all examples correct in this block?
        if numexamplescorrect==len(test[str(exampleblock)]["examples"]):
            analysis["whole_examples_correct"].append(str(exampleblock))

    return analysis


def analyse_lexical_choice(analysis):
    total=(analysis["numcorrect"] +analysis["numincorrect"])

    # summary number of correct and incorrect
    print("Total correct: " +str(analysis["numcorrect"]))
    print("Total incorrect: " +str(analysis["numincorrect"]) + "\n")
    print("Number of example blocks entirely correct: " + \
          str(len(analysis["whole_examples_correct"])))
    print("Number of example blocks not entirely correct: " + \
          str(total-len(analysis["whole_examples_correct"])) + "\n")

    print("--------- By type of example -----------")
    print("Repet: Total: " +str(analysis["repet-numcorrect"] + \
                               analysis["repet-numincorrect"]) + \
          ", #correct: " +str(analysis["repet-numcorrect"]) + \
          ", #incorrect: " +str(analysis["repet-numincorrect"]))
    print("Disambig: Total: " +str(analysis["disambig-numcorrect"] + \
                                   analysis["disambig-numincorrect"]) + \
          ", #correct: " +str(analysis["disambig-numcorrect"]) + \
          ", #incorrect: " +str(analysis["disambig-numincorrect"]))

    # summary in one line
    print("\n--------- Summary ---------")
    print("Total precision = " + str(analysis["numcorrect"]) + '/' + str(total) + \
          " = " + str(analysis["numcorrect"] / float(total)) + "\n")

    #print("\t".join([str(analysis["numcorrect"]),
    #                 str(len(analysis["whole_examples_correct"])),
    #                 str(analysis["repet-numcorrect"]),
    #                 str(analysis["disambig-numcorrect"])]))
    
    
def scores2analysis_anaphora(score_file, testjson):
    tfp = open_file(score_file)
    test = json.load(open(testjson))

    analysis = {"numcorrect":{"correct":0, "semi-correct":0},
                "numincorrect":{"correct":0, "semi-correct":0},
                "pronouns":{
                    "numcorrect":{"correct":0, "semi-correct":0},
                    "numincorrect":{"correct":0, "semi-correct":0},
                    "m.sg":{"numcorrect":{"correct":0, "semi-correct":0},
                            "numincorrect":{"correct":0, "semi-correct":0}},
                    "m.pl":{"numcorrect":{"correct":0, "semi-correct":0},
                            "numincorrect":{"correct":0, "semi-correct":0}},
                    "f.sg":{"numcorrect":{"correct":0, "semi-correct":0},
                            "numincorrect":{"correct":0, "semi-correct":0}},
                    "f.pl":{"numcorrect":{"correct":0, "semi-correct":0},
                            "numincorrect":{"correct":0, "semi-correct":0}},
                },
                "whole_examples": {"all_correct": [], "at_least_one_incorrect": []}
    }

    # go through each example
    for example in sorted([int(x) for x in test.keys()]):

        # source and target
        example = str(example)
        src = test[example]["src"]
        trg = test[example]["trg"]

        # keep track of num correct and incorrect
        num_correct = 0
        num_incorrect = 0
        
        ptypes = {} # to check number of different types

        # for each possible target constrastive pair
        for t in trg:
            
            # is it correct or semi-correct translation?
            if "correct" in t:
                exampletype = "correct"
            else:
                exampletype="semi-correct"


            # what gender and number?
            gennum = t["type"]


            #if gennum == "f.pl" and exampletype=="semi-correct":
            #    print(t[exampletype])
            #    input()
            
            # get correct and incorrect translations and their scores
            correct = t[exampletype]
            incorrect = t["incorrect"]
            score_correct = float(tfp.readline().strip())
            score_incorrect = float(tfp.readline().strip())

            
            # compare raw scores and mark as correct or incorrect
            if score_correct < score_incorrect:
                analysis["numcorrect"][exampletype] +=1
                num_correct += 1
            else:
                analysis["numincorrect"][exampletype] +=1
                num_incorrect +=1

            # (in)correct for that example type
            if score_correct < score_incorrect:
                analysis["pronouns"]["numcorrect"][exampletype] +=1
                analysis["pronouns"][gennum]["numcorrect"][exampletype] +=1
            else:
                analysis["pronouns"][gennum]["numincorrect"][exampletype] +=1


            

        # for baseline, should be 2
        #if num_incorrect!=2:
        #    print(str(num_incorrect) + " = examples incorrect")
        #    print(example)

        if num_incorrect==0:
            analysis["whole_examples"]["all_correct"].append(example)

        else: analysis["whole_examples"]["at_least_one_incorrect"].append(example)

        
    return analysis


    
def analyse_anaphora(analysis):    
    print("Distribution of pronoun types (in examples): ")
    for pron in ["m.sg", "f.sg", "m.pl", "f.pl"]:

        num_correct_ex = analysis["pronouns"][pron]["numcorrect"]["correct"] +analysis["pronouns"][pron]["numincorrect"]["correct"]
        num_semicorrect_ex = analysis["pronouns"][pron]["numcorrect"]["semi-correct"] +analysis["pronouns"][pron]["numincorrect"]["semi-correct"]
        
        print("\t" +pron +"\ttotal: " +str(num_correct_ex + num_semicorrect_ex))
        print("\t\t\t: correct: " +str(num_correct_ex) +", semi-correct: " +str(num_semicorrect_ex))

    print("----------------")
    print("Number correct of each type:")

    total_correct=0
    for pron in ["m.sg", "f.sg", "m.pl", "f.pl"]:

        num_correct_correct_ex = analysis["pronouns"][pron]["numcorrect"]["correct"]
        num_correct_semi_ex = analysis["pronouns"][pron]["numcorrect"]["semi-correct"]
        num_incorrect_correct_ex = analysis["pronouns"][pron]["numincorrect"]["correct"]
        num_incorrect_semi_ex = analysis["pronouns"][pron]["numincorrect"]["semi-correct"]

        total_correct += num_correct_correct_ex + num_correct_semi_ex
        
        print("\t" +pron +"\tTotal correct: " +str(num_correct_correct_ex + num_correct_semi_ex))
        print("\t\t\t: correct: " +str(num_correct_correct_ex) +" correct, " +str(num_correct_semi_ex) +" semi-correct")
        print("\t\t\t: incorrect: " +str(num_incorrect_correct_ex) +" correct, " +str(num_incorrect_semi_ex) +" semi-correct")

    print("----------------")
    print("How many example blocks (of 4 contrastive pairs) are systematically right?")

    print("Number of examples where all right: " +str(len(analysis["whole_examples"]["all_correct"])))
    print("\tCorresponds to examples:" +str(analysis["whole_examples"]["all_correct"]))
    #print("At least one wrong: " +str(len(analysis["whole_examples"]["at_least_one_incorrect"])))
    

    # short summary
    if False:
        print("\t".join([str(total_correct),
                     str(analysis["pronouns"]["m.sg"]["numcorrect"]["correct"] + \
                         analysis["pronouns"]["m.sg"]["numcorrect"]["semi-correct"]),
                     str(analysis["pronouns"]["f.sg"]["numcorrect"]["correct"] + \
                         analysis["pronouns"]["f.sg"]["numcorrect"]["semi-correct"]),
                     str(analysis["pronouns"]["m.pl"]["numcorrect"]["correct"] + \
                         analysis["pronouns"]["m.pl"]["numcorrect"]["semi-correct"]),
                     str(analysis["pronouns"]["f.pl"]["numcorrect"]["correct"] + \
                         analysis["pronouns"]["f.pl"]["numcorrect"]["semi-correct"]),
                     str(len(analysis["whole_examples"]["all_correct"]))
        ])
        )

    total = sum(analysis["numcorrect"].values()) + sum(analysis["numincorrect"].values())
    print("\n-------- Summary ---------")
    print("Overall precision = " + str(total_correct) + "/" + str(total) +
          " = " + str(total_correct/float(total)))
    
    #print("Total numbers: " +str(sum(analysis["numcorrect"].values())) +" correct, " +str(sum(analysis["numincorrect"].values())) +" incorrect")
    #print(analysis)


    

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_test_set_file")
    parser.add_argument("type", choices=["anaphora", "lexical_choice"])
    parser.add_argument("scorefile")
    args = parser.parse_args()

    src, trg = 'en', 'fr' #tuple(args.lang.split("-"))


    if args.type=="anaphora":
        analysis = scores2analysis_anaphora(args.scorefile, args.json_test_set_file)
        analyse_anaphora(analysis)
    else:
        analysis = scores2analysis_lexical_choice(args.scorefile, args.json_test_set_file)
        analyse_lexical_choice(analysis)




