import os
from lxml import etree
import __CONSTS__ 
import _edx_consts
import _process_html
import _css_settings
import _mob_iframe
#--------------------------------------------------------------------------------------------------
WARNING = "      WARNING:"

CHECKBOXES_INSTRUCTIONS = [
    'Please select all applicable options from the list below. ' + 
    'Multiple selections are allowed.'][0]

SUBMIT_EXAMPLE_DESCRIPTION = [
    'Below is an example of the output that you need to submit. ' + 
    'This model does not include the procedure. ' + 
    'That is the part you need to figure out.' +
    'If you look at the paremeters, you will see the values that were used to generate this version of the model.'][0]

SUBMIT_INSTRUCTIONS = [
    'Please submit your Mobius Model. ' + 
    'First create your answer model and save it to your local drive. ' + 
    'Then click Submit and select your .mob file. ' + 
    'Your submission will be auto-graded and you should receiev the results within a few seconds.'][0]

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
    #           <choice correct="false">Some text. </choice>
    #           <choice correct="false">Some text. </choice>
    #           <choice correct="true">Some text. </choice>
    #       </checkboxgroup>
    #       <solution>
    #           <div class="detailed-solution">
    #               <p>Explanation</p>
    #               <p>xxx</p>
    #           </div>
    #       </solution>
    #   </choiceresponse>
    # </problem>
    # ----  ----  ----

    # make the xml
    problem_tag = etree.Element("problem") 
    choiceresponse_tag = etree.Element("choiceresponse")
    problem_tag.append( choiceresponse_tag )

    # process the settings
    for key in settings:
        if key not in ['type']:
            problem_tag.set(key, settings[key])

    # process html
    _process_html.processHtmlTags(content, unit_filename)

    # process the elements
    # these will be converted to <label>, and solution <p> elements
    # the elements are split using '===', there should be two splits
    labels = []
    choices = []
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
                    if elem.text[:3] in ['[ ]', '[x]']:
                        correct_val = 'true'
                        if elem.text[:3] == '[ ]':
                            correct_val = 'false'
                        choice_tag = etree.Element("choice")
                        choice_tag.text = elem.text[3:]
                        choice_tag.set('correct', correct_val)
                        choices.append(choice_tag)
                    else:
                        print(WARNING, 'Submit problem choice must start with [ ] or [x].', filename)
                else:
                    solutions.append(elem)
    else:
        print(WARNING, 'Submit problem is missing content.', filename)

    # add the choices and solutions to the choiceresponse_tag
    if labels:
        label_tag = etree.Element("label") 
        choiceresponse_tag.append(label_tag)
        for label in labels:
            label_tag.append(label)
    else:
        print(WARNING, 'Choice problem seems to have no text that describes the question.', filename)
    if CHECKBOXES_INSTRUCTIONS:
        description_tag = etree.Element("description")
        choiceresponse_tag.append(description_tag)
        description_tag.text = CHECKBOXES_INSTRUCTIONS
    if choices:
        checkboxgroup_tag = etree.Element("checkboxgroup")
        choiceresponse_tag.append(checkboxgroup_tag)
        for choice in choices:
            checkboxgroup_tag.append(choice)
    else:
        print(WARNING, 'Choice problem seems to have no choices.', filename)
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

    # convert problem_tag to string
    result = etree.tostring(problem_tag, pretty_print=True)

    # write the file
    xml_out_path = os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.COMP_PROBS_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)

    # return the file name and folder
    return [[filename, _edx_consts.COMP_PROBS_FOLDER]]
#--------------------------------------------------------------------------------------------------
