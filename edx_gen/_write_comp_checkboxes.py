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

CHECKBOXES_INSTRUCTIONS = [
    'Please select all applicable options from the list below. ' + 
    'Multiple selections are allowed.'][0]

#--------------------------------------------------------------------------------------------------
# write xml for problem Checkboxescomponent
def writeXmlForProbCheckboxesComp(component_path, filename, content, settings, unit_filename):

    # ----  ----  ----
    # <problem 
    #   display_name="Q2" 
    #   max_attempts="2" 
    #   rerandomize="always" 
    #   weight="1.0"
    # >
    #   <choiceresponse>
    #       <label>xxx, which of the following are true?</label>
    #       <description>Please select all applicable options from the list below. Multiple selections are allowed. </description>
    #       <checkboxgroup>
    #           <choice correct="false">
    #               Some text. 
    #               <choicehint selected="true">Feedback.</choicehint>
    #           </choice>
    #           <choice correct="false">
    #               Some text. 
    #               <choicehint selected="true">Feedback.</choicehint>
    #           </choice>
    #           <choice correct="true">Some text. </choice>
    #       </checkboxgroup>
    #       <solution>
    #           <div class="detailed-solution">
    #               <p>Explanation</p>
    #               <p>xxx</p>
    #           </div>
    #       </solution>
    #       <demandhint>
    #           <hint>Hint.</hint>
    #           <hint>Another hint.</hint>
    #       </demandhint>
    #   </choiceresponse>
    # </problem>
    # ----  ----  ----

    # make the xml
    problem_tag = etree.Element("problem") 
    choiceresponse_tag = etree.Element("choiceresponse")
    problem_tag.append( choiceresponse_tag )

    # process the settings
    for key in settings:
        if key not in ['type', 'verified_only', 'id']:
            problem_tag.set(key, settings[key])

    # verified_only
    if 'verified_only' in settings and settings['verified_only'] == 'true':
        problem_tag.set('group_access', '{"50":[2]}')

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
        print(WARNING, 'Checkboxes problem is missing content.', filename)

    # add labels
    if labels:
        label_tag = etree.Element("label") 
        choiceresponse_tag.append(label_tag)
        for label in labels:
            label_tag.append(label)
    else:
        print(WARNING, 'Checkboxes problem seems to have no text that describes the question.', filename)

    # add instructions
    description_tag = etree.Element("description")
    choiceresponse_tag.append(description_tag)
    description_tag.text = CHECKBOXES_INSTRUCTIONS

    # add choices
    if choices:
        checkboxgroup_tag = etree.Element("checkboxgroup")
        choiceresponse_tag.append(checkboxgroup_tag)
        for choice in choices:
            checkboxgroup_tag.append(choice)
    else:
        print(WARNING, 'Checkboxes problem seems to have no choices.', filename)

    # add solutions
    if solutions:
        solution_tag = etree.Element("solution")
        div_tag = etree.Element("div")
        div_tag.set('class', 'detailed-solution')
        choiceresponse_tag.append(solution_tag)
        solution_tag.append(div_tag)
        for solution in solutions:
            div_tag.append(solution)
    else:
        pass # It is ok to have no solution text

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

    # check if we have id
    if 'id' in settings:
        filename = settings['id']

    # write the file
    xml_out_path = os.path.join(sys.argv[2], _edx_consts.COMP_PROBS_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)

    # return the file name and folder
    return [[filename, _edx_consts.COMP_PROBS_FOLDER]]
#--------------------------------------------------------------------------------------------------
