import sys, os
from lxml import etree
import urllib
from edx_gen import  _edx_consts
from edx_gen import  _css_settings
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

    # check size
    small = False
    if 'size' in mob_settings and mob_settings['size'] == 'small':
        small = True
    
    if small:
        iframe_tag.set('width', _css_settings.MOB_MINI_IFRAME_WIDTH)
        iframe_tag.set('height', _css_settings.MOB_MINI_IFRAME_HEIGHT)
    else:
        iframe_tag.set('width', _css_settings.MOB_IFRAME_WIDTH)
        iframe_tag.set('height', _css_settings.MOB_IFRAME_HEIGHT)
    iframe_tag.set('style', _css_settings.MOB_IFRAME_STYLE)
    iframe_tag.set('src', iframe_src)
    iframe_tag.text = 'Mobius Modeller'

    # add a div
    div_tag = etree.Element('div')
    div_tag.append(iframe_tag)
    a_tag = etree.Element('a')
    a_tag.set('href', iframe_src)
    a_tag.set('target', 'Mobius')
    a_tag.text = 'Open Mobius in a separate browser tab.'
    p_tag = etree.Element('p')
    p_tag.append(a_tag)
    div_tag.append(p_tag)

    # return the div tag
    return div_tag
