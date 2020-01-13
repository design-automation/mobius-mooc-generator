import sys, os
from lxml import etree
import urllib
from edx_gen import  _edx_consts
from edx_gen import  _css_settings
from edx_gen import  _mob_iframe
from edx_gen import  _util
import __SETTINGS__
#--------------------------------------------------------------------------------------------------
# Text strings
WARNING = "      WARNING:"
#--------------------------------------------------------------------------------------------------
# process a hrefs
def processHtmlTags(component_path, content_root_tag, unit_filename):

    # process headings
    h3_tags = list(content_root_tag.iter('h3'))
    h4_tags = list(content_root_tag.iter('h4'))
    h5_tags = list(content_root_tag.iter('h5'))
    _processHeadingsTags(h3_tags, h4_tags, h5_tags)

    # process pre
    pre_tags = list(content_root_tag.iter('pre'))
    _processPreTags(pre_tags)

    # process hrefs
    a_tags = list(content_root_tag.iter('a'))
    _processHtmlATags(component_path, a_tags, unit_filename)

    # process images
    img_tags = list(content_root_tag.iter('img'))
    _processHtmlImgTags(component_path, img_tags, unit_filename)

#--------------------------------------------------------------------------------------------------
# process headings
def _processHeadingsTags(h3_tags, h4_tags, h5_tags):
    for h3_tag in h3_tags:
        h3_tag.set('style', _css_settings.H3_CSS)
    for h4_tag in h4_tags:
        h4_tag.set('style', _css_settings.H4_CSS)
    for h5_tag in h5_tags:
        h5_tag.set('style', _css_settings.H5_CSS)

#--------------------------------------------------------------------------------------------------
# process pre
def _processPreTags(pre_tags):
    for pre_tag in pre_tags:
        pre_tag.set('style', _css_settings.PRE_CSS)
        children = pre_tag.getchildren()
        if len(children) > 0:
            first_child = children[0]
            if first_child.tag == 'code':
                code = first_child.text
                if code.startswith('\n'):
                    code = code[1:]
                if code.endswith('\n'):
                    code = code[:-1]
                first_child.text = code
#--------------------------------------------------------------------------------------------------
# process images
def _processHtmlImgTags(component_path, img_tags, unit_filename):

    for img_tag in img_tags:

        # create new image
        new_img_tag = etree.Element("img")
        for key in img_tag.keys():
            if not key in ['src', 'modal']:
                new_img_tag.set(key, img_tag.get(key))
        
        # get modal setting
        modal = False
        if 'modal' in img_tag.keys() and img_tag.get('modal') == 'true':
            modal = True

        # add css
        if modal:
            new_img_tag.set('style', _css_settings.IMAGE_MODAL_CSS)
        else:
            new_img_tag.set('style', _css_settings.IMAGE_CSS)
        src = img_tag.get('src')

        # get the new src for the image
        new_src = ''
        if src.startswith('/') or src.startswith('http'):
            new_src = src
        else:
            # check that that the file exists
            component_dir = os.path.dirname(component_path)
            image_filepath = os.path.normpath(component_dir + '/' + src)
            if (not os.path.exists(image_filepath) or not os.path.isfile(image_filepath)):
                print(WARNING, 'The image file does not exist: "' + image_filepath +'" in', component_path)
            # new src
            new_src = '/' + _edx_consts.STATIC_FOLDER + '/' + unit_filename + '_' + src
        new_img_tag.set('src', new_src)
            
        # create figure
        figure_tag = etree.Element("figure")
        if _css_settings.FIGURE_CSS:
            figure_tag.set('style', _css_settings.FIGURE_CSS)
        if modal:
            a_tag = etree.Element("a")
            a_tag.set('target', 'image')
            a_tag.set('href', new_src)
            a_tag.append(new_img_tag)
            figure_tag.append(a_tag)
        else:
            figure_tag.append(new_img_tag)

        #  create caption for the figure
        if 'alt' in img_tag.keys():
            figcaption_tag = etree.Element("figcaption")
            if _css_settings.FIGCAPTION_CSS:
                figcaption_tag.set('style', _css_settings.FIGCAPTION_CSS)
            figcaption_tag.text = img_tag.get('alt')
            figure_tag.append(figcaption_tag)

        # replace the existing image with the figure
        img_tag.getparent().replace(img_tag, figure_tag)

#--------------------------------------------------------------------------------------------------
# process a hrefs
def _processHtmlATags(component_path, a_tags, unit_filename):

    for a_tag in a_tags:

        # get the href
        href = a_tag.get('href')
        if not href:
            print(WARNING, 'An <a/> tag has no "href" attribute:', unit_filename)
            return

        # create the new tag, either an <iframe/> or an image <a/>
        if _util.ends(href, __SETTINGS__.MOB_EXAMPLE_FILENAMES):
            _createMobIframeTag(a_tag, href, unit_filename)

        # an answer! this should not happen
        elif _util.ends(href, __SETTINGS__.MOB_ANSWER_FILENAMES):
            print(WARNING, 'Found an answer being displayed to the learners:', unit_filename)

        # normal a tag
        else:
            _updateATag(a_tag, href, unit_filename)

#--------------------------------------------------------------------------------------------------
# create a mob Iframe tag
def _createMobIframeTag(a_tag, href, unit_filename):

    # create mobius iframe
    mob_settings = dict([[item.strip() for item in pair.split('=')] for pair in a_tag.text.split(',')])

    # create the iframe
    new_iframe_tag = _mob_iframe.createMobIframe(href, mob_settings, unit_filename)

    # replace the existing a with the new tag
    a_tag.getparent().replace(a_tag, new_iframe_tag)

# create an image tag
def _updateATag(a_tag, href, unit_filename):

    # break down the url
    href_parts = list(urllib.parse.urlparse(href))
    href_file = None
    href_file_ext = None
    href_path = href_parts[2]
    if href_path and '.' in href_path:
        href_file = href_path.split('/')[-1]
        href_file_ext = href_path.split('.')[-1]

    # create the new href
    new_href = None

    # no extension, so must be a url like http://google.com
    if href_file_ext == None or href_file_ext == '':
        return

    # an asset that goes to the edx static folder
    elif href_file_ext in __SETTINGS__.EDX_ASSET_FILE_EXTENSIONS:
        new_href = '/' + _edx_consts.STATIC_FOLDER + '/' + unit_filename + '_' + href_file
        a_tag.set('href', new_href)

    # something unknown
    else:
        new_href = href
        print(WARNING, 'Found an unrecognised href:', href, href_file_ext, unit_filename)

#--------------------------------------------------------------------------------------------------