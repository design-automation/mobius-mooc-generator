import sys, os
from lxml import etree
from edx_gen import  _edx_consts
from edx_gen import  _process_html
from edx_gen import  _css_settings
from edx_gen import  _mob_iframe
import __SETTINGS__
#--------------------------------------------------------------------------------------------------
WARNING = "      WARNING:"

EMBED_START = '<iframe src="'

EMBED_END = '" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>'

#--------------------------------------------------------------------------------------------------
# xml for google doc component
def tagForGoogleDocComp(filename, settings, unit_filename):

    # ---- XML tag ----
    # <google-document 
    #     url_name = "9c4bfb0a3ff04465939bbade3778140e" 
    #     xblock-family = "xblock.v1" 
    #     display_name = "Google Document" 
    #     alt_text = "" 
    #     embed_code = "&lt;iframe&#10; src=&quot;https://docs.google.com/forms/d/e/1FAIpQLScCy4XgLwL7PXE_53Mu5oK7orx1kTfhX9jhapobkbhC2Ft7eg/viewform&quot;&#10; frameborder=&quot;0&quot;&#10; width=&quot;960&quot;&#10; height=&quot;569&quot;&#10; allowfullscreen=&quot;true&quot;&#10; mozallowfullscreen=&quot;true&quot;&#10; webkitallowfullscreen=&quot;true&quot;&gt;&#10;&lt;/iframe&gt;&#10;"
    # />
    # ----  ----  ----

    # create the main component tag
    component_tag = etree.Element('google-document')
    component_tag.set('xblock-family', 'xblock.v1')
    component_tag.set('url_name', filename)
    # display name
    if 'display_name' in settings:
        component_tag.set('display_name', settings['display_name'])
        component_tag.set('alt_text', settings['display_name'])
    else:
        component_tag.set('display_name', 'Google Document')
        component_tag.set('alt_text', 'Google Document')
    # url
    if 'google_doc_url' in settings:
        embed_code = EMBED_START + settings['google_doc_url'] + EMBED_END
        component_tag.set('embed_code', embed_code)
    else:
        print(WARNING, 'Goole Doc component is missing "google_doc_url".', unit_filename)

    # return the tag and type
    return [
        [component_tag, 'google-doc']
    ]
#--------------------------------------------------------------------------------------------------
