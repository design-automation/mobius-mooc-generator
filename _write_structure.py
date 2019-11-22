
import os
from lxml import etree
import __CONSTS__
import _edx_consts
import _read_metadata

#--------------------------------------------------------------------------------------------------
# Text strings
WARNING = "      WARNING:"

#--------------------------------------------------------------------------------------------------
# generate xml for a course
def writeXmlForRoot():
    # create a file in the root folder
    
    # ----  ----  ----
    # <course url_name="1234" org="abc" course="online101"/>
    # ----  ----  ----

    print("writing root xml")

    # get settings
    root_folder_settings = _read_metadata.getFolderMetaSettings(
        __CONSTS__.COURSE_PATH, _edx_consts.ROOT_FOLDER_REQ, _edx_consts.ROOT_FOLDER_OPT)

    # create xml
    course_tag = etree.Element("course")
    for key in root_folder_settings:
        course_tag.set(key, root_folder_settings[key])
    result = etree.tostring(course_tag, pretty_print=True)

    # write the file
    root_xml_out_path = os.path.join(__CONSTS__.OUTPUT_PATH, 'course.xml')
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
    if not sections:
        print(WARNING, 'There seem to be no sections:', in_folder)
        return

    # get settings
    course_folder_settings = _read_metadata.getFolderMetaSettings(
        in_folder, _edx_consts.COURSE_FOLDER_REQ, _edx_consts.COURSE_FOLDER_OPT)

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
    xml_out_path = os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.COURSE_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)

#--------------------------------------------------------------------------------------------------
# generate xml for a section, also called a chapter
# a section contains subsections
# examples, week 1, week 2
def writeXmlForSection(in_folder, filename, subsections):
    # create a file in the section folder ('chapter')

    # ----  ----  ----
    # <chapter display_name="Section">
    #     <sequential url_name="c717ae712f294fe397b72be2011b4ec0"/>
    #     <sequential url_name="c717ae712f294fe397b72be2011b4ec0"/>
    #     <sequential url_name="c717ae712f294fe397b72be2011b4ec0"/>
    # </chapter>
    # ----  ----  ----

    print("- writing section xml")
    if not subsections:
        print(WARNING, 'There seem to be no subsections:', in_folder)
        return

    # get settings
    section_folder_settings = _read_metadata.getFolderMetaSettings(
        in_folder, _edx_consts.SECTION_FOLDER_REQ, _edx_consts.SECTION_FOLDER_OPT)
    
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
    xml_out_path = os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.SECTION_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)

#--------------------------------------------------------------------------------------------------
# generate xml for a subsection, also called a sequence
# a subsection can contain units
# example, intorduction, shorts, assignments
def writeXmlForSubsection(in_folder, filename, units):
    # create a file in the subsection folder ('sequental')

    # ----  ----  ----
    # <sequential display_name="Section Title">
    #   <vertical url_name="fbb654358e4a4c0f8cc5bce4627ec82b"/>
    #   <vertical url_name="fbb654358e4a4c0f8cc5bce4627ec82b"/>
    # </sequential>
    # ----  ----  ----

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
    if not units:
        print(WARNING, 'There seem to be no units:', in_folder)
        return

    # get settings
    subsection_folder_settings = _read_metadata.getFolderMetaSettings(
        in_folder, _edx_consts.SUBSECTION_FOLDER_REQ, _edx_consts.SUBSECTION_FOLDER_OPT)
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
    xml_out_path = os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.SUBSECTION_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)

#--------------------------------------------------------------------------------------------------
# generate xml for a unit, also called a vertical
# a unit can contain many componets
def writeXmlForUnit(in_folder, filename, components):
    # create a file in the units folder ('vertical')

    # ----  ----  ----
    # <vertical display_name="Unit Title">
    #     <html url_name="7d3ba88c180745e5baf29084667409b2"/>
    #     <video url_name="05c171c507ab4d76830823f60075b0ae"/>
    #     <problem url_name="e2b890df14c1441ca66528ab58ca07b9"/>
    # </vertical>
    # ----  ----  ----

    print("--- writing unit xml")
    if not components:
        print(WARNING, 'There seem to be no components:', in_folder)
        return

    # get settings
    unit_folder_settings = _read_metadata.getFolderMetaSettings(
        in_folder, _edx_consts.UNIT_FOLDER_REQ, _edx_consts.UNIT_FOLDER_OPT)
    
    # create xml
    vertical_tag = etree.Element("vertical")
    for key in unit_folder_settings:
        vertical_tag.set(key, unit_folder_settings[key])

    for component in components:

        # get the component data
        component_filename = component[0]
        component_type = component[1] # 'html' or 'video' or 'quiz'
        if not component_type:
            continue # something went wrong
        component_cat = component_type
        if component_cat.startswith('problem'):
            component_cat = 'problem'

        # additinal processing for submit problems to add descriptio and language
        if component_type == 'problem-submit':
            prob_descr_tag = etree.Element('html')
            prob_descr_tag.set('url_name', component_filename)
            vertical_tag.append(prob_descr_tag)

        # add the main component
        component_tag = etree.Element(component_cat)
        component_tag.set('url_name', component_filename)
        vertical_tag.append(component_tag)

        # additional processing for videos to add language bar below
        if component_type == 'video' and len( __CONSTS__.LANGUAGES) > 1:
            video_lang_tag = etree.Element('html')
            video_lang_tag.set('url_name', component_filename)
            vertical_tag.append(video_lang_tag)

    # convert the component data to string
    component_data = etree.tostring(vertical_tag, pretty_print = True)

    # write file
    xml_out_path = os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.UNIT_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(component_data)

#--------------------------------------------------------------------------------------------------
