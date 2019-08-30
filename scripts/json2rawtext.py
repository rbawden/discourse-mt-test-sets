#! encoding: utf8
import re
import argparse
import json
import os

def open_file(fname):
    if ".gz" in fname: fp = gzip.open(fname, "rt")
    else: fp = open(fname, "r")
    return fp


def write_to_plain_text_lexical_choice(fname, outputdir, lsrc, ltrg, type_artificial="lexical_choice"):
    with open(fname) as fp:
        test = json.load(fp)
    src_curr = open(outputdir+"/"+type_artificial+".current."+lsrc, "w")
    src_prev = open(outputdir+"/"+type_artificial+".prev."+lsrc, "w")
    trg_curr = open(outputdir+"/"+type_artificial+".current."+ltrg, "w")
    trg_prev = open(outputdir+"/"+type_artificial+".prev."+ltrg, "w")

    for exampleblock in sorted([int(x) for x in test.keys()]):
        examples = test[str(exampleblock)]["examples"]
        for example in examples:
            
            src=example["src"]
            trg_correct=example["trg"]["correct"]
            trg_incorrect=example["trg"]["incorrect"]
            for i in range(2):
                src_curr.write(src[1]+"\n")
                src_prev.write(src[0]+"\n")
            trg_curr.write(trg_correct[1]+"\n")
            trg_prev.write(trg_correct[0]+"\n")
            trg_curr.write(trg_incorrect[1]+"\n")
            trg_prev.write(trg_incorrect[0]+"\n")
    src_curr.close()
    src_prev.close()
    trg_curr.close()
    trg_prev.close()    
    
    
def write_to_plain_text(fname, outputdir, lsrc, ltrg, type_artificial="anaphora"):
    with open(fname) as fp:
        test = json.load(fp)

    src_curr = open(outputdir+"/"+type_artificial+".current."+lsrc, "w")
    src_prev = open(outputdir+"/"+type_artificial+".prev."+lsrc, "w")
    trg_curr = open(outputdir+"/"+type_artificial+".current."+ltrg, "w")
    trg_prev = open(outputdir+"/"+type_artificial+".prev."+ltrg, "w")
        
    for example in sorted([int(x) for x in test.keys()]):
        example = str(example)
        src = test[example]["src"]
        trg = test[example]["trg"]
        
        for t in trg:
            
            # for each pair correct-incorrect, print out
            if "correct" in t: correct = t["correct"]
            else: correct = t["semi-correct"]
            incorrect = t["incorrect"]

            # print out twice (for correct and incorrect)
            for i in range(2):
                src_curr.write(src[1]+"\n")
                src_prev.write(src[0]+"\n")
            # print out targets
            # correct
            trg_curr.write(correct[1]+"\n")
            trg_prev.write(correct[0]+"\n")
            # then incorrect
            trg_curr.write(incorrect[1]+"\n")
            trg_prev.write(incorrect[0]+"\n")
    src_curr.close()
    src_prev.close()
    trg_curr.close()
    trg_prev.close()        

    
    


    

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("artificial_test_set")
    parser.add_argument("type", choices=["anaphora", "lexical-choice"])
    #parser.add_argument("lang", choices=["en-fr"])
    parser.add_argument("outputdir")
    args = parser.parse_args()

    src, trg = "en", "fr" #tuple(args.lang.split("-"))

    if args.type=="anaphora":
        write_to_plain_text(args.artificial_test_set, args.outputdir, src, trg)
    else:
        write_to_plain_text_lexical_choice(args.artificial_test_set, args.outputdir, src, trg)



