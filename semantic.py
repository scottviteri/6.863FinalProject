# -*- coding: utf-8 -*-

"""
6.863 - Spring 2018 - semantic.py

This file holds the main method.
"""

from copy import deepcopy
import argparse
import readline
import traceback
import nltk

import syntactic_and_semantic_rules

import lambda_interpreter
import production_matcher

##############################################################################



def parse_input_str(input_str, verbose=False):
    trees = syntactic_and_semantic_rules.sem.parse_sentence(input_str)
    if len(trees) > 1:
        if verbose:
            print("[WARNING] Obtained %d parses; selecting the first one."%(len(trees)))
    elif len(trees) == 0:
        raise Exception("Failed to parse the sentence: " + input_str)
    return trees[0]


def handle_syntax_parser_mode(tree, sem_rule_set, gui=False):
    print "Parse Tree: "
    if gui:
        nltk.draw.tree.TreeView(production_matcher.decorate_parse_tree(tree,
                                     sem_rule_set,
                                     set_productions_to_labels=True))


def validate_output(actual_output, expected_output):
    if actual_output == expected_output:
        print "[VALIDATION] SUCCESS: '%s' does match expected output: '%s'"%(actual_output, expected_output)
    else:
        print "[VALIDATION] FAILURE: '%s' does not match expected output: '%s'"%(actual_output, expected_output)


def display_trace_gui(GUI_decorated_tree, sem_rule_set):
    # Display the GUI of the trace through the evaluation.
    if args.gui:
        try:
            trace_to_display = lambda_interpreter.eval_tree(GUI_decorated_tree, sem_rule_set, verbose=False)
            tv = drawtree.TreeView([lambda_interpreter.decorate_tree_with_trace(entry['tree'])
                                for entry in trace_to_display])
            tv.update()
            tv.showTree()
        except:
            traceback.print_exc()

##############################################################################

'''
    arg_parser.add_argument('-v',
                            '--verbose',
                            action='store_true',
                            help='output evaluation traces.')
    arg_parser.add_argument('--spm',
                            action='store_true',
                            help='syntax parser mode (no semantic evaluation).')
    arg_parser.add_argument('--gui',
                            action='store_true',
                            help="""
                                 display a graphical user interface for stepping 
                                 through the trace of the last evaluation prior to 
                                 the exiting of the program
                                 """)
    arg_parser.add_argument('--show_database',
                            action='store_true',
                            help='display the contents of the semantic database after each evaluation')
    arg_parser.add_argument('--validate_output',
                            dest='validation_file',
                            type=str,
                            required=False,
                            help='check the specified input against expected output.')
'''

#def load_sentences(batch_file='inputs.txt', gui=False, show_database=False, spm=False, validation_file=None, verbose=False):

batch_file = 'inputs.txt'
gui = False
show_database = False
spm = False
validation_file = None
verbose = False

with open(batch_file, 'r') as f_bm:
    batch_sentences = [x.strip() for x in f_bm]

if validation_file:
    print "> Validating output against " + validation_file
    with open(validation_file, 'r') as f_vo:
        valid_output = [x.strip() for x in f_vo]
        assert len(batch_sentences) == len(valid_output)

sem_rule_set = syntactic_and_semantic_rules.sem

evaluation_history = []

for input_str in batch_sentences:
    # Read in a sentence.
    print '> '+input_str

    try:
        tree = parse_input_str(input_str)
        if spm:
            handle_syntax_parser_mode(tree, sem_rule_set)
        # Evaluate the parse tree.
        decorated_tree = production_matcher.decorate_parse_tree(tree,
                                             sem_rule_set,
                                             set_productions_to_labels=False)

        trace = lambda_interpreter.eval_tree(decorated_tree,
                                             sem_rule_set,
                                             verbose)
        evaluation_history.append(deepcopy(trace))

        output = trace[-1]['expr']

        if gui:
            display_trace_gui(production_matcher.decorate_parse_tree(deepcopy(tree),
                                                  sem_rule_set,
                                                  set_productions_to_labels=True),
                              sem_rule_set)
        
    except Exception as e:
        # The parser did not return any parse trees.
        if verbose: print("[WARNING] Could not parse input.")
        #traceback.print_exc() # Uncomment this line while debugging.
        output = "I don't understand."
    

    # Print the result of the speech act
    #print output
    
    #if output_validation_mode:
    #    validate_output(output, valid_output[0])
    #    del valid_output[0]
        
    if show_database:
        syntactic_and_semantic_rules.sem.learned.print_knowledge()

def eventToDictionary(event):
    d = {}
    for k in event.keys():
        if type(event[k]) is str:
            d[k] = event[k]
        else:
            d[k] = event[k].values()[-1]
    return d

def makeGroupings(events): #making assumption that all fit in same grouping
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

event_list = syntactic_and_semantic_rules.event_list
events = map(eventToDictionary, event_list)
#print(events)
grouped_events = makeGroupings(events)
print(grouped_events)
