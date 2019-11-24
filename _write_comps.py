import sys, os
import tarfile
import shutil
import __CONSTS__ 
import _edx_consts
import _read_metadata
import _write_structure
import _write_comps
import _write_comp_html
import _write_comp_checkboxes
import _write_comp_submit
import _write_comp_video
import _markdown
import _util

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

    # list to store all files
    files = []

    # process htmls
    for i in range(1, len(tree_snippets)):
        tree_snippet = tree_snippets[i]

        # generate the files
        new_filename = unit_filename + '_c' + str(i)
        comp_files = _writeFilesForSnippet(md_filepath, new_filename, tree_snippet, unit_filename)
        files.extend(comp_files)

    # return the result
    return files

#--------------------------------------------------------------------------------------------------
# write to either units folder or problems folder, depending on the type
def _writeFilesForSnippet(md_filepath, comp_filename, tree_snippet, unit_filename):

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
        print(WARNING, 'The "type"setting is not recognised:', md_filepath)
        print(WARNING, '  Found:', comp_type)
        print(WARNING, '  Valid options:', _edx_consts.METADATA_ENUMS['type'])

    # generate xml files
    if comp_type == 'html':

        # get the setting out of the meta_tag
        settings = _read_metadata.getMetaSettings(md_filepath, meta_tag, 
            _edx_consts.COMP_HTML_REQ, _edx_consts.COMP_HTML_OPT )

        # check that we have ssettings
        if not settings:
            print(WARNING, 'There seem to be no settings for this "html" component:', md_filepath)
            return

        # remove h1 meta_tag from the tree so it does not end up in the output
        tree_snippet.remove(meta_tag)

        # write the files and return the list of files
        return _write_comp_html.writeXmlForHtmlComp(
            md_filepath, comp_filename, tree_snippet, settings, unit_filename)
    
    elif comp_type == 'problem-checkboxes':

        # get the setting out of the meta_tag
        settings = _read_metadata.getMetaSettings(md_filepath, meta_tag, 
            _edx_consts.COMP_PROB_CHECKBOXES_REQ, _edx_consts.COMP_PROB_CHECKBOXES_OPT )

        # check that we have settings
        if not settings:
            print(WARNING, 'There seem to be no settings for this "problem-checkboxes" component:', md_filepath)
            return

        # remove h1 meta_tag from the tree so it does not end up in the output
        tree_snippet.remove(meta_tag)

        # write the files and return the list of files
        return _write_comp_checkboxes.writeXmlForProbCheckboxesComp(
            md_filepath, comp_filename, tree_snippet, settings, unit_filename)
    
    elif comp_type == 'problem-submit':

        # get the setting out of the meta_tag
        settings = _read_metadata.getMetaSettings(md_filepath, meta_tag, 
            _edx_consts.COMP_PROB_SUBMIT_REQ , _edx_consts.COMP_PROB_SUBMIT_OPT )
            
        # check that we have settings
        if not settings:
            print(WARNING, 'There seem to be no settings for this "problem-submit" component:', md_filepath)
            return

        # remove h1 meta_tag from the tree so it does not end up in the output
        tree_snippet.remove(meta_tag)

        # write the files and return the list of files
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

        # write the files and return the list of files
        return _write_comp_video.writeXmlForVidComp( comp_filename, settings, unit_filename)
    
    else:
        print(WARNING, 'Component type not recognised:', comp_type, "in", md_filepath)


#--------------------------------------------------------------------------------------------------
