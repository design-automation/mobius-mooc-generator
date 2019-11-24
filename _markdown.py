import sys, os
import markdown
from lxml import etree
import _util
import _edx_consts

#--------------------------------------------------------------------------------------------------
# Text strings
WARNING = "      WARNING:"

#--------------------------------------------------------------------------------------------------
# create the markdow instance
md = markdown.Markdown(extensions = ['extra', 'sane_lists'])

#--------------------------------------------------------------------------------------------------
# converts markdown to html
# returns the html string (in xml tags)
def convertMd(in_path):

    # we look for a file that has a name that ends with 'settings.md'
    html = None

    # read the settings file
    try:
        with open(in_path, 'r') as fin:

            # test = md.convert( fin.read() )

            # print ('-------------------------')
            # print ( "TEST", repr(test) )
            # print ('-------------------------')

            # raise Exception

            lines = fin.readlines()

            # print ('-------------------------')
            # print ( "LINES OF TEXT", repr(lines) )
            # print ('-------------------------')

            snippets = _preprocess( lines )

            # print ('-------------------------')
            # print ( "TEXT AFTER PREPROCESSING", repr(snippets) )
            # print ('-------------------------')

            html_snippets = [md.convert( snippet ) for snippet in snippets]

            # print ('-------------------------')
            # print ( "HTML AFTER CONV", repr(html_snippets) )
            # print ('-------------------------')

            tree_snippets = [etree.fromstring('<root>' + html + '</root>') for html in html_snippets]

            # print ('-------------------------')
            # print ( tree_snippets )
            # print ('-------------------------')

    except:
        print("Error: Failed to read file: ", in_path, sys.exc_info()[0])
        raise Exception

    # return html
    
    return tree_snippets

#--------------------------------------------------------------------------------------------------
# Preprocess the md
def _preprocess(data):

    # add custom attribs to the end of the line above
    new_lines = ['']
    found_attribs = False
    for line in data:
        line = line.strip()
        if line.startswith('{:') and not '}' in line:
            found_attribs = True
        if found_attribs:
            new_lines[-1] += ' ' + line + ' '
        else:
            new_lines.append(line)
        if found_attribs and '}' in line:
            found_attribs = False
    
    # group the lines into snippets
    snippets = [[]]
    for line in new_lines:
        if _util.starts(line, _edx_consts.MD_SNIPPET_MARKERS):
            snippets.append([])
        snippets[-1].append(line)
    
    # join the snippets into strings
    snippet_strs = []
    for snippet in snippets:
        joined_str = '\n'.join(snippet)
        if len(joined_str) > 0:
            snippet_strs.append(joined_str)

    # return array of snippet strings
    return snippet_strs

#--------------------------------------------------------------------------------------------------
