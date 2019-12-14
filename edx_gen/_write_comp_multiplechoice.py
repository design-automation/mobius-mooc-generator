import sys, os
from lxml import etree
from edx_gen import  _edx_consts
from edx_gen import  _process_html
from edx_gen import  _css_settings
from edx_gen import  _mob_iframe
from edx_gen import  _write_comp_util
import __SETTINGS__

#--------------------------------------------------------------------------------------------------
WARNING = "      WARNING:"

MULTIPLECHOICE_INSTRUCTIONS = [
    'Please select one option from the list below. '][0]

#--------------------------------------------------------------------------------------------------
# write xml for problem Checkboxescomponent
def writeXmlForProbMultiplechoiceComp(component_path, filename, content, settings, unit_filename):

    # ----  ----  ----
    # <problem 
    #   display_name="Q1"  
    #   max_attempts="3" 
    #   rerandomize="onreset" 
    #   weight="1.8"
    #   showanswer="attempted" 
    #   attempts_before_showanswer_button="3" 
    # >
    # 	<multiplechoiceresponse>
    # 		<p>You can use this template as a guide to the simple editor markdown and OLX markup to use for multiple choice with hints and feedback problems. Edit this component to replace this template with your own assessment.</p>
    # 		<label>Add the question text, or prompt, here. This text is required.</label>
    # 		<description>Please select one option from the list below.</description>
    # 		<choicegroup type="MultipleChoice">
    # 			<choice correct="false">
    #               an incorrect answer 
    #               <choicehint>You can specify optional feedback like this, which appears after this answer is submitted.</choicehint>
    # 		    </choice>
    # 			<choice correct="true">
    #               the correct answer
    #           </choice>
    # 			<choice correct="false">
    #               an incorrect answer 
    #               <choicehint>You can specify optional feedback for none, a subset, or all of the answers.</choicehint>
    # 		    </choice>
    # 		</choicegroup>
    # 	</multiplechoiceresponse>
    # 	<demandhint>
    # 	  <hint>You can add an optional hint like this. Problems that have a hint include a hint button, and this text appears the first time learners select the button.</hint>
    # 	  <hint>If you add more than one hint, a different hint appears each time learners select the hint button.</hint>
    # 	</demandhint>
    # </problem>
    # ----  ----  ----

    # make the xml
    problem_tag = etree.Element("problem") 
    multiplechoiceresponse_tag = etree.Element("multiplechoiceresponse")
    problem_tag.append( multiplechoiceresponse_tag )

    # process the settings
    for key in settings:
        if key not in ['type']:
            problem_tag.set(key, settings[key])

    # process html
    _process_html.processHtmlTags(component_path, content, unit_filename)

    # process the elements
    # these will be converted to <label>, and solution <p> elements
    # the elements are split using '===', there should be two splits
    labels = []
    choices = []
    hints = []
    solutions = []
    found_splitter = 0 # found ===
    elems = content.getchildren()
    if elems:
        for elem in elems:
            if (elem.text and elem.text.startswith('===')):
                found_splitter += 1
            else:
                if found_splitter == 0:
                    labels.append(elem)
                elif found_splitter == 1:
                    _write_comp_util.addChoiceTag(choices, elem, filename)
                elif found_splitter == 2:
                    solutions.append(elem)
                else:
                    _write_comp_util.addHintTag(hints, elem, filename)
    else:
        print(WARNING, 'Multiplechoice problem is missing content.', filename)

    # add labels
    if labels:
        label_tag = etree.Element("label") 
        multiplechoiceresponse_tag.append(label_tag)
        for label in labels:
            label_tag.append(label)
    else:
        print(WARNING, 'Multiplechoice problem seems to have no text that describes the question.', filename)
    
    # add instructions
    description_tag = etree.Element("description")
    multiplechoiceresponse_tag.append(description_tag)
    description_tag.text = MULTIPLECHOICE_INSTRUCTIONS

    # add choices
    if choices:
        choicegroup_tag = etree.Element("choicegroup")
        multiplechoiceresponse_tag.append(choicegroup_tag)
        for choice in choices:
            choicegroup_tag.append(choice)
    else:
        print(WARNING, 'Multiplechoice problem seems to have no choices.', filename)

    # add solutions
    if solutions:
        solution_tag = etree.Element("solution")
        div_tag = etree.Element("div")
        div_tag.set('class', 'detailed-solution')
        multiplechoiceresponse_tag.append(solution_tag)
        solution_tag.append(div_tag)
        for solution in solutions:
            div_tag.append(solution)
    else:
        pass # It is ok to have no solution

    # add hints
    if hints:
        demandhint_tag = etree.Element("demandhint")
        problem_tag.append(demandhint_tag)
        for hint in hints:
            demandhint_tag.append(hint)
    else:
        pass # It is ok to have no hints

    # convert problem_tag to string
    result = etree.tostring(problem_tag, pretty_print=True)

    # write the file
    xml_out_path = os.path.join(sys.argv[2], _edx_consts.COMP_PROBS_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)

    # return the file name and folder
    return [[filename, _edx_consts.COMP_PROBS_FOLDER]]
#--------------------------------------------------------------------------------------------------
