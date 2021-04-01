import sys, os
from lxml import etree
from edx_gen import  _edx_consts
from edx_gen import  _process_html
from edx_gen import  _css_settings
from edx_gen import  _mob_iframe
from edx_gen import  _util
import __SETTINGS__
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

    # process html
    _process_html.processHtmlTags(component_path, content, unit_filename)

    # write the html file
    html_out_path = os.path.join(sys.argv[2], _edx_consts.COMP_HTML_FOLDER, filename + '.html')
    with open(html_out_path, 'wb') as fout:
        if 'display_name' in  settings:
            h3_tag = etree.Element("h3")
            h3_tag.text = settings['display_name']
            h3_tag.set('style', _css_settings.H3_CSS)
            fout.write(etree.tostring(h3_tag, pretty_print = True))
        for tag in content:
            tag_result = etree.tostring(tag, pretty_print = True, method = "html")
            fout.write(tag_result)

    # create xml
    html_tag = etree.Element("html")
    for key in settings:
        if key not in ['type']:
            html_tag.set(key, settings[key])
    html_tag.set('filename', filename)
    result = etree.tostring(html_tag, pretty_print = True)

    # write the xml file
    xml_out_path = os.path.join(sys.argv[2], _edx_consts.COMP_HTML_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)

    # return the file name and folder
    return [[filename, _edx_consts.COMP_HTML_FOLDER]]
#--------------------------------------------------------------------------------------------------
