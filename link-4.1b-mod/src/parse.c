/********************************************************************************/
/* Copyright (c) 2004                                                           */
/* Daniel Sleator, David Temperley, and John Lafferty                           */
/* All rights reserved                                                          */
/*                                                                              */
/* Use of the link grammar parsing system is subject to the terms of the        */
/* license set forth in the LICENSE file included with this software,           */ 
/* and also available at http://www.link.cs.cmu.edu/link/license.html           */
/* This license allows free redistribution and use in source and binary         */
/* forms, with or without modification, subject to certain conditions.          */
/*                                                                              */
/********************************************************************************/

 /****************************************************************************
 *  
 *   This is a simple example of the link parser API.  It similates most of
 *   the functionality of the original link grammar parser, allowing sentences
 *   to be typed in either interactively or in "batch" mode (if -batch is
 *   specified on the command line, and stdin is redirected to a file).
 *   The program:
 *     Opens up a dictionary
 *     Iterates:
 *        1. Reads from stdin to get an input string to parse
 *        2. Tokenizes the string to form a Sentence
 *        3. Tries to parse it with cost 0
 *        4. Tries to parse with increasing cost
 *     When a parse is found:
 *        1. Extracts each Linkage
 *        2. Passes it to process_some_linkages()
 *        3. Deletes linkage
 *     After parsing each Sentence is deleted by making a call to 
 *     sentence_delete.
 *     
 ****************************************************************************/


#include "link-includes.h"
#include "command-line.h"

#define MAXINPUT 1024
#define DISPLAY_MAX 1024
#define COMMENT_CHAR '%'  /* input lines beginning with this are ignored */

static int batch_errors = 0;
static int input_pending=FALSE;
static Parse_Options  opts;
static Parse_Options  panic_parse_opts;

typedef enum {UNGRAMMATICAL='*', 
	      PARSE_WITH_DISJUNCT_COST_GT_0=':',
	      NO_LABEL=' '} Label;


/**************************************************************************
*  
*  This procedure displays a linkage graphically.  Since the diagrams 
*  are passed as character strings, they need to be deleted with a 
*  call to string_delete.
*
**************************************************************************/

int there_was_an_error(Label label, Sentence sent, Parse_Options opts) {

    if (sentence_num_valid_linkages(sent) > 0) {
	if (label == UNGRAMMATICAL) {
	    batch_errors++;
	    return UNGRAMMATICAL;
	}
	if ((sentence_disjunct_cost(sent, 0) == 0) && 
	    (label == PARSE_WITH_DISJUNCT_COST_GT_0)) {
	    batch_errors++;
	    return PARSE_WITH_DISJUNCT_COST_GT_0;
	}
    } else {
	if  (label != UNGRAMMATICAL) {
	    batch_errors++;
	    return UNGRAMMATICAL;
	}
    }
    return FALSE;
}


void print_usage(char *str) {
    fprintf(stderr, 
	    "Usage: %s [dict_file] [-pp pp_knowledge_file]\n"
	    "          [-c constituent_knowledge_file] [-a affix_file]\n"
	    "          [-ppoff] [-coff] [-aoff] [-batch] [-<special \"!\" command>]\n", str);
    exit(-1);
}


int main(int argc, char * argv[]) {

    Dictionary      dict;
    Parse_Options   opts;
    Sentence        sent;
    Linkage         Linkage;
    char            *sentence;
    int             num_linkages, i;

    opts  = parse_options_create();
    dict  = dictionary_create("4.0.dict", "4.0.knowledge", NULL, "4.0.affix");

    FILE *in = fopen("./input.txt","r");
    FILE *out = fopen("./output.txt","w+");
    char buff[255];

    while ( fgets ( buff, sizeof buff, in ) != NULL ) {
        //printf("%s", buff);
        sentence = buff;
        sent = sentence_create(sentence, dict);
        num_linkages = sentence_parse(sent, opts); 
        if (num_linkages > 0) {
            fprintf(out, "%s\n", sentence);
        }
    }

    fclose(in);
    fclose(out);

    return 0;

}
