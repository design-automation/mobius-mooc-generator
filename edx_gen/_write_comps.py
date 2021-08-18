import sys, os
import tarfile
import shutil
from edx_gen import  _edx_consts
from edx_gen import  _read_metadata
from edx_gen import  _write_structure
from edx_gen import  _write_comps
from edx_gen import  _write_comp_html
from edx_gen import  _write_comp_checkboxes
from edx_gen import  _write_comp_multiplechoice
from edx_gen import  _write_comp_submit
from edx_gen import  _write_comp_video
from edx_gen import  _write_comp_discuss
from edx_gen import  _markdown
from edx_gen import  _util
import __SETTINGS__
#--------------------------------------------------------------------------------------------------
# Text strings
WARNING = "      WARNING:"

#--------------------------------------------------------------------------------------------------
# write to either units folder or problems folder, depending on the type
def writeCompsForUnit(md_filepath, unit_filename):

    # print("component_path", component_path)

    # generate the files in the right folders
    tree_snippets = _markdown.convertMd(md_filepath)

    # check we have at least 2 snippets, the header and one component
    if len(tree_snippets) <= 1:
        print(WARNING, 'The markdown file does not seem to contain any components:', md_filepath)

    # get the display name of the unit
    first_h1_tag = list(tree_snippets[0].iter('h1'))[0]
    unit_display_name = first_h1_tag.get('display_name')

    # list to store all files
    unit_comps = []

    # process components
    for i in range(1, len(tree_snippets)):
        tree_snippet = tree_snippets[i]

        # generate the files
        new_filename = unit_filename + '_c' + str(i)
        comp_files = _writeFilesForSnippet(md_filepath, new_filename, tree_snippet, unit_filename, unit_display_name)
        unit_comps.extend(comp_files)

    # return the result
    return unit_comps

#--------------------------------------------------------------------------------------------------
# write to either units folder or problems folder, depending on the type
def _writeFilesForSnippet(md_filepath, comp_filename, tree_snippet, unit_filename, unit_display_name):

    meta_tag = None
    comp_type = None
    # meta_text = None

    # get the h1 tags
    h1_tags = list(tree_snippet.iter('h1'))
    if len(h1_tags) == 0:
        print(WARNING, 'The snippet does not start with any settings:', md_filepath)
        return

    # get the meta tag for the snippet
    meta_tag = h1_tags[0] # the first h1 the should contain the meta data

    # # check the meta tag text
    # meta_text = meta_tag.text.strip()
    # if meta_text == None or meta_text != 'UNIT':
    #     print(WARNING, 'The markdown file must start with the "UNIT" settings:', component_path)
    #     print(WARNING, 'Make sure that the first line of the markdown file is blank')

    # get the type for this component
    comp_type = meta_tag.get('type')
    if comp_type == None or comp_type not in _edx_consts.METADATA_ENUMS['type']:
        print(WARNING, 'The "type" setting is not recognised:', md_filepath)
        print(WARNING, '  Found:', comp_type)
        print(WARNING, '  Valid options:', _edx_consts.METADATA_ENUMS['type'])

    # write xml and/or html files
    if comp_type == 'html':

        # get the setting out of the meta_tag
        settings = _read_metadata.getMetaSettings(md_filepath, meta_tag, 
            _edx_consts.COMP_HTML_REQ, _edx_consts.COMP_HTML_OPT )

        # check that we have settings
        if not settings:
            print(WARNING, 'There seem to be no settings for this "html" component:', md_filepath)
            return

        # remove h1 meta_tag from the tree so it does not end up in the output
        tree_snippet.remove(meta_tag)

        # write .html file to COMP_HTML_FOLDER
        # write .xml file to COMP_HTML_FOLDER
        # return the list of files
        return _write_comp_html.writeXmlForHtmlComp(
            md_filepath, comp_filename, tree_snippet, settings, unit_filename)
    
    elif comp_type == 'problem-checkboxes':

        # get the setting out of the meta_tag
        settings = _read_metadata.getMetaSettings(md_filepath, meta_tag, 
            _edx_consts.COMP_PROB_QUIZ_REQ, _edx_consts.COMP_PROB_QUIZ_OPT )

        # check that we have settings
        if not settings:
            print(WARNING, 'There seem to be no settings for this "problem-checkboxes" component:', md_filepath)
            return

        # remove h1 meta_tag from the tree so it does not end up in the output
        tree_snippet.remove(meta_tag)

        # write .xml file to COMP_PROBS_FOLDER
        # return the list of files
        return _write_comp_checkboxes.writeXmlForProbCheckboxesComp(
            md_filepath, comp_filename, tree_snippet, settings, unit_filename)
    
    elif comp_type == 'problem-multiplechoice':

        # get the setting out of the meta_tag
        settings = _read_metadata.getMetaSettings(md_filepath, meta_tag, 
            _edx_consts.COMP_PROB_QUIZ_REQ, _edx_consts.COMP_PROB_QUIZ_OPT )

        # check that we have settings
        if not settings:
            print(WARNING, 'There seem to be no settings for this "problem-multiplechoice" component:', md_filepath)
            return

        # remove h1 meta_tag from the tree so it does not end up in the output
        tree_snippet.remove(meta_tag)

        # write .xml file to COMP_PROBS_FOLDER
        # return the list of files
        return _write_comp_multiplechoice.writeXmlForProbMultiplechoiceComp(
            md_filepath, comp_filename, tree_snippet, settings, unit_filename)

    elif comp_type == 'problem-submit':

        print("===PROBLEM SUBMIT===")
        # get the setting out of the meta_tag
        settings = _read_metadata.getMetaSettings(md_filepath, meta_tag, 
            _edx_consts.COMP_PROB_SUBMIT_REQ , _edx_consts.COMP_PROB_SUBMIT_OPT )

        # check that we have settings
        if not settings:
            print(WARNING, 'There seem to be no settings for this "problem-submit" component:', md_filepath)
            return

        # remove h1 meta_tag from the tree so it does not end up in the output
        tree_snippet.remove(meta_tag)

        # write .xml file to COMP_HTML_FOLDER
        # write .xml file to COMP_PROBS_FOLDER
        # return the list of files
        return _write_comp_submit.writeXmlForSubmitComp(
            md_filepath, comp_filename, tree_snippet, settings, unit_filename)
    
    elif comp_type == 'video':

        # get the setting out of the meta_tag
        settings = _read_metadata.getMetaSettings(
            md_filepath, meta_tag, _edx_consts.COMP_VIDEO_REQ, _edx_consts.COMP_VIDEO_OPT )

        # check that we have settings
        if not settings:
            print(WARNING, 'There seem to be no settings for this "video" component:', md_filepath)
            return

        # remove h1 meta_tag from the tree so it does not end up in the output
        tree_snippet.remove(meta_tag)

        # write .xml file to COMP_VIDS_FOLDER
        # for each language
        # write .html file to COMP_HTML_FOLDER
        # write .xml file to COMP_HTML_FOLDER
        # return the list of files
        return _write_comp_video.writeXmlForVidComp(
            md_filepath, comp_filename, settings, unit_filename)

    elif comp_type == 'discussion':

        # get the setting out of the meta_tag
        settings = _read_metadata.getMetaSettings(md_filepath, meta_tag, 
            _edx_consts.COMP_DISCUSS_REQ, _edx_consts.COMP_DISCUSS_OPT )

        # check that we have settings
        if not settings:
            print(WARNING, 'There seem to be no settings for this "discussion" component:', md_filepath)
            return

        # in this case, no files are written
        # we return the component tag instead
        return _write_comp_discuss.tagForDiscussComp(
            md_filepath, comp_filename, tree_snippet, settings, unit_filename, unit_display_name)

    else:
        print(WARNING, 'Component type not recognised:', comp_type, "in", md_filepath)


#--------------------------------------------------------------------------------------------------
