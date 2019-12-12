import sys, os
import _edx_consts

#--------------------------------------------------------------------------------------------------
# Text strings
WARNING = "      WARNING:"
ERROR   = "      ERROR:"
#--------------------------------------------------------------------------------------------------
# get the settings from a component or a folder
# returns a dict of settings
def getMetaSettings(input, meta_tag, req_names, opt_names=None):

    # process requires metadata
    req_values = {}
    for req_name in req_names:
        if req_name in meta_tag.keys():
            req_values[req_name] = meta_tag.get(req_name)
        else:
            print(ERROR, 'Failed to find the required metadata "', req_name, '" in: ', input)
            print(ERROR, '  Found the following metadata keys:', meta_tag.keys())
            raise Exception

    # process optional metadata
    opt_values = {}
    if opt_names:
        for name in opt_names:
            if name in meta_tag.keys():
                opt_values[name] = meta_tag.get(name)
                if name in _edx_consts.METADATA_ENUMS:
                    if not opt_values[name] in _edx_consts.METADATA_ENUMS[name]:
                        print(WARNING, "Unrecognised metadata value '" + name + "':'" + opt_values[name] + "' in: ", input)
    
    # check the names in meta
    for key in meta_tag.keys():
        if not key in req_names and not key in opt_names:
            print(WARNING, "Unrecognised metadata '" + key + "' in: ", input)
            print(WARNING, "  Required metadata:", req_names)
            print(WARNING, "  Optional metadata:", opt_names)
    
    # return the settings as two dicts or one dict
    req_values.update(opt_values)
    return req_values
#--------------------------------------------------------------------------------------------------
