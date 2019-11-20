import sys, os
import tarfile
import shutil
import urllib
from lxml import etree
import markdown
import html
from __CONSTS__ import COURSE_PATH, OUTPUT_PATH, SETTINGS_FILENAME, ASSET_FILE_EXTENSIONS, LANGUAGES, S3_FILE_EXTENSIONS, S3_ANSWERS_BUCKET, S3_EXAMPLES_BUCKET, S3_ANSWER_FILENAME
# create the markdow instance
md = markdown.Markdown(extensions = ['extra', 'meta', 'sane_lists'])
#--------------------------------------------------------------------------------------------------
# available languages: ["us", "uk", "pt", "es", "zh", "fr", "de", "nl"]
ALL_LANGUAGES = {
    'en': 'English',
    'zh': 'Mandarin',
    'pt': 'Portuguese',
    'fr': 'French',
    'es': 'Spanish',
    'de': 'German',
    'nl': 'Dutch'
} 
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
# File extensions used for different types of assets
# Images, PDFs, Video captions, these will be copied to the STATIC_FOLDER
ASSET_FILE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'srt']
# Upload extensions
UPLOAD_EXTENSIONS = ['mob']
#--------------------------------------------------------------------------------------------------
# Metadata settings for folders
# root
ROOT_FOLDER_REQ = ['org', 'course', 'url_name']
ROOT_FOLDER_OPT = ['visible_to_staff_only', 'start']
# course
COURSE_FOLDER_REQ = ['display_name']
COURSE_FOLDER_OPT = ['visible_to_staff_only', 'enrollment_start', 'start', 'end', 'self_paced', 'is_new',
    'cert_html_view_enabled', 'course_image', 'graceperiod', 'instructor_info', 'invitation_only', 
    'language', 'learning_info', 'minimum_grade_credit', 'wiki_slug', 'cosmetic_display_price']
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
COMP_VIDEO_REQ = ['type']
COMP_VIDEO_OPT = ['voice', 'display_name', 'edx_video_id', 'visible_to_staff_only', 'start', 'download_video', 
    'show_captions', 'sub', 'html5_sources', 'youtube_id_1_0', 'html5_sources']
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
IMAGE_CSS = ';'.join([
    'width:400px',
    'display:block',
    'margin-left:auto',
    'margin-right:auto',
    'border-style:solid',
    'border-width:1px'
    ])
FIGCAPTION_CSS = ';'.join([
    'width:400px',
    'display:block',
    'margin-left:auto',
    'margin-right:auto',
    'margin-top:8px',
    'text-align:center',
    'font-style:italic'
    ])
LANG_BUTTON_CSS = ';'.join([
    'padding:2px',
    'margin:1px',
    'border-style:solid',
    'border-width:1px',
    'display:inline',
    'cursor:pointer'
    ])
SELECT_LANG_SCRIPT = '''
function myFunction(lang) {
  document.getElementById('chinese').style="display:none";
  document.getElementById('french').style="display:none";
  if (lang !== 'none') {
    document.getElementById(lang).style="display:block";
  }
}
'''
#--------------------------------------------------------------------------------------------------
# Iframe settings
# Any <a> tags with files with these extension will be replaced with iframes
MOB_IFRAME_EXTENSIONS = ['mob']
MOB_IFRAME_WIDTH = '100%' 
MOB_IFRAME_HEIGHT ='600px' 
MOB_IFRAME_STYLE = 'border: 1px solid black;'
#--------------------------------------------------------------------------------------------------
WARNING = "      WARNING:"
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
            print(WARNING, 'An <a/> tag has no "href" attribute:', a_elem)
            return
        # break down the url
        href_parts = list(urllib.parse.urlparse(href))
        href_file = None
        href_file_ext = None
        href_path = href_parts[2]
        if href_path and '.' in href_path:
            href_file = href_path.split('/')[-1]
            href_file_ext = href_path.split('.')[-1]
        iframe_tag = None
        # create the new href
        # either the file needs to be uploaded to a repo
        # or the file has already been copied to the STATIC_FOLDER
        new_href = None
        if href_file_ext == None or href_file_ext == '':
            new_href = href
        elif href_file_ext in ASSET_FILE_EXTENSIONS:
            new_href = '/' + STATIC_FOLDER + '/' + unit_filename + '_' + href_file
        elif href_file_ext in S3_FILE_EXTENSIONS:
            # for example https://sct-mooc-examples.s3.amazonaws.com/hello.txt
            new_href = 'https://' + S3_EXAMPLES_BUCKET + '.s3.amazonaws.com/' + unit_filename + '_' + href_file
        else:
            new_href = href
            print(WARNING, 'Found an unrecognised href:', href, href_file_ext)
        # create the new tag, either an <iframe/> or a <a/>
        if href_file_ext in MOB_IFRAME_EXTENSIONS:
            # create iframe
            mob_settings = dict([[item.strip() for item in pair.split('=')] for pair in a_elem.text.split(',')])
            iframe_src = 'https://mobius.design-automation.net/'
            if 'mobius' in mob_settings:
                iframe_src += mob_settings['mobius'] + '?file=' + new_href
                del mob_settings['mobius']
                for key in mob_settings:
                    iframe_src += '&' +  key + '=' + mob_settings[key]
            else:
                print(WARNING, 'Mobius Iframe data is missing the "publish" setting:', mob_settings)
                print(WARNING, 'Possible options include "mobius = publish" and "mobius = dashboard".')
            iframe_tag = etree.Element('iframe')
            iframe_tag.set('width', MOB_IFRAME_WIDTH)
            iframe_tag.set('height', MOB_IFRAME_HEIGHT)
            iframe_tag.set('style', MOB_IFRAME_STYLE)
            iframe_tag.set('src', iframe_src)
        else:
            iframe_tag = etree.Element('a')
            for key in a_elem:
                if key not in ['href']:
                    iframe_tag.set(key, a_elem.get(key))
            iframe_tag.set('src', new_href)
        # replace the existing a with the new tag
        a_elem.getparent().replace(a_elem, iframe_tag)
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
def writeXmlForRoot():
    # create a file in the root folder
    # ----  ----  ----
    # <course url_name="1234" org="abc" course="online101"/>
    # ----  ----  ----
    print("writing root xml")
    # get settings
    root_folder_settings = getFolderMetaSettings(COURSE_PATH, ROOT_FOLDER_REQ, ROOT_FOLDER_OPT)
    # create xml
    course_tag = etree.Element("course")
    for key in root_folder_settings:
        course_tag.set(key, root_folder_settings[key])
    result = etree.tostring(course_tag, pretty_print=True)
    # write the file
    root_xml_out_path = os.path.join(OUTPUT_PATH, 'course.xml')
    with open(root_xml_out_path, 'wb') as fout:
        fout.write(result)
    # return the url_name, this is needed for the next level, the filename for course
    return root_folder_settings['url_name']
#--------------------------------------------------------------------------------------------------
# generate xml for a course
def writeXmlForCourse(in_folder, filename, sections):
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
    xml_out_path = os.path.join(OUTPUT_PATH, COURSE_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
#--------------------------------------------------------------------------------------------------
# generate xml for a section, also called a chapter
# a section contains subsections
# examples, week 1, week 2
def writeXmlForSection(in_folder, filename, subsections):
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
    xml_out_path = os.path.join(OUTPUT_PATH, SECTION_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
#--------------------------------------------------------------------------------------------------
# generate xml for a subsection, also called a sequence
# a subsection can contain units
# example, intorduction, shorts, assignments
def writeXmlForSubsection(in_folder, filename, units):
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
    xml_out_path = os.path.join(OUTPUT_PATH, SUBSECTION_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
#--------------------------------------------------------------------------------------------------
# generate xml for a unit, also called a vertical
# a unit can contain many componets
def writeXmlForUnit(in_folder, filename, components):
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
        if component_type == 'video' and len(LANGUAGES) > 1:
            video_lang_tag = etree.Element('html')
            video_lang_tag.set('url_name', component_filename)
            vertical_tag.append(video_lang_tag)
    result = etree.tostring(vertical_tag, pretty_print = True)
    # write file
    xml_out_path = os.path.join(OUTPUT_PATH, UNIT_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
#--------------------------------------------------------------------------------------------------
# read md
# write to either units folder or problems folder, depending on the type
def processMd(component_path, component_filename, unit_filename):
    # print("component_path", component_path)
    # generate the files in the right folders
    [content, meta] = getComponentContentMeta(component_path)
    # get component type
    comp_type = meta['type']
    if comp_type:
        comp_type = comp_type[0]
    else:
        print(WARNING, 'Error: Component type missing:', component_path)
        return 
    # generate xml files
    if comp_type == 'html':
        settings = getMetaSettings(component_path, meta, COMP_HTML_REQ, COMP_HTML_OPT )
        writeXmlForHtmlComp(component_path, component_filename, content, settings, unit_filename)
    elif comp_type == 'problem-checkboxes':
        settings = getMetaSettings(component_path, meta, COMP_PROB_CHECKBOXES_REQ, COMP_PROB_CHECKBOXES_OPT )
        writeXmlForProbCheckboxesComp(component_path, component_filename, content, settings, unit_filename)
    elif comp_type == 'problem-submit':
        settings = getMetaSettings(component_path, meta, COMP_PROB_SUBMIT_REQ , COMP_PROB_SUBMIT_OPT )
        writeXmlForSubmitComp(component_path, component_filename, content, settings, unit_filename)
    elif comp_type == 'video':
        settings = getMetaSettings(component_path, meta, COMP_VIDEO_REQ, COMP_VIDEO_OPT )
        writeXmlForVidComp(component_filename, content, settings, unit_filename)
    else:
        print(WARNING, 'Error: Component type not recognised:', comp_type, "in", component_path)
    # return the component type, which is needed for generating the xml for the subsection
    if comp_type.startswith('problem'):
        comp_type = 'problem'
    return comp_type
#--------------------------------------------------------------------------------------------------
# write xml for Html component
def writeXmlForHtmlComp(component_path, filename, content, settings, unit_filename):
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
    html_out_path = os.path.join(OUTPUT_PATH, COMP_HTML_FOLDER, filename + '.html')
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
    xml_out_path = os.path.join(OUTPUT_PATH, COMP_HTML_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
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
    # process the html
    content_root_tag = etree.fromstring(content)
    # process hrefs
    a_elems = list(content_root_tag.iter('a'))
    setHrefHtml(component_path, a_elems, unit_filename)
    # process images
    img_elems = list(content_root_tag.iter('img'))
    setImageHtml(img_elems, unit_filename)
    # process the elements
    # these will be converted to <label>, and solution <p> elements
    # the elements are split using '===', there should be two splits
    labels = []
    choices = []
    solutions = []
    found_splitter = 0 # found ===
    elems = content_root_tag.getchildren()
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
    xml_out_path = os.path.join(OUTPUT_PATH, COMP_PROBS_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
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
        if key not in ['type', 'question', 'queuename', 'answer']:
            problem_tag.set(key, settings[key])
    queuename = 'Dummy_Queuename'
    if 'queuename' in settings:
        queuename = settings.get('queuename')
    else:
        print(WARNING, 'Submit problem is missing metadata: queuename.', filename)
    coderesponse_tag.set('queuename', queuename)
    question = 'Dummy_Question'
    if 'question' in settings:
        question = settings.get('question')
    else:
        print(WARNING, 'Submit problem is missing metadata: question.', filename)
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
    # process the elements
    # these will be converted to <label>, and solution <p> elements
    # the elements are spli using '==='
    # everything before the split is added to <label>
    # everything after the split is added to 
    labels = []
    solutions = []
    found_splitter = 0 # found ===
    elems = content_root_tag.getchildren()
    if elems:
        for elem in elems:
            if (elem.text and elem.text.startswith('===')):
                found_splitter += 1
            else:
                if found_splitter == 0:
                    labels.append(elem)
                else:
                    solutions.append(elem)
    else:
        print(WARNING, 'Submit problem is missing content.', filename)
    # add labels to the coderesponse_tag
    if labels:
        label_tag = etree.Element("label") 
        coderesponse_tag.append(label_tag)
        for label in labels:
            label_tag.append(label)
    else:
        print(WARNING, 'Submit problem is missing a description of the problem.', filename)
    # add <filesubmission> and <codeparam> to the coderesponse_tag
    coderesponse_tag.append(etree.Element("filesubmission") )
    codeparam_tag = etree.Element("codeparam")
    codeparam_tag.append(grader_payload_tag)
    coderesponse_tag.append(codeparam_tag)
    # add <solution> to the coderesponse_tag
    if solutions:
        solution_tag = etree.Element("solution")
        coderesponse_tag.append(solution_tag)
        for solution in solutions:
            solution_tag.append(solution)
    else:
        print(WARNING, 'Submit problem is missing a description of the solution.', filename)
    # convert problem_tag to string
    result = etree.tostring(problem_tag, pretty_print=True)
    # write the file
    xml_out_path = os.path.join(OUTPUT_PATH, COMP_PROBS_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
#--------------------------------------------------------------------------------------------------
# write xml for video component
def writeXmlForVidComp(filename, content, settings, unit_filename):
    # ----  ----  ----
    # Youtube Video
    # <video 
    #   url_name="section_week_1_subsection_2_shorts_unit_1_text_and_videos_02_video" 
    #   sub="" 
    #   transcripts="{&quot;en&quot;: &quot;7d76f250-0000-42ea-8aba-c0c0ce845280-en.srt&quot;}" 
    #   display_name="A Video" edx_video_id="7d76f250-0000-42ea-8aba-c0c0ce845280" 
    #   youtube_id_1_0="3_yD_cEKoCk" >
    #
    #   <video_asset client_video_id="External Video" duration="0.0" image="">
    #     <transcripts>
    #       <transcript file_format="srt" language_code="en" provider="Custom"/>
    #     </transcripts>
    #   </video_asset>
    #   <transcript language="en" src="7d76f250-0000-42ea-8aba-c0c0ce845280-en.srt"/>
    # </video>
    # ----  ----  ----
    # Non-Youtube video
    # <video 
    #   url_name="section_week_1_subsection_2_shorts_unit_1_text_and_videos_02_video" 
    #   sub="" 
    #   transcripts="{&quot;en&quot;: &quot;7d76f250-0000-42ea-8aba-c0c0ce845280-en.srt&quot;}" 
    #   display_name="A Video" edx_video_id="7d76f250-0000-42ea-8aba-c0c0ce845280" 
    #   html5_sources="[&quot;https://aaa.bbb.com/ccc.mp4&quot;]"  >
    #
    #   <video_asset client_video_id="External Video" duration="0.0" image="">
    #     <transcripts>
    #       <transcript file_format="srt" language_code="en" provider="Custom"/>
    #     </transcripts>
    #   </video_asset>
    #   <transcript language="en" src="7d76f250-0000-42ea-8aba-c0c0ce845280-en.srt"/>
    # </video>
    # ----  ----  ----
    # Video with multiple transcripts in different languages
    # <video url_name="section_week_1_subsection_2_shorts_unit_1_02_video" 
    #   sub="" 
    #   transcripts="{&quot;en&quot;: &quot;d8446257-1d13-4b5c-a21a-a4ca57b06cf5-en.srt&quot;, &quot;zh&quot;: &quot;d8446257-1d13-4b5c-a21a-a4ca57b06cf5-zh.srt&quot;}" 
    #   display_name="Basic Blocking" 
    #   edx_video_id="d8446257-1d13-4b5c-a21a-a4ca57b06cf5" 
    #   html5_sources="[&quot;https://mooc-s3cf.s3-ap-southeast-1.amazonaws.com/Ct2.7.1_uk_comp.mp4&quot;]" >
    #
    #   <source src="https://mooc-s3cf.s3-ap-southeast-1.amazonaws.com/Ct2.7.1_uk_comp.mp4"/>
    #   <video_asset client_video_id="External Video" duration="0.0" image="">
    #     <transcripts>
    #       <transcript file_format="srt" language_code="en" provider="Custom"/>
    #       <transcript file_format="srt" language_code="zh" provider="Custom"/>
    #     </transcripts>
    #   </video_asset>
    #   <transcript language="en" src="d8446257-1d13-4b5c-a21a-a4ca57b06cf5-en.srt"/>
    #   <transcript language="zh" src="d8446257-1d13-4b5c-a21a-a4ca57b06cf5-zh.srt"/>
    # </video>
    # 
    # create xml
    video_tag = etree.Element("video")
    video_tag.set('url_name', filename)
    for key in settings:
        if key not in ['type', 'transcript', 'title', 'voice']:
            video_tag.set(key, settings[key])
    # add youtube
    if 'youtube_id_1_0' in settings:
        video_tag.set('youtube', '1.00:' + settings['youtube_id_1_0'])
    else:
        video_tag.set('youtube_id_1_0', '')
    # set the transcript object
    transcripts_obj = {}
    for lang in LANGUAGES:
        transcripts_obj[lang] = filename + '_sub_' + lang + '.srt'
    # escape this dict so that we get &quot; but do not escale the &
    video_tag_transcripts_list = []
    for k in transcripts_obj:
        video_tag_transcripts_list.append( '"' + k + '":"' + transcripts_obj[k] + '"' )
    video_tag.set('transcripts', '{' + ','.join(video_tag_transcripts_list) + '}')
    # add the source tag
    html5_sources_list = []
    if 'html5_sources' in settings:
        html5_sources_list = eval(bytes(settings['html5_sources'], "utf-8").decode("unicode_escape"))
        source_tag = etree.Element("source")
        source_tag.set('src', html5_sources_list[0])
        video_tag.append(source_tag)
    # add the video asset tag
    video_asset_tag = etree.Element("video_asset")
    video_asset_tag.set('client_video_id', 'external video')
    video_asset_tag.set('duration', '0.0')
    video_asset_tag.set('image', '')
    video_tag.append(video_asset_tag)
    transcripts_tag = etree.Element('transcripts')
    for lang in LANGUAGES:
        transcript_tag = etree.Element('transcript')
        transcript_tag.set('file_format', 'srt')
        transcript_tag.set('language_code', lang)
        transcript_tag.set('provider', 'Custom')
        transcripts_tag.append(transcript_tag)
    video_asset_tag.append(transcripts_tag)
    # add the transcript tags
    for lang in LANGUAGES:
        transcript2_tag = etree.Element('transcript')
        transcript2_tag.set('language', lang)
        transcript2_tag.set('src', transcripts_obj[lang])
        video_tag.append(transcript2_tag)
    # write the file
    result = etree.tostring(video_tag, pretty_print = True)
    xml_out_path = os.path.join(OUTPUT_PATH, COMP_VIDS_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)
    # generate the language options
    if 'html5_sources' in settings and len(LANGUAGES) > 1:
        # create the html file for video languages
        # create script str
        script_str = '\nfunction selLang(lang) {\n'
        for lang in LANGUAGES[1:]:
            script_str += '  document.getElementById("' + lang + '").style="display:none";\n'
        script_str += '  if (lang !== "none") { \n'
        script_str += '    document.getElementById(lang).style="display:block";\n'
        script_str += '  }\n'
        script_str += '}\n'
        # script tag
        script_tag = etree.Element("script")
        script_tag.text = script_str
        # p tag
        p_languages_tag = etree.Element("p")
        p_languages_tag.set('style','display:inline')
        p_languages_tag.text = 'View video in other language: '
        button_tag = etree.Element("div")
        button_tag.set('style', LANG_BUTTON_CSS)
        button_tag.set('onclick', 'selLang("none")')
        button_tag.text = 'None'
        p_languages_tag.append(button_tag)
        div_tag =  etree.Element("div")
        for lang in LANGUAGES[1:]:
            # p with row of buttons
            if lang != 'en':
                button_tag = etree.Element("div")
                button_tag.set('style', LANG_BUTTON_CSS)
                button_tag.set('onclick', 'selLang("' + lang + '")')
                button_tag.text = ALL_LANGUAGES[lang]
                p_languages_tag.append(button_tag)
            # videos
            video_tag = etree.Element("video")
            div_tag.append(video_tag)
            video_tag.set('id', lang)
            video_tag.set('style', 'display:none')
            video_tag.set('width', '100%')
            video_tag.set('controls', '')
            # source tag 
            source_tag = etree.Element("source")
            video_tag.append(source_tag)
            source_tag.set('src', html5_sources_list[0][:-4] + '_' + lang + html5_sources_list[0][-4:])
            source_tag.set('type', 'video/mp4')
            source_tag.text = 'Your browser does not support the video tag.'
        # write the html file for video languages
        xml_out_path = os.path.join(OUTPUT_PATH, COMP_HTML_FOLDER, filename + '.html')
        with open(xml_out_path, 'wb') as fout:
            fout.write(etree.tostring(script_tag, pretty_print = True))
            fout.write(etree.tostring(p_languages_tag, pretty_print = True))
            fout.write(etree.tostring(div_tag, pretty_print = True))
        # create the xml file for video languages
        html_tag = etree.Element("html")
        html_tag.set('display_name', 'View Video in Other Language')
        html_tag.set('filename', filename)
        # write the xml file for video languages
        xml_out_path = os.path.join(OUTPUT_PATH, COMP_HTML_FOLDER, filename + '.xml')
        with open(xml_out_path, 'wb') as fout:
            fout.write(etree.tostring(html_tag, pretty_print = True))
#--------------------------------------------------------------------------------------------------
# this is just in case there are some html files
# write to units to the correct folder
# returns void
def processHtml(component_path, filename):
    with open(component_path, 'r') as f_read:
        contents = f_read.read()
        xml_path = ''
        if (contents.startswith('<html')):
            xml_path = os.path.join(OUTPUT_PATH, COMP_HTML_FOLDER, filename + '.xml')
        elif (contents.startswith('<problem')):
            xml_path = os.path.join(OUTPUT_PATH, COMP_PROBS_FOLDER, filename + '.xml')
        elif (contents.startswith('<video')):
            xml_path = os.path.join(OUTPUT_PATH, COMP_VIDS_FOLDER, filename + '.xml')
        # write the content
        with open(xml_path, 'w') as f:
            f.write(contents)
#--------------------------------------------------------------------------------------------------
# write the image to the assets folder
# returns void
def processAsset(component_path, component, unit_filename):
    # copy the image to the assets folder
    out_path = os.path.join(OUTPUT_PATH, STATIC_FOLDER, unit_filename + '_' + component)
    shutil.copyfile(component_path, out_path)
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
def processCourse():
    # get the main mooc input folder, which we assume is the first folder
    courses = getSubFolders(COURSE_PATH)
    if (len(courses) != 1):
        print(WARNING, 'There should only be one folder in the root folder.')
        return
    course_path = courses[0][1]
    # make the folders inside dist
    os.mkdir(os.path.join(OUTPUT_PATH, COURSE_FOLDER))
    os.mkdir(os.path.join(OUTPUT_PATH, SECTION_FOLDER))
    os.mkdir(os.path.join(OUTPUT_PATH, SUBSECTION_FOLDER))
    os.mkdir(os.path.join(OUTPUT_PATH, UNIT_FOLDER))
    os.mkdir(os.path.join(OUTPUT_PATH, COMP_HTML_FOLDER))
    os.mkdir(os.path.join(OUTPUT_PATH, COMP_VIDS_FOLDER))
    os.mkdir(os.path.join(OUTPUT_PATH, COMP_PROBS_FOLDER))
    os.mkdir(os.path.join(OUTPUT_PATH, STATIC_FOLDER))
    # create the root xml file
    course_filename = writeXmlForRoot()
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
                            component_type = processMd(component_path, component_filename, unit_filename)
                            components.append([component_filename, component_type])
                    elif component_ext in ['htm','html']:
                        # this is an html snippet, only used in special cases
                        processHtml(component_path, component_filename)
                        components.append([component_filename, 'html'])
                    elif component_ext in ASSET_FILE_EXTENSIONS:
                        # this is an asset that needs to get copied to the STATIC folder
                        processAsset(component_path, component, unit_filename)
                    else:
                        pass
                        # could be any other file, just ignore and continue
                        # print("Warning: File extension not recognised. Expecting either .md or .xml:", component_path)
                writeXmlForUnit(unit_path, unit_filename, components)
            writeXmlForSubsection(subsection_path, subsection_filename, units)
        writeXmlForSection(section_path, section_filename, subsections)
    writeXmlForCourse(course_path, course_filename, sections)
#--------------------------------------------------------------------------------------------------
def main():
    print("Start compiling")

    # check the input and output folders
    print("in", COURSE_PATH)
    if (not os.path.isdir(COURSE_PATH)):
        print("The input path is not a valid path")
        return
    print("out", OUTPUT_PATH)
    try:
        if (os.path.isdir(OUTPUT_PATH)):
            print("Deleting contents in " + OUTPUT_PATH)
            shutil.rmtree(OUTPUT_PATH)
        os.mkdir(OUTPUT_PATH)
    except:
        print("Failed to create the output folder: " + OUTPUT_PATH)
    
    # create content
    processCourse()

    # create the tar file
    [out_folder_path, out_folder_name] = os.path.split(OUTPUT_PATH)
    tar = tarfile.open(out_folder_name + ".tar.gz", "w:gz")
    os.chdir(out_folder_path)
    tar.add(out_folder_name, recursive=True)
    tar.close()

    print("Finish compiling")
#--------------------------------------------------------------------------------------------------
main()
