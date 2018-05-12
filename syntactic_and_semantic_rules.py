# -*- coding: utf-8 -*-

import lab3.cfg
from lab3.category import Category, GrammarCategory, Variable, C, StarCategory
from lab3.semantic_rule_set import SemanticRuleSet
from lab3.semantic_db import pretty_print_entry

####################################################################

def translate(data):
    pass

def translateModifier(data):
    pass

####################################################################

identity = lambda x: x

sem = SemanticRuleSet()

####################################################################
# Speech Actions
def processSentence(data):
    sem.learned.add_fact(data)
    return "Okay."


def ynQuestion(data):
    if sem.learned.yesno_query(data):
        return "Yes."
    else:
        return "No."


def whQuestion(data):
    results = sem.learned.wh_query(data)
    if len(results) == 0:
        return "I don't know."
    else:
        return list(results)[0]


def npOnlyHuhResponse(data):
    return "What about %s?"%(pretty_print_entry(data))


####################################################################
# Start rules


sem.add_rule("Start -> S", lambda s: processSentence(s))

# Declarative Sentence
sem.add_rule("S -> NP[-wh] VP", lambda np, vp: vp(np)) 

sem.add_rule("Start -> Q[+wh]", lambda q: whQuestion(q))

sem.add_rule("Start -> Q[-wh]", lambda q: ynQuestion(q))

sem.add_rule("Q[-wh] -> Do_Modal NP[-wh] VBAR[+fin]",
             lambda dm, np, vbar: dm(vbar(np)))

sem.add_rule("Start -> NP", lambda np: npOnlyHuhResponse(np))

####################################################################
# Where did ...

#(Where) (did John eat)
sem.add_rule("Q[+wh] -> AdvP[+wh] Q[-wh]",
             lambda advp, q:\
                 q.addFeature(str(advp["type"]), advp["var"]))

sem.add_rule("Q[+wh] -> NP[+wh] VP", 
             lambda np, vp: vp(np))

#(who) (...)
sem.add_rule("Q[+wh] -> NP[+wh] Q/NP",
             lambda np, q: q(np))

#did John see
sem.add_rule("Q/NP -> Do_Modal NP VBAR[+fin]/NP",
             lambda dm, np, vbar: lambda object:\
                 dm(vbar(np, object)))

sem.add_rule("VBAR[+fin]/NP -> V2[-tense] NP/NP",
             lambda v2, e: v2)

sem.add_rule("VBAR[+fin]/NP -> V3[-tense] NP PP_dat/NP",
             lambda v3, np, pp: lambda subj, beneficiary:\
                 v3(subj, beneficiary, np))

sem.add_rule("VBAR[+fin]/NP -> V3[-tense] NP/NP PP_dat",
             lambda v3, np, pp: lambda subj, patient:\
                 v3(subj, pp, patient))

####################################################################
# NP

#sem.add_rule("NP[-wh] -> Name", identity)
sem.add_rule("NP[-pro,-wh] -> Name",
             identity)
sem.add_rule("NP[-pro,-wh] -> Det APX N",
             lambda det, apstar, n: n(det, apstar))
sem.add_rule("NP[-pro,-wh] -> APX N[+mass]",
             lambda apstar, nmass: nmass(apstar))



####################################################################
# AdvP[+wh]
sem.add_rule("AdvP[+wh] -> Adv[+wh]", identity)

####################################################################
# AP
sem.add_rule("APX -> APX AP", lambda apstar, ap: C(ap, mod=apstar))
sem.add_rule("APX ->", lambda: StarCategory())
sem.add_rule("AP -> A", identity)

####################################################################
# VP

sem.add_rule("VP -> V_args",
             lambda v: lambda subj: v(subj))

sem.add_rule("VP -> Do_Modal VBAR[+fin]",
             lambda dm, vbar: lambda subj: dm(vbar(subj)))

sem.add_rule("V_args -> Be[+tense] V_part[form: V2]",
             lambda be, vpart: lambda subj:\
                 be(vpart(Category.parse("Object"), subj)))

sem.add_rule("V_args -> Be[+tense] V_part[form: V2] PP_by",
             lambda be, vpart, pp: lambda subj:\
                 be(vpart(pp, subj)))

# ---

sem.add_rule("V_args -> V1[+tense]",
             lambda v1: lambda subj: v1(subj))

sem.add_rule("V_args -> V1[+tense] PP",
             lambda v1, pp: lambda subj: pp(v1(subj)))

sem.add_rule("VBAR[+fin] -> V1[-tense]",
             lambda v1: lambda subj: v1(subj))

# ---

sem.add_rule("V_args -> V2[-plural,+tense] NP",
             lambda v2, np: lambda subj: v2(subj, np))

sem.add_rule("V_args -> V2[+tense,+plural] NP",
             lambda v2, np: lambda subj: v2(subj, np))

sem.add_rule("V_args -> V2[+tense] NP[-wh] PP",
             lambda v2, np, pp: lambda subj: pp(v2(subj, np)))

sem.add_rule("VBAR[+fin] -> V2[-tense] NP[-wh]",
             lambda v2, np: lambda subj: v2(subj, np))

# ---

sem.add_rule("V_args -> V3[+tense] NP[-wh] PP_dat",
             lambda v3, np, pp: lambda subj: v3(subj, pp, np))

sem.add_rule("VBAR[+fin] -> V3[-tense] NP[-wh] PP_dat",
             lambda v3, np, pp: lambda subj: v3(subj, pp, np))


####################################################################

sem.add_rule("V_args -> V4[+tense] NP[-wh] PP[+loc]",
             lambda v4, np, pp: lambda subj: v4(subj, np, pp))

# ---

sem.add_rule("V_args -> V5[+tense] VBAR[-fin]",
             lambda v5, vbar: lambda subj: v5(subj, vbar(subj)))

# ---

sem.add_rule("V_args -> V6[+tense] NP[-wh] VBAR[-fin]",
             lambda v6, np, vbar: lambda subj: v6(subj, np, vbar(np)))

# ---

sem.add_rule("V_args -> V8[+tense] SBAR_that[-fact]",
             lambda v8, sbar: lambda subj: v8(subj, sbar))

# ---

sem.add_rule("V_args -> V9[+tense] SBAR_that[+fact]",
             lambda v9, sbar: lambda subj: v9(subj, sbar))

# ---

sem.add_rule("V_args -> V10[+tense] AP_pred",
             lambda v10, ap: lambda subj: v10(subj, ap))

# ---

sem.add_rule("V_args -> V11[+tense] Q_emb",
             lambda v11, qemb: lambda subj: v11(subj, qemb))

# ---

sem.add_rule("V_args -> V12[+tense] SBAR_for",
             lambda v12, sbar: lambda subj: v12(subj, sbar))

####################################################################

# VBAR[-fin]
sem.add_rule("VBAR[-fin] -> To VBAR[+fin]",
             lambda to, vbar: lambda subj: vbar(subj))

# Q_emb
sem.add_rule("Q_emb -> SBAR_comp[+wh]", identity)

# AP_pred
sem.add_rule("AP_pred -> A_pred PP", lambda a, ppstar: a(ppstar))

# PP
sem.add_rule("PP -> P NP", lambda p, np: p(np))
sem.add_rule("PP_dat -> P_dat NP", lambda p, np: p(np))
sem.add_rule("PP_by -> P_by NP", lambda p, np: p(np))

# SBAR_that
sem.add_rule("SBAR_that -> That S",
             lambda that, s: s)

# SBAR_comp[+wh]
sem.add_rule("SBAR_comp[+wh] -> Comp[+wh] S",
             lambda comp, s: s)

# SBAR_for
sem.add_rule("SBAR_for -> For NP[-wh] VBAR[-fin]",
             lambda for_, np, vbar: vbar(np))

# Do or Modal
sem.add_rule("Do_Modal -> Do[+tense]", identity)
sem.add_rule("Do_Modal -> Modal", identity)

# Empty slash rules
sem.add_rule("NP/NP ->", lambda: None)
sem.add_rule("PP_dat/NP -> P_dat NP/NP", lambda p, np: None)

####################################################################
## Lexicon

# Names
sem.add_lexicon_rule("Name",
                     ['John', 'Mary', 'Fido', 'Poirot', 'Susan'],
                     lambda name: C("Object", name=name))

# Common nouns
sem.add_lexicon_rule("N[-mass, number=singular]",
                     ['book', 'city', 'dog', 'man', 'park', 'woman', 'country'],
                     lambda word: lambda det, apstar:\
                         C("Object", type=word, definite=det, mod=apstar))

sem.add_lexicon_rule("N[-mass, number=plural]",
                     ['books', 'cities', 'dogs', 'men', 'parks', 'women', 'countries'],
                     lambda word: lambda det, apstar:\
                         C("Object", type=word, definite=det, mod=apstar))

# Determiners
sem.add_lexicon_rule("Det",
                     ['the', 'this'],
                     lambda word: True)

sem.add_lexicon_rule("Det",
                     ['a', 'an'],
                     lambda word: False)

# wh-words
sem.add_lexicon_rule("NP[+pro, +wh]",
                     ['who', 'what'],
                     lambda word: Variable(word))

sem.add_rule("Adv[+wh] -> 'where'",
             lambda word:\
                 C('Adverb', type='locative', var=Variable("where")))

####################################################################

v1form = (GrammarCategory(pos="V1"),
   lambda root, tense:\
		lambda word: lambda agent:\
			C("Event", action=root, agent=agent, tense=tense))

sem.add_verb(v1form, 'come', 'came', 'comes', 'come')
sem.add_verb(v1form, 'drive', 'drove', 'drives', 'driven')
sem.add_verb(v1form, 'eat', 'ate', 'eats', 'eaten')
sem.add_verb(v1form, 'return', 'returned', 'returns')
sem.add_verb(v1form, 'sing', 'sang', 'sings', 'sung')
sem.add_verb(v1form, 'sleep', 'slept', 'sleeps')
sem.add_verb(v1form, 'talk', 'talked', 'talks')

####################################################################

v2form = (GrammarCategory(pos="V2"),
	lambda root, tense:\
		lambda word: lambda agent, patient:\
			C("Event", action=root, agent=agent, patient=patient, tense=tense))

sem.add_verb(v2form, 'eat', 'ate', 'eats', 'eaten')
sem.add_verb(v2form, 'buy', 'bought', 'buys')
sem.add_verb(v2form, 'catch', 'caught', 'catches')
sem.add_verb(v2form, 'chase', 'chased', 'chases')
sem.add_verb(v2form, 'compute', 'computed', 'computes')
sem.add_verb(v2form, 'drive', 'drove', 'drives', 'driven')
sem.add_verb(v2form, 'find', 'found', 'finds')
sem.add_verb(v2form, 'hate', 'hated', 'hates')
sem.add_verb(v2form, 'keep', 'kept', 'keeps')
sem.add_verb(v2form, 'kill', 'killed', 'kills')
sem.add_verb(v2form, 'like', 'liked', 'likes')
sem.add_verb(v2form, 'love', 'loved', 'loves')
sem.add_verb(v2form, 'make', 'made', 'makes')
sem.add_verb(v2form, 'pass', 'passed', 'passes')
sem.add_verb(v2form, 'please', 'pleased', 'pleases')
sem.add_verb(v2form, 'sing', 'sang', 'sings', 'sung')
sem.add_verb(v2form, 'see', 'saw', 'sees', 'seen')
sem.add_verb(v2form, 'support', 'supported', 'supports')
sem.add_verb(v2form, 'surprise', 'surprised', 'surprises')
sem.add_verb(v2form, 'visit', 'visited', 'visits')
sem.add_verb(v2form, 'kiss', 'kissed', 'kisses')
sem.add_verb(v2form, 'lose', 'lost', 'loses')

####################################################################

v3form = (GrammarCategory(pos="V3"),
	lambda root, tense:\
		lambda word: lambda agent, beneficiary, patient:\
			C("Event", action=root, agent=agent, patient=patient, beneficiary=beneficiary, tense=tense))

sem.add_verb(v3form, 'give', 'gave', 'gives', 'given')

####################################################################
# prepositions

sem.add_rule("P[-loc] -> 'in'",
             lambda word: lambda location: lambda frame:\
                 frame.addFeature("locative", C("Place", relation="in", location=location)))

sem.add_rule("P[-loc] -> 'under'",
             lambda word: lambda location: lambda frame:\
                 frame.addFeature("locative", C(None, relation="under", location=location)))

sem.add_rule("P[+loc] -> 'on'",
             lambda word: lambda location:\
                 C("locative", C(None, relation="on", location=location)))

sem.add_rule("P[-loc] -> 'of'",
             lambda word: lambda source: lambda frame:\
                 frame.addFeature("source", source))

sem.add_rule("P_dat -> 'to'",
             lambda word: identity)

sem.add_rule("P_by -> 'by'",
             lambda word: identity)

####################################################################

# Adjectives -- disabled for now.

sem.add_lexicon_rule("A",
                     ['rabid', 'raw', 'smart', 'red', 'blue'],
                     lambda word: C(word))

                     
## sem.add_rule("A_pred -> 'suspicious'",
##              lambda word: lambda source:\
##                  C("suspicious", source=source))

####################################################################

# Aux and Modal
sem.add_rule("Do[+tense] -> 'did'",
            lambda word: lambda verb_frame:\
                verb_frame.addFeature("tense", "past"))

sem.add_rule("Do[+tense] -> 'does'",
            lambda word: lambda verb_frame:\
                verb_frame.addFeature("tense", "present"))

sem.add_rule("Be[+tense] -> 'is'",
            lambda word: lambda verb_frame:\
                verb_frame.addFeature("tense", "present"))

sem.add_rule("Be[+tense] -> 'was'",
            lambda word: lambda verb_frame:\
                verb_frame.addFeature("tense", "past"))

sem.add_rule("Modal -> 'can'",
            lambda word: lambda verb_frame:\
                verb_frame.addFeature("mood", "can").addFeature("tense", "present"))

sem.add_rule("To -> 'to'",
            lambda word: lambda: None)

sem.add_rule("That -> 'that'",
            lambda word: lambda: None)

sem.add_rule("Comp[+wh] -> 'whether'",
            lambda word: lambda: None)

sem.add_rule("NP[-wh, +pro] -> 'somebody'",
            lambda word: C("Object"))

##############################################################################

#John gave Mary Fido.
sem.add_rule("V_args -> V3[+tense] NP[-wh] NP[-wh]",
             lambda v3, np1, np2: lambda subj: v3(subj, np1, np2))

#John did give Mary Fido. and Did John give Mary Fido?
sem.add_rule("VBAR[+fin] -> V3[-tense] NP[-wh] NP[-wh]",
             lambda v3, np1, np2: lambda subj: v3(subj, np1, np2))

# What did John give Mary?
sem.add_rule("VBAR[+fin]/NP -> V3[-tense] NP NP/NP",
            lambda v3, np1, np2: lambda subj, patient:\
                v3(subj, np1, patient))


# John saw the woman who caught Fido.
sem.add_rule("NP -> NP Q[+wh]", lambda np, q: np)

# Susan saw the man that Poirot ate.
sem.add_rule("NP[-wh] -> NP[-wh] SBAR_that", lambda np, sbar: np)

