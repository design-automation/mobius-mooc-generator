import sys, os
from lxml import etree
import urllib
import __CONSTS__
import _edx_consts
import _css_settings
import _mob_iframe
#--------------------------------------------------------------------------------------------------
# Text strings
WARNING = "      WARNING:"
#--------------------------------------------------------------------------------------------------
# process a hrefs
def processHtmlTags(component_path, content_root_tag, unit_filename):

    # process hrefs
    a_tags = list(content_root_tag.iter('a'))
    _processHtmlATags(component_path, a_tags, unit_filename)

    # process images
    img_tags = list(content_root_tag.iter('img'))
    _processHtmlImgTags(component_path, img_tags, unit_filename)

#--------------------------------------------------------------------------------------------------
# process images
def _processHtmlImgTags(component_path, img_elems, unit_filename):

    for img_elem in img_elems:

        # create new image
        img_tag = etree.Element("img")
        for key in img_elem:
            if key not in ['src']:
                img_tag.set(key, img_elem.get(key))
        if _css_settings.IMAGE_CSS:
            img_tag.set('style', _css_settings.IMAGE_CSS)
        src = img_elem.get('src')

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
        img_tag.set('src', new_src)

        # create an a href tag
        a_tag = etree.Element("a")
        a_tag.set('target', 'image')
        a_tag.set('href', new_src)
        a_tag.append(img_tag)

        # create figure
        figure_tag = etree.Element("figure")
        if _css_settings.FIGURE_CSS:
            figure_tag.set('style', _css_settings.FIGURE_CSS)
        figure_tag.append(a_tag)

        #  create caption for the figure
        if 'alt' in img_elem.keys():
            figcaption_tag = etree.Element("figcaption")
            if _css_settings.FIGCAPTION_CSS:
                figcaption_tag.set('style', _css_settings.FIGCAPTION_CSS)
            figcaption_tag.text = img_elem.get('alt')
            figure_tag.append(figcaption_tag)

        # replace the existing image with the figure
        img_elem.getparent().replace(img_elem, figure_tag)

#--------------------------------------------------------------------------------------------------
# process a hrefs
def _processHtmlATags(component_path, a_elems, unit_filename):

    for a_elem in a_elems:

        # get the href
        href = a_elem.get('href')
        if not href:
            print(WARNING, 'An <a/> tag has no "href" attribute:', unit_filename)
            return

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
            new_href = href

        # an asset that goes to the edx static folder
        elif href_file_ext in __CONSTS__.ASSET_FILE_EXTENSIONS:
            new_href = '/' + _edx_consts.STATIC_FOLDER + '/' + unit_filename + '_' + href_file

        # an example that gets uploaded to a s3 examples bucket
        elif href_path.endswith(__CONSTS__.MOB_EXAMPLE_FILENAME):
            new_href = href

        # an answer! this should not happen
        elif href_path.endswith(__CONSTS__.MOB_ANSWER_FILENAME):
            new_href = href
            print(WARNING, 'Found an answer being displayed to the learners:', unit_filename)

        # something unknown
        else:
            new_href = href
            print(WARNING, 'Found an unrecognised href:', href, href_file_ext, unit_filename)

        # create the new tag, either an <iframe/> or an image <a/>
        new_tag = None
        if href_path.endswith(__CONSTS__.MOB_EXAMPLE_FILENAME):

            # create mobius iframe
            mob_settings = dict([[item.strip() for item in pair.split('=')] for pair in a_elem.text.split(',')])

            # create the iframe
            new_tag = _mob_iframe.createMobIframe(href, mob_settings, unit_filename)

        else:

            # create the image
            new_tag = etree.Element('a')
            for key in a_elem:
                if key not in ['href']:
                    new_tag.set(key, a_elem.get(key))
            new_tag.set('src', new_href)

        # replace the existing a with the new tag
        a_elem.getparent().replace(a_elem, new_tag)

#--------------------------------------------------------------------------------------------------
