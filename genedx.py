import sys, os
import tarfile
import shutil
import urllib
from lxml import etree
import markdown
# create the markdow instance
md = markdown.Markdown(extensions = ['extra', 'meta', 'sane_lists'])
#--------------------------------------------------------------------------------------------------
IN_FOLDER = './test/input'
OUT_FOLDER = './test/output'
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
# Repo settings
# Example Repo, Github, where examples can be uploaded
# These examples can be viewed by anyone
# Answer to graded questions should not be uploaded here
EXAMPLE_REPO = {'url': 'https://github-examples.com', 'id': '123', 'key': 'xxx'}
# Answer Repo, AWS, where answers to graded questions can be uploaded
ANSWER_REPO = {'url': 'https://aws-answers.com', 'id': '123', 'key': 'xxx'}
#--------------------------------------------------------------------------------------------------
# File extensions used for different types of assets
# Images, PDFs, Video captions, these will be copied to the STATIC_FOLDER
ASSET_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'srt']
# Upload extensions
UPLOAD_EXTENSIONS = ['mob']
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
COMP_VIDEO_REQ = ['type', 'youtube_id_1_0']
COMP_VIDEO_OPT = ['transcript', 'display_name', 'edx_video_id', 'visible_to_staff_only', 'start', 'download_video', 
    'show_captions', 'sub', 'html5_sources']
COMP_PROB_SUBMIT_REQ = ['type', 'question', 'queuename']
COMP_PROB_SUBMIT_OPT = ['answer', 'display_name', 'visible_to_staff_only', 'start', 'max_attempts', 'weight', 
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
    'show_captions': ['true', 'false'],
    'showanswer': ["always", "answered", "attempted", "closed", "finished", "correct_or_past_due", 
        "past_due", "never", "after_attempts"],
    'rerandomize': ["always", "onreset", "never", "per_student"],
    'type': ['html', 'video', 'problem-submit', 'problem-checkboxes']
    # more types: ['problem-choice', 'problem-dropdown', 'problem-numerical', 'problem-text']
}
#--------------------------------------------------------------------------------------------------
# Problem Instructions
INSTRUCTIONS_CHECKBOXES = 'Please select all applicable options from the list below. Multiple selections are allowed. '
#--------------------------------------------------------------------------------------------------
# Image Settings
FIGURE_CSS = 'margin:20px;'
IMAGE_CSS = 'width:400px;display:block;margin-left:auto;margin-right:auto;border-style:solid;border-width:1px;'
FIGCAPTION_CSS = 'width:400px;display:block;margin-left:auto;margin-right:auto;margin-top:8px;text-align:center;font-style: italic;'
#--------------------------------------------------------------------------------------------------
# Iframe settings
# Any <a> tags with files with these extension will be replaced with iframes
IFRAME_URLS = {'mob': 'https://mobius.design-automation.net/publish?file='}
IFRAME_WIDTH = '100%' 
IFRAME_HEIGHT ='600px' 
IFRAME_STYLE = 'border: 1px solid black;'
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
def setImageHtml(img_elems, unit_filename):
    for img_elem in img_elems:
        # create new image
        img_tag = etree.Element("img")
        for key in img_elem:
            if key not in ['src']:
                img_tag.set(key, img_elem.get(key))
        if IMAGE_CSS:
            img_tag.set('style', IMAGE_CSS)
        src = img_elem.get('src')
        # get the new src for the image
        new_src = ''
        if src.startswith('/') or src.startswith('http'):
            new_src = src
        else:
            new_src = '/' + STATIC_FOLDER + '/' + unit_filename + '_' + src
        img_tag.set('src', new_src)
        # create an a href tag
        a_tag = etree.Element("a")
        a_tag.set('target', 'image')
        a_tag.set('href', new_src)
        a_tag.append(img_tag)
        # create figure
        figure_tag = etree.Element("figure")
        if FIGURE_CSS:
            figure_tag.set('style', FIGURE_CSS)
        figure_tag.append(a_tag)
        #  create caption for the figure
        if 'alt' in img_elem.keys():
            figcaption_tag = etree.Element("figcaption")
            if FIGCAPTION_CSS:
                figcaption_tag.set('style', FIGCAPTION_CSS)
            figcaption_tag.text = img_elem.get('alt')
            figure_tag.append(figcaption_tag)
        # replace the existing image with the figure
        img_elem.getparent().replace(img_elem, figure_tag)
#--------------------------------------------------------------------------------------------------
# process a hrefs
def setHrefHtml(component_path, a_elems, unit_filename):
    for a_elem in a_elems:
        # get the href
        href = a_elem.get('href')
        if not href:
            print('An <a/> tag has no "href" attribute:', a_elem)
            return
        # break down the url
        href_parts = list(urllib.parse.urlparse(href))
        href_file = None
        href_file_ext = None
        href_path = href_parts[2]
        if href_path and '.' in href_path:
            href_file = href_path.split('/')[-1]
            href_file_ext = href_path.split('.')[-1]
        new_tag = None
        # create the new href
        # either the file needs to be uploaded to a repo
        # or the file has already been copied to the STATIC_FOLDER
        new_href = None
        if href_file_ext == None or href_file_ext == '':
            new_href = href
        elif href_file_ext in UPLOAD_EXTENSIONS:
            component_folder = os.path.dirname(component_path)
            new_href = processUploadsToRepo(component_folder, href_file, EXAMPLE_REPO, unit_filename + '_' + href)
        elif href_file_ext in ASSET_EXTENSIONS:
            new_href = '/' + STATIC_FOLDER + '/' + unit_filename + '_' + href_file
        else:
            new_href = href
            print('Found an unrecognised href:', href, href_file_ext)
        # create the new tag, either an <iframe/> or a <a/>
        if href_file_ext in IFRAME_URLS.keys():
            # create new image
            new_tag = etree.Element('iframe')
            new_tag.set('width', IFRAME_WIDTH)
            new_tag.set('height', IFRAME_HEIGHT)
            new_tag.set('style', IFRAME_STYLE)
            new_src = IFRAME_URLS[href_file_ext] + new_href
            new_tag.set('src', new_src)
        else:
            new_tag = etree.Element('a')
            for key in a_elem:
                if key not in ['href']:
                    new_tag.set(key, a_elem.get(key))
            new_tag.set('src', new_href)
        # replace the existing a with the new tag
        a_elem.getparent().replace(a_elem, new_tag)
#--------------------------------------------------------------------------------------------------
# get the settings from a component or a folder
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
def processMd(component_path, out_folder, component_filename, unit_filename):
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
        writeXmlForHtmlComp(component_path, out_folder, component_filename, content, settings, unit_filename)
    elif comp_type == 'problem-checkboxes':
        settings = getMetaSettings(component_path, meta, COMP_PROB_CHECKBOXES_REQ, COMP_PROB_CHECKBOXES_OPT )
        writeXmlForProbCheckboxesComp(component_path, out_folder, component_filename, content, settings, unit_filename)
    elif comp_type == 'problem-submit':
        settings = getMetaSettings(component_path, meta, COMP_PROB_SUBMIT_REQ , COMP_PROB_SUBMIT_OPT )
        writeXmlForSubmitComp(component_path, out_folder, component_filename, content, settings, unit_filename)
        uploadAnswers(component_path, settings, unit_filename)
    elif comp_type == 'video':
        settings = getMetaSettings(component_path, meta, COMP_VIDEO_REQ, COMP_VIDEO_OPT )
        writeXmlForVidComp(out_folder, component_filename, content, settings, unit_filename)
    else:
        print('Error: Component type not recognised:', comp_type, "in", component_path)
    # return the component type, which is needed for generating the xml for the subsection
    if comp_type.startswith('problem'):
        comp_type = 'problem'
    return comp_type
#--------------------------------------------------------------------------------------------------
# write xml for Html component
def writeXmlForHtmlComp(component_path, out_folder, filename, content, settings, unit_filename):
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
    # process hrefs
    a_elems = list(content_root_tag.iter('a'))
    setHrefHtml(component_path, a_elems, unit_filename)
    # process images
    img_elems = list(content_root_tag.iter('img'))
    setImageHtml(img_elems, unit_filename)
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
def writeXmlForProbCheckboxesComp(component_path, out_folder, filename, content, settings, unit_filename):
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
    # process hrefs
    a_elems = list(content_root_tag.iter('a'))
    setHrefHtml(component_path, a_elems, unit_filename)
    # process images
    img_elems = list(content_root_tag.iter('img'))
    setImageHtml(img_elems, unit_filename)
    # process the p elements
    # these will be converted to <label>, and solution <p> elements
    labels = []
    solutions = []
    choices = []
    for elem in content_root_tag.getchildren():
        # first deal with the bullets, <ul/>
        # this could be normal bullets or could be the choices
        if elem.tag == 'ul' and not choices:
            this_is_choices_tag = False
            for li_elem in elem.getchildren():
                if li_elem.text[:3] in ['[ ]', '[x]']:
                    this_is_choices_tag = True # we found a choice
                    correct_val = 'true'
                    if li_elem.text[:3] == '[ ]':
                        correct_val = 'false'
                    choice_tag = etree.Element("choice")
                    choice_tag.text = li_elem.text[3:]
                    choice_tag.set('correct', correct_val)
                    choices.append(choice_tag)
                else:
                    pass # this is ok, could be normal bullets
            if not this_is_choices_tag:
                if choices:
                    solutions.append(elem)
                else:
                    labels.append(elem)
        # process other stuff, like <p/>
        # if choices is not empty, this must be part of solution text
        # if choices is empty, this must be part of label text
        else:
            if choices:
                solutions.append(elem)
            else:
                labels.append(elem)
    # add the choices and solutions to the choiceresponse_tag
    if labels:
        label_tag = etree.Element("label") 
        choiceresponse_tag.append(label_tag)
        for label in labels:
            label_tag.append(label)
    else:
        print('Choice problem seems to have no text that describes the question.', filename)
    if INSTRUCTIONS_CHECKBOXES:
        description_tag = etree.Element("description")
        choiceresponse_tag.append(description_tag)
        description_tag.text = INSTRUCTIONS_CHECKBOXES
    if choices:
        checkboxgroup_tag = etree.Element("checkboxgroup")
        choiceresponse_tag.append(checkboxgroup_tag)
        for choice in choices:
            checkboxgroup_tag.append(choice)
    else:
        print('Choice problem seems to have no choices.', filename)
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
    xml_out_path = os.path.join(out_folder, COMP_PROBS_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
#--------------------------------------------------------------------------------------------------
# write xml for problem submit
def writeXmlForSubmitComp(component_path, out_folder, filename, content, settings, unit_filename):
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
        if key not in ['type', 'question', 'queuename', 'answer']:
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
    # process hrefs
    a_elems = list(content_root_tag.iter('a'))
    setHrefHtml(component_path, a_elems, unit_filename)
    # process images
    img_elems = list(content_root_tag.iter('img'))
    setImageHtml(img_elems, unit_filename)
    # process the p elements
    # these will be converted to <label>, and solution <p> elements
    label_tag = etree.Element("label") 
    solutions = []
    elems = content_root_tag.getchildren()
    if elems:
        label_tag.text = elems[0].text
        for elem in elems[1:]:
            solutions.append(elem)
    else:
        print('Submit problem is missing paragraphs.', filename)
    # add elems to the coderesponse_tag
    coderesponse_tag.append(label_tag)
    coderesponse_tag.append(etree.Element("filesubmission") )
    codeparam_tag = etree.Element("codeparam")
    codeparam_tag.append(grader_payload_tag)
    coderesponse_tag.append(codeparam_tag)
    if solutions:
        solution_tag = etree.Element("solution")
        coderesponse_tag.append(solution_tag)
        for solution in solutions:
            solution_tag.append(solution)
    # convert problem_tag to string
    result = etree.tostring(problem_tag, pretty_print=True)
    # write the file
    xml_out_path = os.path.join(out_folder, COMP_PROBS_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
#--------------------------------------------------------------------------------------------------
# write xml for video component
def writeXmlForVidComp(out_folder, filename, content, settings, unit_filename):
    # ----  ----  ----
    # <video 
    #   url_name="section_week_1_subsection_2_shorts_unit_1_text_and_videos_02_video" 
    #   sub="" 
    #   transcripts="{&quot;en&quot;: &quot;7d76f250-0000-42ea-8aba-c0c0ce845280-en.srt&quot;}" 
    #   display_name="A Video" edx_video_id="7d76f250-0000-42ea-8aba-c0c0ce845280" 
    #   youtube_id_1_0="3_yD_cEKoCk" >
    #   <video_asset client_video_id="External Video" duration="0.0" image="">
    #     <transcripts>
    #       <transcript file_format="srt" language_code="en" provider="Custom"/>
    #     </transcripts>
    #   </video_asset>
    #   <transcript language="en" src="7d76f250-0000-42ea-8aba-c0c0ce845280-en.srt"/>
    # </video>
    # ----  ----  ----
    # create xml
    video_tag = etree.Element("video")
    video_tag.set('url_name', filename)
    for key in settings:
        if key not in ['type', 'transcript']:
            video_tag.set(key, settings[key])
    # add youtube
    if 'youtube_id_1_0' in settings:
        video_tag.set('youtube', '1.00:' + settings['youtube_id_1_0'])
    # add transcript data
    if 'transcript' in settings:
        # set the transcript attribute
        transcripts_str = unit_filename + '_' + settings['transcript']
        transcripts_obj = '{"en": "' + transcripts_str + '"}'
        video_tag.set('transcripts', transcripts_obj)
        # add the video asset tag
        video_asset_tag = etree.Element("video_asset")
        video_asset_tag.set('client_video_id', 'external video')
        video_asset_tag.set('duration', '0.0')
        video_asset_tag.set('image', '')
        transcripts_tag = etree.Element('transcripts')
        transcript_tag = etree.Element('transcript')
        transcript_tag.set('file_format', transcripts_str.split('.')[-1])
        transcript_tag.set('language_code', 'en')
        transcript_tag.set('provider', 'Custom')
        video_tag.append(video_asset_tag)
        video_asset_tag.append(transcripts_tag)
        transcripts_tag.append(transcript_tag)
        # add the second transcript tag
        transcript2_tag = etree.Element('transcript')
        transcript2_tag.set('language', 'en')
        transcript2_tag.set('src', transcripts_str)
        video_tag.append(transcript2_tag)
    # write the file
    result = etree.tostring(video_tag, pretty_print = True)
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
def processAsset(component_path, out_folder, component, unit_filename):
    # copy the image to the assets folder
    out_path = os.path.join(out_folder, STATIC_FOLDER, unit_filename + '_' + component)
    shutil.copyfile(component_path, out_path)
#--------------------------------------------------------------------------------------------------
# upload the file to an online repository
# out_repo is a dictionary, { url, id, key }
# returns the url
def processUploadsToRepo(in_folder, in_filename, out_repo, out_filename):
    # print('out_repo', out_repo)
    # print('out_filename', out_filename)
    repo_url = out_repo.get('url')
    auth_id = out_repo.get('id')
    auth_key = out_repo.get('key')
    cloud_answer_url = repo_url + '/' + out_filename
    # read the file
    in_path = os.path.join(in_folder, in_filename)
    if os.path.isfile(in_path):
        pass
        # TODO Upload to Repo
        # TODO
        # TODO
    else:
        print('Answer does not exist: ' + in_path)
        print('in_folder', in_folder)
        print('in_filename', in_filename)
    return cloud_answer_url
#--------------------------------------------------------------------------------------------------
# upload files for problem submit
def uploadAnswers(component_path, settings, unit_filename):
    # upload the answer to the answer repository (this repo is private)
    component_folder = os.path.dirname(component_path)
    if 'answer' in settings.keys():
        answer_filename = settings['answer']
        processUploadsToRepo(component_folder, answer_filename, ANSWER_REPO, unit_filename + '_' + answer_filename)
    else:
        print('Settings does not contain the answer file: ' + component_folder)
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
                            component_type = processMd(component_path, out_folder, component_filename, unit_filename)
                            components.append([component_filename, component_type])
                    elif component_ext in ['htm','html']:
                        # this is an html snippet, only used in special cases
                        processHtml(component_path, out_folder, component_filename)
                        components.append([component_filename, 'html'])
                    elif component_ext in ASSET_EXTENSIONS:
                        # this is an asset that needs to get copied to the STATIC folder
                        processAsset(component_path, out_folder, component, unit_filename)
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
    in_folder = os.path.normpath(sys.argv[1])
    out_folder = os.path.normpath(sys.argv[2])

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
