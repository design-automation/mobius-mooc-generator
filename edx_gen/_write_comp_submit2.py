import sys, os
from lxml import etree
from edx_gen import  _edx_consts
from edx_gen import  _process_html
from edx_gen import  _css_settings
from edx_gen import  _mob_iframe
import __SETTINGS__
#--------------------------------------------------------------------------------------------------
WARNING = "      WARNING:"

SUBMIT_PRELUDE = '' + \
    'Below is the example model and the base codescript for this assignment.'

SUBMIT_PRELUDE_BULLETS = [
    "Explore the example model and get an understanding of the geometric entities your codescript needs to generate.",
    "Go to the base model below and add your code.",
    "Click 'execute' and check the resulting geometric entities match the example model.",
    "Save your Mobius codescript file (.mob) on your computer.",
    "Scroll down to the Submit button below, click the 'Choose Files' button, and select your saved file (.mob) and click 'submit'."
    ]

SUBMIT_EXAMPLE_DESCRIPTION = '' + \
    'This is an example of the output that your Mobius codescript will need to generate for this assignment. ' + \
    'This example only contains the output geometry, it does not include the codescript. ' + \
    'If you open the parameters, you will see the values that were used to generate this output.'

SUBMIT_BASE_DESCRIPTION = '' + \
    'This is the base file that you should use to create your answer for this assignment. '+ \
    'Add your code to this base file save it.'

SUBMIT_INSTRUCTIONS = '' + \
    'Please submit your Mobius codescript. ' + \
    'Your submission will be auto-graded and you should receive the results within a few seconds.'

#--------------------------------------------------------------------------------------------------
# write xml for problem submit
def writeXmlForSubmitComp(component_path, filename, content, settings, unit_filename):

    # ----  HTML file in COMP_HTML_FOLDER ----
    # <h3 style="font-size: 22px;font-weight: 400;font-style: normal;color: #474747">
    # Assignment Model: Parametric Building </h3>
    # <p> This is your first modelling assignment for the Procedural Modelling course. It is worth
    # <strong> 10 % </strong>.</p>
    # <p> Please make sure that you have attempted the demo assignment in the previous section. That will give you a good sense of how the grader works.</p>
    # <p> For this assignment, you need to create a codescript that generates a parametric massing model consisting of a podium with a tower on top. For a description of the required model, see the previous page.</p>
    # <p> In the base model below, the flowchart parameters have already been defined and the code for generating the podium has already been created for you. You need to add code to generate the tower.</p>
    # <h4 style="font-size: 20px;font-weight: 400;font-style: italic;color: #474747"> Completing the Assignment </h4>
    # <p> Below is the example model and the base codescript for this assignment.</p>
    # <ul>
    #   <li> Explore the example model and get an understanding of the geometric entities your codescript needs to generate.</li>
    #   <li> Go to the base model below and add your code.</li>
    #   <li> Click 'execute' and check the resulting geometric entities match the example model.</li>
    #   <li> Save your Mobius codescript file(.mob) on your computer.</li>
    #   <li> Scroll down to the Submit button below, click the 'Choose Files' button, and select your saved file(.mob) and click 'submit'.</li>
    # </ul>
    # <h4 style="font-size: 20px;font-weight: 400;font-style: italic;color: #474747"> Example Model </h4>
    # <p> This is an example of the output that your Mobius codescript will need to generate for this assignment. This example only contains the output geometry, it does not include the codescript. If you open the parameters, you will see the values that were used to generate this output.</p>
    # <div>
    #   <iframe width="100%" height="600px" style="border-style:solid;border-width:4px;border-color:#065683" src="https://design-automation.github.io/mobius-parametric-modeller-dev-0-8/publish?file=https://mooc-s3cf.s3-ap-southeast-1.amazonaws.com/procedural_modelling_v3/mob_examples/w1_s7_u2_assign_building_exp.mob&amp;showView=1"> Mobius Modeller </iframe>
    #   <p>
    #     <a href="https://design-automation.github.io/mobius-parametric-modeller-dev-0-8/publish?file=https://mooc-s3cf.s3-ap-southeast-1.amazonaws.com/procedural_modelling_v3/mob_examples/w1_s7_u2_assign_building_exp.mob&amp;showView=1" target="Mobius"> Open Mobius in a separate browser tab.</a>
    #   </p>
    # </div>
    # <h4 style="font-size: 20px;font-weight: 400;font-style: italic;color: #474747"> Base Codescript </h4>
    # <p> This is the base file that you should use to create your answer for this assignment. Add your code to this base file save it.</p>
    # <div>
    #   <iframe width="100%" height="600px" style="border-style:solid;border-width:4px;border-color:#065683" src="https://design-automation.github.io/mobius-parametric-modeller-dev-0-8/editor?file=https://mooc-s3cf.s3-ap-southeast-1.amazonaws.com/procedural_modelling_v3/mob_examples/w1_s7_u2_assign_building_base.mob&amp;showView=1&amp;node=1"> Mobius Modeller </iframe>
    #   <p>
    #     <a href="https://design-automation.github.io/mobius-parametric-modeller-dev-0-8/editor?file=https://mooc-s3cf.s3-ap-southeast-1.amazonaws.com/procedural_modelling_v3/mob_examples/w1_s7_u2_assign_building_base.mob&amp;showView=1&amp;node=1" target="Mobius"> Open Mobius in a separate browser tab.</a>
    #   </p>
    # </div>
    # ----  ----  ----

    # ----  XML file in COMP_PROBS_FOLDER ----
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
    #           <iframe src="https://mobius.design-automation.net/gallery" style="width: 100%; 
    #               height: 600px; border: 1px solid black;">Your Browser does not support iFrame</iframe>
    #       </solution>
    #   </coderesponse>
    # </problem>
    # ----  ----  ----

    # make the xml
    from lxml import etree

    # process html
    _process_html.processHtmlTags(component_path, content, unit_filename)

    # return the file name and folder
    return [
        [filename, _edx_consts.COMP_HTML_FOLDER], 
        [filename_prob, _edx_consts.COMP_PROBS_FOLDER]
    ]

#--------------------------------------------------------------------------------------------------
# split teh data
def _splutContent(component_path, filename, content, settings, unit_filename):
    pass

#--------------------------------------------------------------------------------------------------
# write file
def _writeXMLFileToForDescr(component_path, filename, content, settings, unit_filename):
    pass

#--------------------------------------------------------------------------------------------------
# write file that contains the Html component before the problem
def _writeXMLFileForProb(component_path, filename, content, settings, unit_filename):
    problem_tag = etree.Element("problem")

    # check the file
    answer_filename = ''
    if 'answer_filename' in settings:

        # get the filename
        answer_filename = settings['answer_filename'].strip()

        # check that that the file exists
        component_dir = os.path.dirname(component_path)
        answer_filepath = os.path.normpath(
            component_dir + '/' + answer_filename)
        if (not os.path.exists(answer_filepath) or not os.path.isfile(answer_filepath)):
            print(WARNING, 'The answer file does not exist: "' +
                  answer_filepath + '" in', component_path)

    else:
        print(WARNING, 'Submit problem is missing "answer".', unit_filename)

    # construct the question name from the answer file name
    question = __SETTINGS__.S3_MOOC_FOLDER + \
        '/' + __SETTINGS__.S3_ANSWERS_FOLDER + '/'
    question = question + unit_filename + '_' + answer_filename.split('.')[0]

    # payload for grader
    grader_payload_tag = etree.Element("grader_payload")
    grader_payload_tag.text = '{"question": "' + question + '"}'


    # process the settings
    for key in settings:
        if key not in ['type', 'id', 'answer_filename', 'example_filename', 'base_filename',
                'verified_only', 'display_name']:
            problem_tag.set(key, settings[key])

    # verified_only
    if 'verified_only' in settings and settings['verified_only'] == 'true':
        problem_tag.set('group_access', '{"50":[2]}')

    # override display name
    problem_tag.set('display_name', 'Submit Your Mobius File')

    # convert problem_tag to string
    prob_data = etree.tostring(problem_tag, pretty_print=True)

    # check if we have id
    filename_prob = filename
    if 'id' in settings:
        filename_prob = settings['id']

    # write the XML file to COMP_PROBS_FOLDER
    prob_xml_out_path = os.path.join(
        sys.argv[2], _edx_consts.COMP_PROBS_FOLDER, filename_prob + '.xml')
    with open(prob_xml_out_path, 'wb') as fout:
        fout.write(prob_data)
    
#--------------------------------------------------------------------------------------------------
# write file
def _writeHtmlFileForDescr(component_path, filename, content, settings, unit_filename):
    # create tags for description and solution
    problem_description_tag = etree.Element("div")
    problem_solutions_tag = etree.Element("div")

    #
    coderesponse_tag = etree.Element("coderesponse")
    problem_tag.append(coderesponse_tag)

    # grader queue
    queuename = __SETTINGS__.EDX_EXTERNAL_GRADER_QUEUENAME
    coderesponse_tag.set('queuename', queuename)

    # add labels to the coderesponse_tag
    label_tag = etree.Element("label")
    coderesponse_tag.append(label_tag)

    # add the instruction text
    # dont use p, it results in small text
    instruct_p_tag = etree.Element("div")
    instruct_p_tag.text = SUBMIT_INSTRUCTIONS
    label_tag.append(instruct_p_tag)

    # add <filesubmission> and <codeparam> to the coderesponse_tag
    coderesponse_tag.append(etree.Element("filesubmission"))
    codeparam_tag = etree.Element("codeparam")
    codeparam_tag.append(grader_payload_tag)
    coderesponse_tag.append(codeparam_tag)

    # add <solution> to the coderesponse_tag
    solution_tag = etree.Element("solution")
    coderesponse_tag.append(solution_tag)
    solution_tag.append(problem_solutions_tag)

    # set the display name for the description tag
    display_name = 'Mobius Modelling Assignment'
    if 'display_name' in settings:
        display_name = settings['display_name']
        # add an h3 heading to the description tag
        h3_tag = etree.Element("h3")
        h3_tag.text = display_name
        h3_tag.set('style', _css_settings.H3_CSS)
        problem_description_tag.append(h3_tag)
    problem_description_tag.set('display_name', display_name)

    # process the elements
    # these will be saved in the problem_description_tag and as solution <p> elements
    # the elements are spli using '==='
    # everything before the split is added to <label>
    # everything after the split is added to

    found_splitter = 0  # found ===
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

    # add prelude
    if 'example_filename' in settings and 'base_filename' in settings:
        _addPrelude(problem_description_tag)

    # if there is an example model, add a mobius iframe
    if 'example_filename' in settings:
        _addExampleModel(component_path, settings,
                         unit_filename, problem_description_tag)

    # if there is a base model, add a mobius iframe
    if 'base_filename' in settings:
        _addBaseModel(component_path, settings,
                      unit_filename, problem_description_tag)

    # convert problem_description_data to string
    problem_desc_data = etree.tostring(
        problem_description_tag, pretty_print=True)
    # print("=================")
    # print(problem_desc_data)
    # print("=================")
    # print(etree.dump(problem_description_tag))
    # print("=================")

    # write the Html file for the problem_description to COMP_HTML_FOLDER
    prob_xml_out_path = os.path.join(
        sys.argv[2], _edx_consts.COMP_HTML_FOLDER, filename + '.html')
    with open(prob_xml_out_path, 'wb') as fout:
        fout.write(problem_desc_data)

#--------------------------------------------------------------------------------------------------
# add prelude
def _addPrelude(problem_description_tag):

    # heading
    h4_tag = etree.Element("h4")
    h4_tag.set('style', _css_settings.H4_CSS)
    h4_tag.text = 'Completing the Assignment'
    problem_description_tag.append(h4_tag)

    # the example model description text
    prelude_p_tag = etree.Element("p")
    prelude_p_tag.text = SUBMIT_PRELUDE
    problem_description_tag.append(prelude_p_tag)
    prelude_ul_tag = etree.Element("ul")
    problem_description_tag.append(prelude_ul_tag)
    for bullet in SUBMIT_PRELUDE_BULLETS:
        prelude_li_tag = etree.Element("li")
        prelude_li_tag.text = bullet
        prelude_ul_tag.append(prelude_li_tag)

# add the example
def _addExampleModel(component_path, settings, unit_filename, problem_description_tag):

    # get the filename
    example_filename = settings['example_filename'].strip()

    # check that that the file exists
    component_dir = os.path.dirname(component_path)
    example_filepath = os.path.normpath(component_dir + '/' + example_filename)
    if (not os.path.exists(example_filepath) or not os.path.isfile(example_filepath)):
        print(WARNING, 'The example file does not exist: "' + example_filepath +'" in', component_path)

    # heading
    h4_tag = etree.Element("h4")
    h4_tag.set('style', _css_settings.H4_CSS)
    h4_tag.text = 'Example Model'
    problem_description_tag.append(h4_tag)
    
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


# add the base file
def _addBaseModel(component_path, settings, unit_filename, problem_description_tag):

    # get the filename
    base_filename = settings['base_filename'].strip()

    # check if there are any parameters
    params = ''
    if '?' in base_filename:
        [base_filename, params] = base_filename.split('?')

    # check that that the file exists
    component_dir = os.path.dirname(component_path)
    example_filepath = os.path.normpath(component_dir + '/' + base_filename)
    if (not os.path.exists(example_filepath) or not os.path.isfile(example_filepath)):
        print(WARNING, 'The example file does not exist: "' + example_filepath +'" in', component_path)

    # heading
    h4_tag = etree.Element("h4")
    h4_tag.set('style', _css_settings.H4_CSS)
    h4_tag.text = 'Base Codescript'
    problem_description_tag.append(h4_tag)
    
    # the base model description text
    base_descr_p_tag = etree.Element("p")
    base_descr_p_tag.text = SUBMIT_BASE_DESCRIPTION
    problem_description_tag.append(base_descr_p_tag)

    # the base model iframe
    mob_settings = {
        'mobius':'editor',
        'showView':'1',
        'node':'1'
    }

    # add the params to the mob_settings
    for param in params.split('&'):
        if '=' in param:
            [key, value] = param.split('=')
            mob_settings[key.strip()] = value.strip()

    iframe_tag = _mob_iframe.createMobIframe(base_filename, mob_settings, unit_filename)
    problem_description_tag.append(iframe_tag)
#--------------------------------------------------------------------------------------------------
