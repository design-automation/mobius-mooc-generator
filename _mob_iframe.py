import sys, os
from lxml import etree
import urllib
import _edx_consts
import _css_settings
import __SETTINGS__
#--------------------------------------------------------------------------------------------------
# Text strings
WARNING = "      WARNING:"

#--------------------------------------------------------------------------------------------------
MODES = ['gallery', 'dashboard', 'flowchart', 'editor', 'publish']
#--------------------------------------------------------------------------------------------------
# create an iframe with a mobius model inside it
def createMobIframe(mob_filename, mob_settings, unit_filename):
 
    # constcat the mob file url
    # this matches the url created in mob_uploader.py
    mob_file_url = __SETTINGS__.S3_LINKS_URL + __SETTINGS__.S3_MOOC_FOLDER + '/' +  __SETTINGS__.S3_EXAMPLES_FOLDER + '/' + unit_filename + '_' + mob_filename

    # the mobius src
    iframe_src = __SETTINGS__.MOB_URL
    if 'mobius' in mob_settings:

        # get the mode
        mode = mob_settings['mobius']
        del mob_settings['mobius']

        # check if this mode is OK
        if (mode not in MODES):
            print(WARNING, 'Mobius mode is not recognised:', mode)
            print(WARNING, 'Valid modes are as follows: ', MODES)

        # construct the src
        iframe_src += '/' + mode + '?file=' + mob_file_url
        for key in mob_settings:
            iframe_src += '&' +  key + '=' + mob_settings[key]
    else:
        print(WARNING, 'Mobius Iframe data is missing the "publish" setting:', mob_settings)
        print(WARNING, 'Possible options include "mobius = publish" and "mobius = dashboard".')

    # the iframe tag
    iframe_tag = etree.Element('iframe')
    iframe_tag.set('width', _css_settings.MOB_IFRAME_WIDTH)
    iframe_tag.set('height', _css_settings.MOB_IFRAME_HEIGHT)
    iframe_tag.set('style', _css_settings.MOB_IFRAME_STYLE)
    iframe_tag.set('src', iframe_src)

    # return the iframe tag
    return iframe_tag