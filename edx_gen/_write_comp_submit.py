import sys, os
from lxml import etree
from edx_gen import  _edx_consts
from edx_gen import  _process_html
from edx_gen import  _css_settings
from edx_gen import  _mob_iframe
import __SETTINGS__
#--------------------------------------------------------------------------------------------------
WARNING = "      WARNING:"

SUBMIT_EXAMPLE_DESCRIPTION = [
    'Below is an example of the output that your Mobius Model will need to be able to generate. ' + 
    'This example model does not include the procedure. ' + 
    'That is the part you need to figure out.' +
    'If you open the paremeters, you will see the values that were used to generate this version of the model.' +
    'If you open the settings, you will be able to switch on the GI Summary and see ' + 
    'the number of geometric entities that have been generated.'][0]

SUBMIT_INSTRUCTIONS = [
    'Please submit your Mobius Model. ' + 
    'First create your answer model and save it to your local drive. ' + 
    'Then click Submit and select your .mob file. ' + 
    'Your submission will be auto-graded and you should receiev the results within a few seconds.'][0]

#--------------------------------------------------------------------------------------------------
# write xml for problem submit
def writeXmlForSubmitComp(component_path, filename, content, settings, unit_filename):

    # ----  ----  ----
    # <problem 
    #       attempts_before_showanswer_button="1" 
    #       display_name="Task 1: Submission" 
    #       markdown="null" 
    #       max_attempts="1" 
    #       showanswer="finished" 
    #       weight="1.0">
    #   <coderesponse queuename="mooc_queue_name_on_edx_server">
    #       <label>Submit your Mobius Modeller file here.</label>
    #       <filesubmission/>
    #       <codeparam>
    #           <grader_payload>
    #               {"question": "SCT_W5_Assignment"}
    #           </grader_payload>
    #       </codeparam>
    #       <solution>
    #           <iframe src="https://mobius.design-automation.net/gallery" style="width: 100%; height: 600px; border: 1px solid black;">Your Browser does not support iFrame</iframe>
    #       </solution>
    #   </coderesponse>
    # </problem>
    # ----  ----  ----

    # make the xml
    from lxml import etree
    problem_tag = etree.Element("problem") 
    coderesponse_tag = etree.Element("coderesponse")
    problem_tag.append( coderesponse_tag )

    # process the settings
    for key in settings:
        if key not in ['type', 'answer_filename', 'example_filename', 'display_name']:
            problem_tag.set(key, settings[key])

    # override display name
    problem_tag.set('display_name', 'Submit Your Mobius File')

    # grader queue
    queuename = __SETTINGS__.EDX_EXTERNAL_GRADER_QUEUENAME
    coderesponse_tag.set('queuename', queuename)

    # check the file
    answer_filename = ''
    if 'answer_filename' in settings:

        # get the filename
        answer_filename = settings['answer_filename'].strip()

        # check that that the file exists
        component_dir = os.path.dirname(component_path)
        answer_filepath = os.path.normpath(component_dir + '/' + answer_filename)
        if (not os.path.exists(answer_filepath) or not os.path.isfile(answer_filepath)):
            print(WARNING, 'The answer file does not exist: "' + answer_filepath +'" in', component_path)

    else:
        print(WARNING, 'Submit problem is missing "answer".', unit_filename)

    # construct the question name from the answer file name
    question = __SETTINGS__.S3_MOOC_FOLDER + '/' + unit_filename + '_' + answer_filename.split('.')[0]

    # payload for grader
    grader_payload_tag = etree.Element("grader_payload")
    grader_payload_tag.text = '{"question": "' + question + '"}'

    # process html
    _process_html.processHtmlTags(component_path, content, unit_filename)

    # create tags for description and solution
    problem_description_tag = etree.Element("div")
    problem_solutions_tag = etree.Element("div") 

    # set the display name for the description tag
    display_name = 'Mobius Modelling Assignment'
    if 'display_name' in settings:
        display_name = settings['display_name']
    problem_description_tag.set('display_name', display_name)

    # add an h1 heading to the description tag
    h1_tag = etree.Element("h1")
    h1_tag.text = display_name
    problem_description_tag.append(h1_tag)

    # process the elements
    # these will be saved in the problem_description_tag and as solution <p> elements
    # the elements are spli using '==='
    # everything before the split is added to <label>
    # everything after the split is added to 

    found_splitter = 0 # found ===
    elems = content.getchildren()
    if elems:
        for elem in elems:
            if (elem.text and elem.text.startswith('===')):
                found_splitter += 1
            else:
                if found_splitter == 0:
                    problem_description_tag.append(elem)
                else:
                    problem_solutions_tag.append(elem)
    else:
        print(WARNING, 'Submit problem is missing content.', unit_filename)

    # if there is an example model, add a mobius iframe
    if 'example_filename' in settings:

        # get the filename
        example_filename = settings['example_filename'].strip()

        # check that that the file exists
        component_dir = os.path.dirname(component_path)
        example_filepath = os.path.normpath(component_dir + '/' + example_filename)
        if (not os.path.exists(example_filepath) or not os.path.isfile(example_filepath)):
            print(WARNING, 'The example file does not exist: "' + example_filepath +'" in', component_path)

        # heading
        h2_tag = etree.Element("h2")
        h2_tag.text = 'Example Model'
        problem_description_tag.append(h2_tag)
        
        # the example model description text
        example_descr_p_tag = etree.Element("p")
        example_descr_p_tag.text = SUBMIT_EXAMPLE_DESCRIPTION
        problem_description_tag.append(example_descr_p_tag)

        # the example model iframe
        mob_settings = {
            'mobius':'publish',
            'showView':'1'
        }
        iframe_tag = _mob_iframe.createMobIframe(example_filename, mob_settings, unit_filename)
        problem_description_tag.append(iframe_tag)

    # convert problem_description_data to string
    problem_desc_data = etree.tostring(problem_description_tag, pretty_print=True)

    # write the file for the problem_description
    prob_xml_out_path = os.path.join(sys.argv[2], _edx_consts.COMP_HTML_FOLDER, filename + '.xml')
    with open(prob_xml_out_path, 'wb') as fout:
        fout.write(problem_desc_data)

    # add labels to the coderesponse_tag
    label_tag = etree.Element("label") 
    coderesponse_tag.append(label_tag)

    # add the instruction text
    instruct_p_tag = etree.Element("div") # dont use p, it results in small text
    instruct_p_tag.text = SUBMIT_INSTRUCTIONS
    label_tag.append(instruct_p_tag)

    # add <filesubmission> and <codeparam> to the coderesponse_tag
    coderesponse_tag.append(etree.Element("filesubmission") )
    codeparam_tag = etree.Element("codeparam")
    codeparam_tag.append(grader_payload_tag)
    coderesponse_tag.append(codeparam_tag)

    # add <solution> to the coderesponse_tag
    solution_tag = etree.Element("solution")
    coderesponse_tag.append(solution_tag)
    solution_tag.append(problem_solutions_tag)

    # convert problem_tag to string
    prob_data = etree.tostring(problem_tag, pretty_print=True)

    # write the file
    prob_xml_out_path = os.path.join(sys.argv[2], _edx_consts.COMP_PROBS_FOLDER, filename + '.xml')
    with open(prob_xml_out_path, 'wb') as fout:
        fout.write(prob_data)

    # return the file name and folder
    return [
        [filename, _edx_consts.COMP_HTML_FOLDER], 
        [filename, _edx_consts.COMP_PROBS_FOLDER]
    ]

#--------------------------------------------------------------------------------------------------
