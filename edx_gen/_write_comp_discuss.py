import sys, os
from lxml import etree
from edx_gen import  _edx_consts
from edx_gen import  _process_html
from edx_gen import  _css_settings
from edx_gen import  _mob_iframe
import __SETTINGS__
#--------------------------------------------------------------------------------------------------
# xml for discussion component
def tagForDiscussComp(component_path, filename, content, settings, unit_filename, unit_display_name):

    # ---- XML tag ----
    # <vertical display_name="Unit">
    #   <html url_name="09842ceb95f24a7390a08a341afae934"/>
    #   <discussion url_name="28461d49643f4ee597cfc385cccc5fd3" 
    #               xblock-family="xblock.v1" 
    #               discussion_category="Week 1xx" 
    #               discussion_target="Topic-Level Student-Visible Labelxx" 
    #               display_name="Discussionxx"/>
    # ----  ----  ----

    # create the main component tag
    component_tag = etree.Element('discussion')
    component_tag.set('xblock-family', 'xblock.v1')
    component_tag.set('url_name', filename)
    # verified only
    if 'verified_only' in settings and settings['verified_only'] == 'true':
        component_tag.set('group_access', '{"50":[2]}')
    # display name
    if 'display_name' in settings:
        component_tag.set('display_name', settings['display_name'])
    else:
        component_tag.set('display_name', 'Discussion')
    # category
    if 'discussion_category' in settings:
        component_tag.set('discussion_category', settings['discussion_category'])
    else:
        component_tag.set('discussion_category', unit_filename + ":" + unit_display_name)
    # target
    if 'discussion_target' in settings:
        component_tag.set('discussion_target', settings['discussion_target'])
    else:
        component_tag.set('discussion_target', 'Queries')

    # return the tag and type
    return [
        [component_tag, 'discussion']
    ]
#--------------------------------------------------------------------------------------------------
