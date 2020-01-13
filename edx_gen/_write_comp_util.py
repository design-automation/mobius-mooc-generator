import sys, os
from lxml import etree
#--------------------------------------------------------------------------------------------------
WARNING = "      WARNING:"

#--------------------------------------------------------------------------------------------------
def addChoiceTag(choices, elem, filename):

    text = elem.text.strip()

    text_elems = []
    if len(elem.getchildren()) > 0:
        for child in elem.getchildren():
            text_elems.append(child)


    if text[:3] in ['[ ]', '[x]']:
        
        # is this choice correct?
        correct_val = 'true'
        if text[:3] == '[ ]':
            correct_val = 'false'

        # check if we have a hint
        if text_elems:
            tail = text_elems[-1].tail
            if tail and tail.strip().endswith('}'):
                print(WARNING, 'Submit problem choice has a hint. NOT IMPLEMENTED.', filename)

        # # get the start of the hint
        # end_text = text
        # if len(text_elems) > 0:
        #     end_text = text_elems[-1].tail
        # has_hint = False
        # hint_text = ''
        # if end_text.strip().endswith('}'):
        #     hint_start_idx = end_text.rfind('{')
        #     if hint_start_idx != -1:
        #         hint_text = end_text[hint_start_idx:]
        #         has_hint = True
        #         text_elems = text_elems[:-1]

        # create the tag
        choice_tag = etree.Element("choice")
        choice_tag.text = text[3:]
        for text_elem in text_elems:
            choice_tag.append(text_elem)
        choice_tag.set('correct', correct_val)
        # if has_hint:
        #     choicehint_tag = etree.Element("choicehint")
        #     choicehint_tag.text = hint_text
        #     choice_tag.append(choicehint_tag)
        choices.append(choice_tag)
    else:
        print(WARNING, 'Submit problem choice must start with [ ] or [x].', filename)

#--------------------------------------------------------------------------------------------------
def addHintTag(hints, elem, filename):
    hint_tag = etree.Element("hint")
    hint_tag.text = elem.text
    hints.append(hint_tag)

#--------------------------------------------------------------------------------------------------
