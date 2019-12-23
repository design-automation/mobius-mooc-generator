
import sys, os
from lxml import etree
from edx_gen import  _edx_consts
from edx_gen import  _read_metadata
from edx_gen import  _markdown
from edx_gen import  _util
import __SETTINGS__
#--------------------------------------------------------------------------------------------------
# Text strings
WARNING = "      WARNING:"
 
#--------------------------------------------------------------------------------------------------
# get the settings from a folder
def _getFolderMetaSettings(in_folder, req_names, opt_names=None):

    # we look for a file that has a name that has an md extension
    tree_snippets = None
    filename = None
    try:

        # the the files
        files = _util.getFiles(in_folder)

        # get the list of files in the folder
        for [filename, filepath] in files:
            filex = filename.lower().split('.')[1]

            # is this a settings file?
            if filex == 'md':

                tree_snippets = _markdown.convertMd(filepath)

            # if we have found the file, we stop looking
            if tree_snippets is not None and len(tree_snippets) > 0:
                break

        if tree_snippets is None or len(tree_snippets) == 0:
            raise Exception()
    except:
        print(WARNING, "Failed to read settings for the folder: ", in_folder, sys.exc_info()[0])

    # get the first item in the list of htmls, which would be the only thing
    tree_snippet = tree_snippets[0]

    # get the h1 tags
    h1_tags = list(tree_snippet.iter('h1'))
    if len(h1_tags) == 0:
        print(WARNING, 'The snippet does not start with any settings:', in_folder, filename)
        return

    # get the meta tag
    meta_tag = h1_tags[0] # the first h1 the should contain the meta data

    # # check meta tag text
    # meta_text = meta_tag.text.strip()
    # if meta_text == None or not _util.starts(meta_text, _edx_consts.SETTINGS_FOLDERS):
    #     print(WARNING, 'The markdown file must start with the folder settings:', in_folder, filename)
    #     print(WARNING, '  Found:', meta_text)
    #     print(WARNING, '  Valid values:', _edx_consts.SETTINGS_FOLDERS)

    # return the metadata
    settings = _read_metadata.getMetaSettings(filepath, meta_tag, req_names, opt_names)
    return settings

#--------------------------------------------------------------------------------------------------
# generate xml for a course
def writeXmlForRoot():
    # create a file in the root folder
    
    # ----  ----  ----
    # <course url_name="1234" org="abc" course="online101"/>
    # ----  ----  ----

    print("writing root xml")

    # get settings
    settings = _getFolderMetaSettings(
        sys.argv[1], _edx_consts.ROOT_FOLDER_REQ, _edx_consts.ROOT_FOLDER_OPT)

    # check we have settings
    if not settings:
        print(WARNING, 'There seem to be no settings for root folder:')
        return

    # create xml
    course_tag = etree.Element("course")
    for key in settings:
        course_tag.set(key, settings[key])
    result = etree.tostring(course_tag, pretty_print=True)

    # write the file
    root_xml_out_path = os.path.join(sys.argv[2], 'course.xml')
    with open(root_xml_out_path, 'wb') as fout:
        fout.write(result)

    # return the url_name, this is needed for the next level, the filename for course
    return settings['url_name']

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
    settings = _getFolderMetaSettings(
        in_folder, _edx_consts.COURSE_FOLDER_REQ, _edx_consts.COURSE_FOLDER_OPT)

    # check we have settings
    if not settings:
        print(WARNING, 'There seem to be no settings for course folder:', in_folder)
        return

    # create xml
    course_tag = etree.Element("course")
    for key in settings:
        if not key in ['wiki_slug']:
            course_tag.set(key, settings[key])
    for section in sections:
        chapter_tag = etree.Element("chapter")
        chapter_tag.set('url_name', section)
        course_tag.append(chapter_tag)
    if 'wiki_slug' in settings:
        wiki_tag = etree.Element("wiki")
        wiki_tag.set('slug', settings['wiki_slug'])
        course_tag.append(wiki_tag)
    result = etree.tostring(course_tag, pretty_print = True)

    # write the file
    xml_out_path = os.path.join(sys.argv[2], _edx_consts.COURSE_FOLDER, filename + '.xml')
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
    settings = _getFolderMetaSettings(
        in_folder, _edx_consts.SECTION_FOLDER_REQ, _edx_consts.SECTION_FOLDER_OPT)
    
    # check we have settings
    if not settings:
        print(WARNING, 'There seem to be no settings for this section folder:', in_folder)
        return

    # create xml
    chapter_tag = etree.Element("chapter")
    for key in settings:
        chapter_tag.set(key, settings[key])
    for subsection in subsections:
        sequential_tag = etree.Element("sequential")
        sequential_tag.set('url_name',subsection)
        chapter_tag.append(sequential_tag)
    result = etree.tostring(chapter_tag, pretty_print = True)

    # write the file
    xml_out_path = os.path.join(sys.argv[2], _edx_consts.SECTION_FOLDER, filename + '.xml')
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
    settings = _getFolderMetaSettings(
        in_folder, _edx_consts.SUBSECTION_FOLDER_REQ, _edx_consts.SUBSECTION_FOLDER_OPT)

    # check we have settings
    if not settings:
        print(WARNING, 'There seem to be no settings for this subsection folder:', in_folder)
        return

    # graded ?
    if 'graded' in settings:
        if settings['graded'] == 'true':
            settings['format'] = 'Assignment'

    # create the root tag
    sequential_tag = etree.Element("sequential")
    for key in settings:
        sequential_tag.set(key, settings[key])

    # add the units
    for unit in units:
        vertical_tag = etree.Element("vertical")
        vertical_tag.set('url_name', unit)
        sequential_tag.append(vertical_tag)
    result = etree.tostring(sequential_tag, pretty_print=True)

    # write the file
    xml_out_path = os.path.join(sys.argv[2], _edx_consts.SUBSECTION_FOLDER, filename + '.xml')
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
    #     <discussion 
    #         url_name="28461d49643f4ee597cfc385cccc5fd3" 
    #         xblock-family="xblock.v1" 
    #         display_name="Discussion" 
    #         discussion_category="Week 1" 
    #         discussion_target="Topic-Level Student-Visible Label"
    #     />
    # </vertical>
    # ----  ----  ----

    print("--- writing unit xml")

    # print(in_folder, filename, components)

    if not components:
        print(WARNING, 'There seem to be no components:', in_folder)
        return

    # get settings
    settings = _getFolderMetaSettings(
        in_folder, _edx_consts.UNIT_FOLDER_REQ, _edx_consts.UNIT_FOLDER_OPT)
    
    # check we have settings
    if not settings:
        print(WARNING, 'There seem to be no settings for this unit folder:', in_folder)
        return

    # create xml
    vertical_tag = etree.Element("vertical")
    for key in settings:
        vertical_tag.set(key, settings[key])

    # loop through the components
    for component in components:

        # get the component data
        comp_filename = component[0]
        comp_type = component[1] # 'html' or 'video' or 'problem'

        # create the main component tag
        component_tag = etree.Element(comp_type)

        # normal components
        if comp_type in ['html', 'video', 'problem']:

            # check the file exists
            filepath = sys.argv[2] + '/' + comp_type + '/' + comp_filename + '.xml'
            if not os.path.exists(filepath):
                print(WARNING, 'Something went wrong. A file does not exist:', filepath)

            # create the main component tag
            component_tag = etree.Element(comp_type)
            component_tag.set('url_name', comp_filename)
            vertical_tag.append(component_tag)

        # discussion components
        elif comp_type == 'discussion':
            
            # component tag is the comp_filename
            vertical_tag.append(comp_filename)

        else:
            print(WARNING, 'Something went wrong. Component type not recognised:', comp_type)

    # convert the component data to string
    component_data = etree.tostring(vertical_tag, pretty_print = True)

    # write file
    xml_out_path = os.path.join(sys.argv[2], _edx_consts.UNIT_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(component_data)

#--------------------------------------------------------------------------------------------------
