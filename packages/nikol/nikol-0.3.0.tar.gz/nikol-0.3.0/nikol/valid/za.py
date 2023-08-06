# za.py
#
# from scripts/valid-2-za.py
#
# Author: yhj
#
# WARNING: Use this script only for *Subject* ZA Corpus.
#
"""
Validation Level 2 of ZA corpus

Usage: valid-2-za nxza.json 


JSON
================

ZA
  predicate : {form, sentence_id, begin, end}
  antecedent : [ {form, type, sentence_id, begin, end} ]

"""
import re
from . import util

def valid_za(document):
    """
    document: koltk.corpus.nikl.annotated.object.Document
    """
    if not hasattr(document, 'ZA') :
        return None

    for za in document.za_list:
        za._error = []

        if len(za.antecedent) > 1 :
            raise Exception('There are more than two antecedents. Use this script only for subject ZA corpus!')

        pred = za.predicate
        subj = za.antecedent[0]
        
        if subj.type != 'subject':
            raise Exception('Non-subject antecedent. Use this script only for subject ZA corpus!')
            

        #
        # check predicate form and begin:end
        #
        sentence = document.getSentenceById(pred.sentence_id)
        try:
            word = sentence.wordAt(pred.begin)
        except:
            # if no word at pred.begin (i.e. if whitespace at pred.begin)
            # then choose the left word
            word = sentence.wordAt(pred.begin - 1)
            za._error.append('ErrorZAPredicateFormBeginEnd();')
            
        word._za = za

        if sentence.form[pred.slice] != pred.form:
            za._error.append('ErrorZAPredicateFormBeginEnd();')

        #
        # check predicate form
        #
        if word.form.find(pred.form) == -1:
            if sentence.form[pred.slice] != pred.form:
                za._error.append('ErrorZAPredicatForm();')

        if pred.form != word.form:
            
            if re.search('[와과]', word.form) and \
               word.form[:-1] == pred.form: continue
            if re.search('[”’\'"]고$', word.form) and \
               word.form[:-2] == pred.form: continue
            if word.form.strip('.,?!\'"“”‘’…') == pred.form : continue
            if re.sub('[^가-힣]', '', word.form) == pred.form : continue
            
            za._error.append('ErrorZAPredicateForm();')


        
        if pred.form.endswith('”고') :
            za._error.append('ErrorZAPredicatForm(”고/JKQ);')

        #
        # check predicate form: quotation marks and parentheses
        #
        # ‘ 0x2018
        # ’ 0x2019
        # “ 0x201c
        # ” 0x201D
        # ' 0x27
        #
        # () <> []
        #
        # Error if
        # - predicate form has only one quotation mark/parenthesis
        # - and word form has both quotation marks/parentheses
        pred_split = re.split('[\'"“”‘’()<>{}\[\]]', pred.form)
        word_split = re.split('[\'"“”‘’()<>{}\[\]]', word.form)
        n = len(word_split) - len(pred_split)
        if len(pred_split) > 1 and n != 0:
            za._error.append('ErrorZAPredicatForm(QuoteParenMatch);')



        #
        # check if subject form is empty
        #
        if subj.form == '' :
            za._error.append('ErrorZAAntecedentForm(Empty);')
            
        #
        # check subject form and begin:end
        #
        if subj.sentence_id != '-1':
            s = document.getSentenceById(subj.sentence_id)
            if s.form[subj.slice].strip() == '':
                za._error.append('ErrorZAAntecedentFormBeginEnd();')
            elif s.form[subj.slice] != subj.form:
                if util.form_match(subj.form, s.form[subj.slice]): continue
                za._error.append('ErrorZAAntecedentFormBeginEnd({})'.format(s.form[subj.slice]))

def table(document, spec='min', valid=False):
    """
    document: koltk.corpus.nikl.annotated.object.Document
    """
 
    if spec == 'min':
        return table_min(document, valid=valid)
    else:
        return table_full(document, valid=valid)
        
    
def table_full(document, valid=False):
    """
    document: koltk.corpus.nikl.annotated.object.Document
    """
 
    valid_za(document)
    rows = []
    for sentence in document.sentence_list:
        for word in sentence.word_list:
            if hasattr(word, '_za'):
                pred = word._za.predicate
                ante = word._za.antecedent[0]
                if ante.sentence_id != '-1':
                    ante_sent = document.getSentenceById(ante.sentence_id)
                    ante_sent_fwid = ante_sent.fwid
                else:
                    ante_sent_fwid = '-1'

                pred_form = pred.form
                pred_slice_str = pred.slice_str
                ante_form = ante.form
                ante_type = ante.type
                ante_slice_str = ante.slice_str
                za_errors = ''.join(word._za._error)
            else:
                ante_sent_fwid = ''
                pred_form = ''
                pred_slice_str = ''
                ante_form = ''
                ante_type = ''
                ante_slice_str = ''
                za_errors = ''
                
            rows.append('\t'.join([
                sentence.fwid,
                word.slice_str,
                str(word.id),
                word.form,
                pred_form,
                pred_slice_str,
                ante_form,
                ante_type,
                ante_sent_fwid,
                ante_slice_str,
                za_errors
            ]))

    return '\n'.join(rows)
 

def table_min(document, valid=False):
    """
    document: koltk.corpus.nikl.annotated.object.Document
    """
 
    valid_za(document)
    rows = []
    for sentence in document.sentence_list:
        for word in sentence.word_list:
            if hasattr(word, '_za'):
                pred = word._za.predicate
                ante = word._za.antecedent[0]
                if ante.sentence_id != '-1':
                    ante_sent = document.getSentenceById(ante.sentence_id)
                    ante_sent_fwid = ante_sent.snum
                    try:
                        ante_word = ante_sent.wordAt(ante.begin)
                        ante_word_id = '{}_{}'.format(ante_sent_fwid, ante_word.id)
                    except:
                        ante_word_id = '{}_*begin{}'.format(ante_sent_fwid, ante.begin)
                else:
                    ante_sent_fwid = '-1'
                    ante_word_id = '-1'

                pred_form = pred.form
                ante_str = '{}__@{}'.format(ante.form, ante_word_id)
                za_errors = ''.join(word._za._error)
            else:
                pred_form = ''
                ante_str = ''
                za_errors = ''

            fields = [
                word.gid,
                word.swid,
                word.form,
                pred_form,
                ante_str
            ]
            if valid: fields.append('### ' + za_errors)

            rows.append('\t'.join(fields))

    return '\n'.join(rows)


       
    
