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
import semantic_db

import lambda_interpreter
import production_matcher
import category 
import cfg


##############################################################################
# Rules


##############################

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


def processSentence(event_list, data):
    new_event = {k:data[k] for k in data.keys() if k != 'semantic type'}
    new_event_list = groupEvent(event_list, new_event)
    return new_event_list


def parse(sem, sentences, training=True):
    event_list = []
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
            new_event = trace[-1]['expr']
            new_event_dict = {k:new_event[k] for k in new_event.keys() if k != 'semantic type'}
            event_list = groupEvent(event_list, new_event_dict)
            print event_list 

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

    return event_list 

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


def groupEvent(event_list, new_event): #if different structure, do not match
    new_event_list = copy.deepcopy(event_list)
    merged = False
    #try merging in
    for i in range(len(event_list)): #try to match with event_list[i]
        event = event_list[i]
        if set(event.keys()) == set(new_event.keys()):
            unequal_count = 0
            for feat in event.keys():
                if new_event[feat] not in event[feat]:
                    unequal_feat = feat
                    unequal_count += 1
            if unequal_count <= 1: #merge into previous
                new_event_list[i][unequal_feat].add(new_event[unequal_feat])
                merged = True
    #make new spot
    if not merged:
        new_event_list.append({k:set([v]) for k,v in new_event.iteritems()})
    return new_event_list


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
testing_events = parse(sem, testing_sentences, training=False)
 

"""
if validate:
    print "> Validating predicted words"
    with open(testing_sentences_file, 'r') as f_vo:
        valid_output = [x.strip() for x in f_vo]
        assert len(training_sentences) == len(valid_output)
"""

