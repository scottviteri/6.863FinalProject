# -*- coding: utf-8 -*-

"""
6.863 - Spring 2018 - semantic.py

This file holds the main method.
"""

import copy 
import argparse
import readline
import traceback
import drawtree

import syntactic_and_semantic_rules
import semantic_rule_set

import lambda_interpreter
import production_matcher


##############################################################################


def parse_input_str(sem, input_str):
    trees = sem.parse_sentence(input_str)
    if len(trees) > 1: #can pick the tree that is likely by the measure we are creating here 
        print("[WARNING] Obtained %d parses; selecting the first one."%(len(trees)))
    elif len(trees) == 0:
        raise Exception("Failed to parse the sentence: " + input_str)
    return trees[0]


def validate_output(actual_output, expected_output):
    if actual_output == expected_output:
        print "[VALIDATION] SUCCESS: '%s' does match expected output: '%s'"%(actual_output, expected_output)
    else:
        print "[VALIDATION] FAILURE: '%s' does not match expected output: '%s'"%(actual_output, expected_output)


def display_trace_gui(GUI_decorated_tree, sem_rule_set):
    # Display the GUI of the trace through the evaluation.
    if gui:
        try:
            trace_to_display = lambda_interpreter.eval_tree(GUI_decorated_tree, sem_rule_set, verbose=False)
            tv = drawtree.TreeView([lambda_interpreter.decorate_tree_with_trace(entry['tree'])
                                for entry in trace_to_display])
            tv.update()
            tv.showTree()
        except:
            traceback.print_exc()



def parse(sem, sentences, training=True):
    for input_str in sentences:
        # Read in a sentence. -- how to control where processsent goes
        print '> '+input_str

        try:
            tree = parse_input_str(sem, input_str)
            # Evaluate the parse tree.
            decorated_tree = production_matcher.decorate_parse_tree(tree,
                                                 sem,
                                                 set_productions_to_labels=False)

            
            trace = lambda_interpreter.eval_tree(decorated_tree,
                                                 sem,
                                                 verbose=False)
            evaluation_history.append(copy.deepcopy(trace))
            event_list = trace[-1]['expr']


        except Exception as e:
            # The parser did not return any parse trees.
            print e
            raise
        
        if show_database:
            sem.learned.print_knowledge()
        if gui:
            display_trace_gui(
                production_matcher.decorate_parse_tree(copy.deepcopy(tree),
                                    sem,
                                    set_productions_to_labels=True),
                              sem)

    return events

def makeGroupingsOneOffBatch(events): 
    # Keep this around for comparison purposes
    grouping_dict = {}
    for feature in events[0].keys():
        grouping = set() 
        for i in range(len(events)): 
            for j in range(i+1,len(events)):
                grouping.add(events[i][feature])
                if all([events[i][k]==events[j][k] for k in events[0].keys() if k != feature]) and events[i][feature] != events[j][feature]:
                    grouping.add(events[j][feature])
        grouping_dict[feature] = grouping
    return grouping_dict 

training_sentences_file = 'training.txt'
testing_sentences_file = 'testing.txt'
show_database = False
validate = False
gui = False

with open(training_sentences_file, 'r') as f:
    training_sentences = [x.strip() for x in f]
with open(testing_sentences_file, 'r') as f:
    testing_sentences = [x.strip() for x in f]


sem = semantic_rule_set.SemanticRuleSet()
sem = syntactic_and_semantic_rules.addLexicon(sem)
training_events = parse(sem, training_sentences, training=True)
#testing_events = parse(sem, testing_sentences, training=False)
 

"""
if validate:
    print "> Validating predicted words"
    with open(testing_sentences_file, 'r') as f_vo:
        valid_output = [x.strip() for x in f_vo]
        assert len(training_sentences) == len(valid_output)
"""

