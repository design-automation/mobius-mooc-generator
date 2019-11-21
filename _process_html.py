from lxml import etree
import urllib
import __CONSTS__
import _edx_consts
import _css_settings
#--------------------------------------------------------------------------------------------------
# Text strings
WARNING = "      WARNING:"
#--------------------------------------------------------------------------------------------------
# process images
def setImageHtml(img_elems, unit_filename):

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
def setHrefHtml(component_path, a_elems, unit_filename):

    for a_elem in a_elems:

        # get the href
        href = a_elem.get('href')
        if not href:
            print(WARNING, 'An <a/> tag has no "href" attribute:', a_elem)
            return

        # break down the url
        href_parts = list(urllib.parse.urlparse(href))
        href_file = None
        href_file_ext = None
        href_path = href_parts[2]
        if href_path and '.' in href_path:
            href_file = href_path.split('/')[-1]
            href_file_ext = href_path.split('.')[-1]
        iframe_tag = None

        # create the new href
        # either the file needs to be uploaded to a repo
        # or the file has already been copied to the STATIC_FOLDER
        new_href = None
        if href_file_ext == None or href_file_ext == '':
            new_href = href
        elif href_file_ext in __CONSTS__.ASSET_FILE_EXTENSIONS:
            new_href = '/' + _edx_consts.STATIC_FOLDER + '/' + unit_filename + '_' + href_file
        elif href_file_ext in __CONSTS__.S3_FILE_EXTENSIONS:
            # for example https://sct-mooc-examples.s3.amazonaws.com/hello.txt
            new_href = 'https://' + __CONSTS__.S3_EXAMPLES_BUCKET + '.s3.amazonaws.com/' + unit_filename + '_' + href_file
        else:
            new_href = href
            print(WARNING, 'Found an unrecognised href:', href, href_file_ext)

        # create the new tag, either an <iframe/> or a <a/>
        if href_file_ext in __CONSTS__.MOB_IFRAME_EXTENSIONS:

            # create iframe
            mob_settings = dict([[item.strip() for item in pair.split('=')] for pair in a_elem.text.split(',')])
            iframe_src = 'https://mobius.design-automation.net/'
            if 'mobius' in mob_settings:
                iframe_src += mob_settings['mobius'] + '?file=' + new_href
                del mob_settings['mobius']
                for key in mob_settings:
                    iframe_src += '&' +  key + '=' + mob_settings[key]
            else:
                print(WARNING, 'Mobius Iframe data is missing the "publish" setting:', mob_settings)
                print(WARNING, 'Possible options include "mobius = publish" and "mobius = dashboard".')
            iframe_tag = etree.Element('iframe')
            iframe_tag.set('width', _css_settings.MOB_IFRAME_WIDTH)
            iframe_tag.set('height', _css_settings.MOB_IFRAME_HEIGHT)
            iframe_tag.set('style', _css_settings.MOB_IFRAME_STYLE)
            iframe_tag.set('src', iframe_src)
        else:
            iframe_tag = etree.Element('a')
            for key in a_elem:
                if key not in ['href']:
                    iframe_tag.set(key, a_elem.get(key))
            iframe_tag.set('src', new_href)

        # replace the existing a with the new tag
        a_elem.getparent().replace(a_elem, iframe_tag)

#--------------------------------------------------------------------------------------------------
