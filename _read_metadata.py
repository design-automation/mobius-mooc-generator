import os, sys
import markdown
import _edx_consts

#--------------------------------------------------------------------------------------------------
# create the markdow instance
md = markdown.Markdown(extensions = ['extra', 'meta', 'sane_lists'])

#--------------------------------------------------------------------------------------------------
# converts markdown to html
# returns the html string (in xml tags) and the metadata object
def convertMd(data):

    if data:
        
        content = '<root>' + md.convert(data) + '</root>'
        meta = md.Meta

        return [content, meta]

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
                if name in _edx_consts.METADATA_ENUMS:
                    if not opt_values[name] in _edx_consts.METADATA_ENUMS[name]:
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

        # get the list of files in the folder
        for filename in os.listdir(in_folder):

            # is this a settings file?
            if filename.endswith("settings.md"):
                in_path = os.path.join(in_folder, filename)
                with open(in_path, 'r') as fin:
                    data = fin.read()

                    # process markdown, html and meta data (using extension)
                    [_, meta] = convertMd(data)

            # if we have found the file, we stop looking
            if in_path and meta:
                break

        if not in_path or not meta:
            raise Exception()
    except:
        print("Error: Failed to read settings for the folder: ", in_folder, sys.exc_info()[0])

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
