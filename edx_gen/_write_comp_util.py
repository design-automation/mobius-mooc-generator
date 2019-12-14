import sys, os
from lxml import etree
#--------------------------------------------------------------------------------------------------
WARNING = "      WARNING:"

#--------------------------------------------------------------------------------------------------
def addChoiceTag(choices, elem, filename):

    text = elem.text.strip()

    if text[:3] in ['[ ]', '[x]']:
        
        # is this choice correct?
        correct_val = 'true'
        if text[:3] == '[ ]':
            correct_val = 'false'

        # get the start of the hint
        hint_start = -1
        if text.endswith('}'):
            index = text.rfind('{')
            if index != -1:
                hint_start = index + 1

        hint_end = len(text) - 1

        # get the end of the choice text
        choice_start = 3
        choice_end = len(text)
        if hint_start != -1:
            choice_end = hint_start - 1
        
        # create the tag
        choice_tag = etree.Element("choice")
        choice_tag.text = text[choice_start:choice_end]
        choice_tag.set('correct', correct_val)
        if hint_start != -1:
            choicehint_tag = etree.Element("choicehint")
            choicehint_tag.text = text[hint_start:hint_end]
            choice_tag.append(choicehint_tag)
        choices.append(choice_tag)
    else:
        print(WARNING, 'Submit problem choice must start with [ ] or [x].', filename)

#--------------------------------------------------------------------------------------------------
def addHintTag(hints, elem, filename):
    hint_tag = etree.Element("hint")
    hint_tag.text = elem.text
    hints.append(hint_tag)

#--------------------------------------------------------------------------------------------------
