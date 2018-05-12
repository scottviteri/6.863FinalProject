# -*- coding: utf-8 -*-

"""
NOTE: Only add lines in this file that have the form:

sem.add_rule(...) 

OR

sem.add_lexicon_rule(...)
"""


def add_my_rules(sem):
    ## Problem 3.
    #John gave Mary Fido.
    sem.add_rule("V_args -> V3[+tense] NP[-wh] NP[-wh]",
                 lambda v3, np1, np2: lambda subj: v3(subj, np1, np2))

    #John did give Mary Fido. and Did John give Mary Fido?
    # Rule for Problem 3-b.
    sem.add_rule("VBAR[+fin] -> V3[-tense] NP[-wh] NP[-wh]",
                 lambda v3, np1, np2: lambda subj: v3(subj, np1, np2))

    # What did John give Mary?
    sem.add_rule("VBAR[+fin]/NP -> V3[-tense] NP NP/NP",
                lambda v3, np1, np2: lambda subj, patient:\
                    v3(subj, np1, patient))

    
    # Problem 4.
    # John saw the woman who caught Fido.
    sem.add_rule("NP -> NP Q[+wh]", lambda np, q: np)

    # Susan saw the man that Poirot ate.
    sem.add_rule("NP[-wh] -> NP[-wh] SBAR_that", lambda np, sbar: np)
