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

import rules
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
        return []
        #raise Exception("Failed to parse the sentence: " + input_str)
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
    new_event_list = groupEvent(event_list, new_event, event_grouping_strategy)
    return new_event_list

def sentenceToEventDict(sem, sentence):
    tree = parse_input_str(sem, sentence)
    if not tree: return None
    # Evaluate the parse tree.
    decorated_tree = production_matcher.decorate_parse_tree(tree,
                                         sem,
                                         set_productions_to_labels=False)
    trace = lambda_interpreter.eval_tree(decorated_tree,
                                         sem,
                                         verbose=False)
    new_event = trace[-1]['expr']
    new_event_dict = {k:new_event[k] for k in new_event.keys() if k != 'semantic type'}
    return new_event_dict

def getTerminals(sem):
    rh_sides = filter(lambda x: len(x)==1, map(lambda x: x.rhs(), sem.productions))
    words = filter(lambda x: type(x) is str, map(lambda y:y[0], rh_sides))
    return words



