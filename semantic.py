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
    new_event_list = groupEvent(event_list, new_event)
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


def train(sem, sentences):
    event_list = []
    for sentence in sentences:
        # Read in a sentence. -- how to control where processsent goes
        print '> '+sentence

        try:
           new_event_dict = sentenceToEventDict(sem, sentence)
           event_list = groupEvent(event_list, new_event_dict)
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

def checkGoodSentence(sem, sentence, event_list):
    event = sentenceToEventDict(sem, sentence)
    if not event: return False
    for event_group in event_list:
        if set(event.keys()) == set(event_group.keys()):
            if all([event[k] in event_group[k] for k in event.keys()]):
                return True
    return False
    
def getTerminals(sem):
    rh_sides = map(lambda x: x.rhs(), sem.productions)
    words = [rhs[0] for rhs in rh_sides if len(rhs) == 1 and type(rhs[0]) is str]
    return words

def test(sem, sentences, event_list):
    results = {}
    guess_words = getTerminals(sem)
    for sentence in sentences:
        without_word =  sentence.split()[:-1]
        good_hypotheses = []
        for guess_word in guess_words:
            guess_sentence = ' '.join(without_word + [guess_word])
            if checkGoodSentence(sem, guess_sentence, event_list): 
                good_hypotheses.append(guess_sentence) 
        results[sentence] = good_hypotheses
    return results 
        

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
print "\n Training"
training_events = train(sem, training_sentences)
testing_results = test(sem, testing_sentences, training_events)
print "\n Testing"
print testing_results 


"""
if validate:
    print "> Validating predicted words"
    with open(testing_sentences_file, 'r') as f_vo:
        valid_output = [x.strip() for x in f_vo]
        assert len(training_sentences) == len(valid_output)
"""

