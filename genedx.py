import sys, os
import tarfile
import shutil
from lxml import etree
import markdown
from shutil import copyfile
# create the markdow instance
md = markdown.Markdown(extensions = ['extra', 'meta', 'sane_lists'])
#--------------------------------------------------------------------------------------------------
# Folders
# Hierarchical Terminology (very confusing)
# In  the edx interface, the names are as follows:
# -  course > section > subsection > unit     > component
# In the tar file folder structure, the names are as follows
# -  course > chapter > sequence   > vertical > component
# For the input data, we will use the first appraoch, since it follows the edx UI
# For the output, we must use the second approach
COURSE_FOLDER = "course" # Contains chapters (sections)
SECTION_FOLDER = "chapter" # Usually week 1, week 2
SUBSECTION_FOLDER = "sequential" # Usually intro, shorts, assignments
UNIT_FOLDER = "vertical" # Contains units, made of three type of components
# Components
COMP_HTML_FOLDER = "html"
COMP_VIDS_FOLDER = "video"
COMP_PROBS_FOLDER = "problem"
# Others
STATIC_FOLDER = "static"
#--------------------------------------------------------------------------------------------------
# Metadata settings for folders
# root
ROOT_FOLDER_REQ = ['org', 'course', 'url_name']
ROOT_FOLDER_OPT = ['visible_to_staff_only', 'start']
# course
COURSE_FOLDER_REQ = ['display_name']
COURSE_FOLDER_OPT = ['visible_to_staff_only', 'start', 
    'cert_html_view_enabled', 'course_image', 'graceperiod', 'instructor_info', 'invitation_only', 
    'language', 'learning_info', 'minimum_grade_credit', 'wiki_slug']
# section
SECTION_FOLDER_REQ = ['display_name']
SECTION_FOLDER_OPT = ['visible_to_staff_only', 'start']
# subsection
SUBSECTION_FOLDER_REQ = ['display_name']
SUBSECTION_FOLDER_OPT = ['visible_to_staff_only', 'start', 'format', 'graded', 'due', 'hide_after_due']
# unit
UNIT_FOLDER_REQ = ['display_name']
UNIT_FOLDER_OPT = ['visible_to_staff_only', 'start']
#--------------------------------------------------------------------------------------------------
# Metadata settings for components
COMP_HTML_REQ = ['type']
COMP_HTML_OPT = ['display_name', 'visible_to_staff_only', 'start']
COMP_VID_REQ = ['type', 'youtube_id_1_0']
COMP_VID_OPT = ['display_name', 'visible_to_staff_only', 'start', 'download_video', 'edx_video_id', 'html5_sources']
COMP_PROB_SUBMIT_REQ = ['type', 'question', 'queuename']
COMP_PROB_SUBMIT_OPT = ['display_name', 'visible_to_staff_only', 'start', 'max_attempts', 'weight', 
    'showanswer', 'attempts_before_showanswer_button']
COMP_PROB_CHECKBOXES_REQ = ['type']
COMP_PROB_CHECKBOXES_OPT = ['display_name', 'visible_to_staff_only', 'start', 'max_attempts', 'weight', 
    'showanswer', 'group_access', 'rerandomize', 'attempts_before_showanswer_button']
#--------------------------------------------------------------------------------------------------
# Metadata settings for components
METADATA_ENUMS = {
    'visible_to_staff_only': ['true', 'false'],
    # settings files
    'hide_after_due': ['true', 'false'],
    'graded': ['true', 'false'],
    'invitation_only': ['true', 'false'],
    'cert_html_view_enabled': ['true', 'false'],
    # component files
    'download_video': ['true', 'false'],
    'show_reset': ['true', 'false'],
    'showanswer': ["always", "answered", "attempted", "closed", "finished", "correct_or_past_due", "past_due", "never", "after_attempts"],
    'rerandomize': ["always", "onreset", "never", "per_student"],
    'type': ['html', 'video', 
        'problem-submit', 'problem-checkboxes', 'problem-choice', 'problem-dropdown', 'problem-numerical', 'problem-text']
}
#--------------------------------------------------------------------------------------------------
# Image Settings
IMAGE_WIDTH = 400
IMAGE_CSS = 'display:block;margin-left:auto;margin-right:auto;border-style:solid;border-width:1px;'
#--------------------------------------------------------------------------------------------------
# converts markdown to html
# returns the html string (in xml tags) and the metadata object
def convertMd(data):
    if data:
        content = '<root>' + md.convert(data) + '</root>'
        meta = md.Meta
        return [content, meta]
#--------------------------------------------------------------------------------------------------
# process images
def setImageHtml(img_elems):
    for img_elem in img_elems:
        img_elem.set('width', str(IMAGE_WIDTH))
        img_elem.set('style', IMAGE_CSS)
        src = img_elem.get('src')
        if not src.startswith('/'):
            img_elem.set('src', '/' + STATIC_FOLDER + '/' + src)
#--------------------------------------------------------------------------------------------------
# get the settings from a folder
# returns a dict of settings
def getMetaSettings(input, meta, req_names, opt_names=None):
    # process requires metadata
    req_values = {}
    for name in req_names:
        if (name in meta):
            req_values[name] = meta[name][0]
        else:
            print("Error: Failed to find the required metadata '" + name + "' in: ", input)
            req_values[name] = "default_" + name
    # process optional metadata
    opt_values = {}
    if opt_names:
        for name in opt_names:
            if (name in meta):
                opt_values[name] = meta[name][0]
                if name in METADATA_ENUMS:
                    if not opt_values[name] in METADATA_ENUMS[name]:
                        print("Warning: Unrecognised metadata value '" + name + "':'" + opt_values[name] + "' in: ", input)
    # check the names in meta
    for key in meta:
        if not key in req_names and not key in opt_names:
            print("Warning: Unrecognised metadata '" + key + "' in: ", input)
            print("Required metadata:", req_names)
            print("Optional metadata:", opt_names)
    # return the settings as two dicts or one dict
    req_values.update(opt_values)
    return req_values
#--------------------------------------------------------------------------------------------------
# get the settings from a folder
def getFolderMetaSettings(in_folder, req_names, opt_names=None):
    # we look for a file that has a name that ends with 'settings.md'
    in_path = None
    meta = {}
    try:
        for filename in os.listdir(in_folder):
            if filename.endswith("settings.md"):
                in_path = os.path.join(in_folder, filename)
                with open(in_path, 'r') as fin:
                    data = fin.read()
                    # process markdown, html and meta data (using extension)
                    [_, meta] = convertMd(data)
            if in_path and meta:
                break
        if not in_path or not meta:
            raise Exception()
    except:
        print("Error: Failed to read settings for the folder: ", in_folder)
    # return the metadata
    settings = getMetaSettings(in_path, meta, req_names, opt_names)
    return settings
#--------------------------------------------------------------------------------------------------
# get the settings from a component .md file
def getComponentContentMeta(in_path):
    content = ""
    meta = {}
    # read the settings file
    try:
        with open(in_path, 'r') as fin:
            data = fin.read()
            # process markdown, html and meta data (using extension)
            [content, meta] = convertMd(data)
            # check we have meta
            if not meta:
                print("Error: Failed to read metadata in: ", in_path)
                meta = {}
    except:
        print("Error: Failed to read file: ", in_path)
    # return the meta
    return [content, meta]
#--------------------------------------------------------------------------------------------------
# generate xml for a course
def writeXmlForRoot(in_folder, out_folder):
    # create a file in the root folder
    # ----  ----  ----
    # <course url_name="1234" org="abc" course="online101"/>
    # ----  ----  ----
    print("writing root xml")
    # get settings
    root_folder_settings = getFolderMetaSettings(in_folder, ROOT_FOLDER_REQ, ROOT_FOLDER_OPT)
    # create xml
    course_tag = etree.Element("course")
    for key in root_folder_settings:
        course_tag.set(key, root_folder_settings[key])
    result = etree.tostring(course_tag, pretty_print=True)
    # write the file
    root_xml_out_path = os.path.join(out_folder, 'course.xml')
    with open(root_xml_out_path, 'wb') as fout:
        fout.write(result)
    # return the url_name, this is needed for the next level, the filename for course
    return root_folder_settings['url_name']
#--------------------------------------------------------------------------------------------------
# generate xml for a course
def writeXmlForCourse(in_folder, out_folder, filename, sections):
    # create a file in the 'course' folder
    # ----  ----  ----
    # <course cert_html_view_enabled="true" display_name="My Course: Part1" language="en" 
    # start="&quot;2030-01-01T00:00:00+00:00&quot;">
    #     <chapter url_name="1de112fb4d5c4da694c56dbfa0fd8086"/>
    #     <chapter url_name="1de112fb4d5c4da694c56dbfa0fd8086"/>
    #     <chapter url_name="1de112fb4d5c4da694c56dbfa0fd8086"/>
    #     <wiki slug="NUS.SCT01.20192020S1"/>
    # </course>
    # ----  ----  ----
    print("writing course xml")
    # get settings
    course_folder_settings = getFolderMetaSettings(in_folder, COURSE_FOLDER_REQ, COURSE_FOLDER_OPT)
    # create xml
    course_tag = etree.Element("course")
    for key in course_folder_settings:
        if not key in ['wiki_slug']:
            course_tag.set(key, course_folder_settings[key])
    for section in sections:
        chapter_tag = etree.Element("chapter")
        chapter_tag.set('url_name', section)
        course_tag.append(chapter_tag)
    if 'wiki_slug' in course_folder_settings:
        wiki_tag = etree.Element("wiki")
        wiki_tag.set('slug', course_folder_settings['wiki_slug'])
        course_tag.append(wiki_tag)
    result = etree.tostring(course_tag, pretty_print = True)
    # write the file
    xml_out_path = os.path.join(out_folder, COURSE_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
#--------------------------------------------------------------------------------------------------
# generate xml for a section, also called a chapter
# a section contains subsections
# examples, week 1, week 2
def writeXmlForSection(in_folder, out_folder, filename, subsections):
    # ----  ----  ----
    # <chapter display_name="Section">
    #     <sequential url_name="c717ae712f294fe397b72be2011b4ec0"/>
    #     <sequential url_name="c717ae712f294fe397b72be2011b4ec0"/>
    #     <sequential url_name="c717ae712f294fe397b72be2011b4ec0"/>
    # </chapter>
    # ----  ----  ----
    print("- writing section xml")
    # get settings
    section_folder_settings = getFolderMetaSettings(in_folder, SECTION_FOLDER_REQ, SECTION_FOLDER_OPT)
    # create xml
    chapter_tag = etree.Element("chapter")
    for key in section_folder_settings:
        chapter_tag.set(key, section_folder_settings[key])
    for subsection in subsections:
        sequential_tag = etree.Element("sequential")
        sequential_tag.set('url_name',subsection)
        chapter_tag.append(sequential_tag)
    result = etree.tostring(chapter_tag, pretty_print = True)
    # write the file
    xml_out_path = os.path.join(out_folder, SECTION_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
#--------------------------------------------------------------------------------------------------
# generate xml for a subsection, also called a sequence
# a subsection can contain units
# example, intorduction, shorts, assignments
def writeXmlForSubsection(in_folder, out_folder, filename, units):
    # ----  ----  ----
    # <sequential display_name="Section Title">
    #   <vertical url_name="fbb654358e4a4c0f8cc5bce4627ec82b"/>
    #   <vertical url_name="fbb654358e4a4c0f8cc5bce4627ec82b"/>
    # </sequential>
    # ----  ----  ----
    # <sequential display_name="Assignment" 
    #       due="&quot;2019-09-08T10:00:00+00:00&quot;" 
    #       format="Assignment" 
    #       graded="true">
    #   <vertical url_name="af6f0c61851d4aaea80866550cfc4c90"/>
    #   <vertical url_name="815e71a4f2434de1ab58c5e177c1aee9"/>
    # </sequential>
    # ----  ----  ----
    print("-- writing subsection xml")
    # get settings
    subsection_folder_settings = getFolderMetaSettings(in_folder, SUBSECTION_FOLDER_REQ, SUBSECTION_FOLDER_OPT)
    if 'graded' in subsection_folder_settings:
        if subsection_folder_settings['graded'] == 'true':
            subsection_folder_settings['format'] = 'Assignment'
    # create the root tag
    sequential_tag = etree.Element("sequential")
    for key in subsection_folder_settings:
        sequential_tag.set(key, subsection_folder_settings[key])
    # add the units
    for unit in units:
        vertical_tag = etree.Element("vertical")
        vertical_tag.set('url_name', unit)
        sequential_tag.append(vertical_tag)
    result = etree.tostring(sequential_tag, pretty_print=True)
    # write the file
    xml_out_path = os.path.join(out_folder, SUBSECTION_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
#--------------------------------------------------------------------------------------------------
# generate xml for a unit, also called a vertical
# a unit can contain many componets
def writeXmlForUnit(in_folder, out_folder, filename, components):
    # ----  ----  ----
    # <vertical display_name="Unit Title">
    #     <html url_name="7d3ba88c180745e5baf29084667409b2"/>
    #     <video url_name="05c171c507ab4d76830823f60075b0ae"/>
    #     <problem url_name="e2b890df14c1441ca66528ab58ca07b9"/>
    # </vertical>
    # ----  ----  ----
    print("--- writing unit xml")
    # get settings
    unit_folder_settings = getFolderMetaSettings(in_folder, UNIT_FOLDER_REQ, UNIT_FOLDER_OPT)
    # create xml
    vertical_tag = etree.Element("vertical")
    for key in unit_folder_settings:
        vertical_tag.set(key, unit_folder_settings[key])
    for component in components:
        component_filename = component[0]
        component_type = component[1] # 'html' or 'video' or 'quiz'
        component_tag = etree.Element(component_type)
        component_tag.set('url_name', component_filename)
        vertical_tag.append(component_tag)
    result = etree.tostring(vertical_tag, pretty_print = True)
    # write file
    xml_out_path = os.path.join(out_folder, UNIT_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
#--------------------------------------------------------------------------------------------------
# read md
# write to either units folder or problems folder, depending on the type
def processMd(component_path, out_folder, filename):
    # print("component_path", component_path)
    # generate the files in the right folders
    [content, meta] = getComponentContentMeta(component_path)
    # get component type
    comp_type = meta['type']
    if comp_type:
        comp_type = comp_type[0]
    else:
        print('Error: Component type missing:', component_path)
        return 
    # generate xml files
    if comp_type == 'html':
        settings = getMetaSettings(component_path, meta, COMP_HTML_REQ, COMP_HTML_OPT )
        writeXmlForHtmlComp(out_folder, filename, content, settings)
    elif comp_type == 'problem-checkboxes':
        settings = getMetaSettings(component_path, meta, COMP_PROB_CHECKBOXES_REQ, COMP_PROB_CHECKBOXES_OPT )
        writeXmlForProbCheckboxesComp(out_folder, filename, content, settings)
    elif comp_type == 'problem-submit':
        settings = getMetaSettings(component_path, meta, COMP_PROB_SUBMIT_REQ , COMP_PROB_SUBMIT_OPT )
        writeXmlForSubmitComp(out_folder, filename, content, settings)
    elif comp_type == 'video':
        settings = getMetaSettings(component_path, meta, COMP_VID_REQ, COMP_VID_OPT )
        writeXmlForVidComp(out_folder, filename, content, settings)
    else:
        print('Error: Component type not recognised:', comp_type, "in", component_path)
    # return the component type, which is needed for generating the xml for the subsection
    if comp_type.startswith('problem'):
        comp_type = 'problem'
    return comp_type
#--------------------------------------------------------------------------------------------------
# write xml for Html component
def writeXmlForHtmlComp(out_folder, filename, content, settings):
    # ---- Html file ----
    # <p>
    #   <span style="text-decoration: underline;">Objective:</span>
    # </p>
    # <p>
    #   This week's assignment is broken down into <strong>three file submissions</strong>. 
    #   These smaller submissions are meant to help you along the way.
    # </p>
    # <p>
    #   <img height="288" width="498" src="/static/assignment.png" alt="" 
    #   style="display: block; margin-left: auto; margin-right: auto;" />
    # </p>
    # ----  ----  ----
    # ---- XML file ----
    # <html 
    #   filename="1c870c63861749dbb45ea16ace9fbe24" 
    #   display_name="Task" 
    #   editor="visual"
    # />
    # ----  ----  ----
    # read content
    content_root_tag = etree.fromstring(content)
    # process images
    img_elems = list(content_root_tag.iter('img'))
    setImageHtml(img_elems)
    # write the html file
    html_out_path = os.path.join(out_folder, COMP_HTML_FOLDER, filename + '.html')
    with open(html_out_path, 'wb') as fout:
        for tag in content_root_tag:
            tag_result = etree.tostring(tag, pretty_print = True)
            fout.write(tag_result)
    # create xml
    html_tag = etree.Element("html")
    for key in settings:
        if key not in ['type']:
            html_tag.set(key, settings[key])
    html_tag.set('filename', filename)
    result = etree.tostring(html_tag, pretty_print = True)
    # write the xml file
    xml_out_path = os.path.join(out_folder, COMP_HTML_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
#--------------------------------------------------------------------------------------------------
# write xml for problem Checkboxescomponent
def writeXmlForProbCheckboxesComp(out_folder, filename, content, settings):
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
    # process the html
    content_root_tag = etree.fromstring(content)
    # process images
    img_elems = list(content_root_tag.iter('img'))
    setImageHtml(img_elems)
    # process the p elements
    # these will be converted to <label>, <description>, and solution <p> elements
    label_tag = etree.Element("label") 
    description_tag = etree.Element("description") 
    solution_p_tags = []
    p_elems = list(content_root_tag.iter('p'))
    if p_elems:
        label_tag.text = p_elems[0].text
        if len(p_elems) > 1:
            description_tag.text = p_elems[1].text
        for p_elem in p_elems[2:]:
            solution_p_tag = etree.Element("p")
            solution_p_tag.text = p_elem.text
            solution_p_tags.append(solution_p_tag)
    else:
        print('Choice problem is missing paragraphs.', filename)
    # process the ul and li elements
    # these will be converted to <choice> elements
    choices_tags = []
    ul_elems = list(content_root_tag.iter('ul'))
    li_elems = []
    if ul_elems:
        li_elems = list(ul_elems[0].iter('li'))
    if li_elems:
        for li_elem in li_elems:
            choice_tag = etree.Element("choice")
            choices_tags.append(choice_tag)
            choice_tag.text = li_elem.text
            if 'correct' in li_elem.keys():
                correct_val = li_elem.get('correct')
                if correct_val not in ['true', 'false']:
                    print('Choice problem choice has a "correct" attribute with an invalid value of "' + correct_val + '".', filename)
                choice_tag.set('correct', correct_val)
            else:
                print('Choice problem choice is missing the "correct" attribute.', filename)
    else:
        print('Choice problem seems to have no choices.', filename)
    # add the choices and solutions to the choiceresponse_tag
    choiceresponse_tag.append(label_tag)
    choiceresponse_tag.append(description_tag)
    if choices_tags:
        checkboxgroup_tag = etree.Element("checkboxgroup")
        choiceresponse_tag.append(checkboxgroup_tag)
        for choice_tag in choices_tags:
            checkboxgroup_tag.append(choice_tag)
    if solution_p_tags:
        solution_tag = etree.Element("solution")
        div_tag = etree.Element("div")
        div_tag.set('class', 'detailed-solution')
        choiceresponse_tag.append(solution_tag)
        solution_tag.append(div_tag)
        for solution_p_tag in solution_p_tags:
            div_tag.append(solution_p_tag)
    # convert problem_tag to string
    result = etree.tostring(problem_tag, pretty_print=True)
    # write the file
    xml_out_path = os.path.join(out_folder, COMP_PROBS_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
#--------------------------------------------------------------------------------------------------
# write xml for problem submit
def writeXmlForSubmitComp(out_folder, filename, content, settings):
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
        if key not in ['type', 'display_name', 'question', 'queuename']:
            problem_tag.set(key, settings[key])
    queuename = 'Dummy_Queuename'
    if 'queuename' in settings:
        queuename = settings.get('queuename')
    else:
        print('Submit problem is missing metadata: queuename.', filename)
    coderesponse_tag.set('queuename', queuename)
    question = 'Dummy_Question'
    if 'question' in settings:
        question = settings.get('question')
    else:
        print('Submit problem is missing metadata: question.', filename)
    grader_payload_tag = etree.Element("grader_payload")
    grader_payload_tag.text = '{"question": "' + question + '"}'
    # read content
    content_root_tag = etree.fromstring(content)
    # process images
    img_elems = list(content_root_tag.iter('img'))
    setImageHtml(img_elems)
    # process the p elements
    # these will be converted to <label>, <description>, and solution <p> elements
    label_tag = etree.Element("label") 
    solution_p_tags = []
    p_elems = list(content_root_tag.iter('p'))
    if p_elems:
        label_tag.text = p_elems[0].text
        for p_elem in p_elems[1:]:
            solution_p_tag = etree.Element("p")
            solution_p_tag.text = p_elem.text
            solution_p_tags.append(solution_p_tag)
    else:
        print('Submit problem is missing paragraphs.', filename)
    # add elems to the coderesponse_tag
    coderesponse_tag.append(label_tag)
    coderesponse_tag.append(etree.Element("filesubmission") )
    codeparam_tag = etree.Element("codeparam")
    codeparam_tag.append(grader_payload_tag)
    coderesponse_tag.append(codeparam_tag)
    if solution_p_tags:
        solution_tag = etree.Element("solution")
        coderesponse_tag.append(solution_tag)
        for solution_p_tag in solution_p_tags:
            solution_tag.append(solution_p_tag)
    # convert problem_tag to string
    result = etree.tostring(problem_tag, pretty_print=True)
    # write the file
    xml_out_path = os.path.join(out_folder, COMP_PROBS_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
#--------------------------------------------------------------------------------------------------
# write xml for video component
def writeXmlForVidComp(out_folder, filename, content, settings):
    # ----  ----  ----
    # <video 
    #   url_name="5bf2b878f31d4d20a2cc657e5b4b0e2e" 
    #   youtube_id_1_0="3_yD_cEKoCk"
    #   display_name="Summary: Week 2" 
    #   download_video="false" 
    #   edx_video_id="" 
    #   html5_sources="[]" 
    # />
    # ----  ----  ----
    # create xml
    video_tag = etree.Element("video")
    for key in settings:
        video_tag.set(key, settings[key])
    result = etree.tostring(video_tag, pretty_print = True)
    # write the file
    xml_out_path = os.path.join(out_folder, COMP_VIDS_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
#--------------------------------------------------------------------------------------------------
# this is just in case there are some html files
# write to units to the correct folder
# returns void
def processHtml(component_path, out_folder, filename):
    with open(component_path, 'r') as f_read:
        contents = f_read.read()
        xml_path = ''
        if (contents.startswith('<html')):
            xml_path = os.path.join(out_folder, COMP_HTML_FOLDER, filename + '.xml')
        elif (contents.startswith('<problem')):
            xml_path = os.path.join(out_folder, COMP_PROBS_FOLDER, filename + '.xml')
        elif (contents.startswith('<video')):
            xml_path = os.path.join(out_folder, COMP_VIDS_FOLDER, filename + '.xml')
        # write the content
        with open(xml_path, 'w') as f:
            f.write(contents)
#--------------------------------------------------------------------------------------------------
# write the image to the assets folder
# returns void
def processImage(component_path, out_folder, component):
    # copy the image to the assets folder
    out_path = os.path.join(out_folder, STATIC_FOLDER, component)
    copyfile(component_path, out_path)
#--------------------------------------------------------------------------------------------------
# get all the sub folders in a folder
# return the folder names and folder paths, like this 
# [[folder_name, folder_path], [folder_name, folder_path], [folder_name, folder_path]...]
def getSubFolders(folder_path):
    folders = []
    files_and_folders = os.listdir(folder_path)
    for file_or_folder in files_and_folders:
        path = os.path.join(folder_path, file_or_folder)
        if (not os.path.isfile(path)):
            folders.append([file_or_folder, path])
    folders.sort()
    return folders
#--------------------------------------------------------------------------------------------------
# get all the files in a folder
# return a list of file names and file paths, as a pair
# [[file_name, file_path], [file_name, file_path], [file_name, file_path] ...]
def getFiles(folder_path):
    files = []
    files_and_folders = os.listdir(folder_path)
    for file_or_folder in files_and_folders:
        path = os.path.join(folder_path, file_or_folder)
        if (os.path.isfile(path)):
            files.append([file_or_folder, path])
    files.sort()
    return files
#--------------------------------------------------------------------------------------------------
# get the folder display name
# returns a string
def getFolderDisplayName(folder_path):
    name = os.path.split(folder_path)[1]
    return name.replace('_', ' ').strip()
#--------------------------------------------------------------------------------------------------
# get meta data
# returns a string
def getCompMetaType(meta):
    if 'type' in meta:
        value = meta['type'][0]
        if value in ['html', 'video', 'problem']:
            return value
        else:
            print('The component type is not recognised. It should be "html", "video", or "problem".')
    return 'html'
#--------------------------------------------------------------------------------------------------
# get meta data
# returns a sting 
def getCompMetaSubtype(meta):
    if 'subtype' in meta:
        value = meta['subtype'][0]
        if value in ['Checkboxes', 'Multiple', 'Dropdown', 'Numerical', 'Text']:
            return value
        else:
            print('The component subtype is not recognised.')
    return 'Checkboxes'
#--------------------------------------------------------------------------------------------------
# get the display_name of a component
# returns a string
def getComponentDisplayName(component_path):
    name = None
    # if this is an md file, get the first heading in the file
    if (component_path.endswith('.md')):
        if (os.path.isfile(component_path)):
            with open(component_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if (line.startswith('#')):
                        name = line.split('#')[1]
    # if the name is still None, then use the file name
    if not name:
        name = os.path.split(component_path)[1]
    # clean up the name
    if ('.' in name):
        name = name.split('.')[0]
    if ('__' in name):
        name = name.split('__')[1]
    name = name.replace('_', ' ').strip()
    # return the final name
    return name
#--------------------------------------------------------------------------------------------------
# process one course
def processCourse(in_folder, out_folder):
    # get the main mooc input folder, which we assume is the first folder
    courses = getSubFolders(in_folder)
    if (len(courses) != 1):
        print('There should only be one folder in the root folder.')
        return
    course_path = courses[0][1]
    # make the folders inside dist
    os.mkdir(os.path.join(out_folder, COURSE_FOLDER))
    os.mkdir(os.path.join(out_folder, SECTION_FOLDER))
    os.mkdir(os.path.join(out_folder, SUBSECTION_FOLDER))
    os.mkdir(os.path.join(out_folder, UNIT_FOLDER))
    os.mkdir(os.path.join(out_folder, COMP_HTML_FOLDER))
    os.mkdir(os.path.join(out_folder, COMP_VIDS_FOLDER))
    os.mkdir(os.path.join(out_folder, COMP_PROBS_FOLDER))
    os.mkdir(os.path.join(out_folder, STATIC_FOLDER))
    # create the root xml file
    course_filename = writeXmlForRoot(in_folder, out_folder)
    # loop
    sections = []
    for [section, section_path] in getSubFolders(course_path):
        print("- section", section)
        section_filename = section.lower()
        sections.append(section_filename)
        subsections = []
        for [subsection, subsection_path] in getSubFolders(section_path):
            print("-- subsection", subsection)
            subsection_filename = section_filename + '_' + subsection.lower()
            subsections.append(subsection_filename)
            units = []
            for [unit, unit_path] in getSubFolders(subsection_path):
                print("--- unit", unit)
                unit_filename = subsection_filename + '_' + unit.lower()
                units.append(unit_filename)
                components = []
                for [component, component_path] in getFiles(unit_path):
                    [component_name, component_ext] = component.lower().split('.')
                    component_filename = unit_filename + '_' + component_name
                    # write the files
                    if component_ext == 'md':
                        if not component_path.endswith('settings.md'):
                            # this is md, not a settings file
                            # this can be html, problem, or video
                            component_type = processMd(component_path, out_folder, component_filename)
                            components.append([component_filename, component_type])
                    elif component_ext in ['htm','html']:
                        # this is an html snippet, only used in special cases
                        processHtml(component_path, out_folder, component_filename)
                        components.append([component_filename, 'html'])
                    elif component_ext in ['jpg', 'jpeg', 'png', 'gif']:
                        # this is an image that needs to go to assets
                        processImage(component_path, out_folder, component)
                    else:
                        pass
                        # could be any other file, just ignore and continue
                        # print("Warning: File extension not recognised. Expecting either .md or .xml:", component_path)
                writeXmlForUnit(unit_path, out_folder, unit_filename, components)
            writeXmlForSubsection(subsection_path, out_folder, subsection_filename, units)
        writeXmlForSection(section_path, out_folder, section_filename, subsections)
    writeXmlForCourse(course_path, out_folder, course_filename, sections)
#--------------------------------------------------------------------------------------------------
def main():
    print("Start compiling")

    # get the args
    if (len(sys.argv) != 3):
        print("Incorrect number of arguments")
        print("Usage: python genedx.py in_folder out_folder.")
        print("Example: python genedx.py ./my_input ./my_output.")
        print("Warning: everything in the out folder will be deleted.")
        return

    # get the paths
    in_folder = sys.argv[1]
    out_folder = sys.argv[2]

    # check the input and output folders
    print("in", in_folder)
    if (not os.path.isdir(in_folder)):
        print("The input path is not a valid path")
        return
    print("out", out_folder)
    try:
        if (os.path.isdir(out_folder)):
            print("Deleting contents in " + out_folder)
            shutil.rmtree(out_folder)
        os.mkdir(out_folder)
    except:
        print("Failed to create the output folder: " + out_folder)
    
    # create content
    processCourse(in_folder, out_folder)

    # create the tar file
    [out_folder_path, out_folder_name] = os.path.split(out_folder)
    tar = tarfile.open(out_folder_name + ".tar.gz", "w:gz")
    os.chdir(out_folder_path)
    tar.add(out_folder_name, recursive=True)
    tar.close()

    print("Finish compiling")
#--------------------------------------------------------------------------------------------------
main()
