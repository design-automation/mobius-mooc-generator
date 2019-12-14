import sys, os
from lxml import etree
from edx_gen import  _edx_consts
from edx_gen import  _process_html
from edx_gen import  _css_settings
from edx_gen import  _mob_iframe
import __SETTINGS__
#--------------------------------------------------------------------------------------------------
ALL_LANGUAGES = {
    'en': 'English',
    'zh': 'Mandarin',
    'pt': 'Portuguese',
    'fr': 'French',
    'es': 'Spanish',
    'de': 'German',
    'nl': 'Dutch'
} 
#--------------------------------------------------------------------------------------------------
WARNING = "      WARNING:"

#--------------------------------------------------------------------------------------------------
# write xml for video component
def writeXmlForVidComp(component_path, filename, settings, unit_filename):

    # ----  ----  ----
    # Youtube Video
    # <video 
    #   url_name="section_week_1_subsection_2_shorts_unit_1_text_and_videos_02_video" 
    #   sub="" 
    #   transcripts="{&quot;en&quot;: &quot;7d76f250-0000-42ea-8aba-c0c0ce845280-en.srt&quot;}" 
    #   display_name="A Video" edx_video_id="7d76f250-0000-42ea-8aba-c0c0ce845280" 
    #   youtube_id_1_0="3_yD_cEKoCk" >
    #
    #   <video_asset client_video_id="External Video" duration="0.0" image="">
    #     <transcripts>
    #       <transcript file_format="srt" language_code="en" provider="Custom"/>
    #     </transcripts>
    #   </video_asset>
    #   <transcript language="en" src="7d76f250-0000-42ea-8aba-c0c0ce845280-en.srt"/>
    # </video>
    # ----  ----  ----

    # ----  ----  ----
    # Non-Youtube video
    # <video 
    #   url_name="section_week_1_subsection_2_shorts_unit_1_text_and_videos_02_video" 
    #   sub="" 
    #   transcripts="{&quot;en&quot;: &quot;7d76f250-0000-42ea-8aba-c0c0ce845280-en.srt&quot;}" 
    #   display_name="A Video" edx_video_id="7d76f250-0000-42ea-8aba-c0c0ce845280" 
    #   html5_sources="[&quot;https://aaa.bbb.com/ccc.mp4&quot;]"  >
    #
    #   <video_asset client_video_id="External Video" duration="0.0" image="">
    #     <transcripts>
    #       <transcript file_format="srt" language_code="en" provider="Custom"/>
    #     </transcripts>
    #   </video_asset>
    #   <transcript language="en" src="7d76f250-0000-42ea-8aba-c0c0ce845280-en.srt"/>
    # </video>
    # ----  ----  ----

    # ----  ----  ----
    # Video with multiple transcripts in different languages
    # <video url_name="section_week_1_subsection_2_shorts_unit_1_02_video" 
    #   sub="" 
    #   transcripts="{&quot;en&quot;: &quot;d8446257-1d13-4b5c-a21a-a4ca57b06cf5-en.srt&quot;, &quot;zh&quot;: &quot;d8446257-1d13-4b5c-a21a-a4ca57b06cf5-zh.srt&quot;}" 
    #   display_name="Basic Blocking" 
    #   edx_video_id="d8446257-1d13-4b5c-a21a-a4ca57b06cf5" 
    #   html5_sources="[&quot;https://mooc-s3cf.s3-ap-southeast-1.amazonaws.com/Ct2.7.1_uk_comp.mp4&quot;]" >
    #
    #   <source src="https://mooc-s3cf.s3-ap-southeast-1.amazonaws.com/Ct2.7.1_uk_comp.mp4"/>
    #   <video_asset client_video_id="External Video" duration="0.0" image="">
    #     <transcripts>
    #       <transcript file_format="srt" language_code="en" provider="Custom"/>
    #       <transcript file_format="srt" language_code="zh" provider="Custom"/>
    #     </transcripts>
    #   </video_asset>
    #   <transcript language="en" src="d8446257-1d13-4b5c-a21a-a4ca57b06cf5-en.srt"/>
    #   <transcript language="zh" src="d8446257-1d13-4b5c-a21a-a4ca57b06cf5-zh.srt"/>
    # </video>
    # 

    # create xml
    video_tag = etree.Element("video")
    video_tag.set('url_name', filename)
    for key in settings:
        if key not in ['type', 'transcript', 'title', 'video_filename']:
            video_tag.set(key, settings[key])

    # check we have either youtube_id_1_0 or video
    if not 'youtube_id_1_0' in settings and not 'video_filename' in settings:
        print(WARNING, 'A video component must have either a "youtube_id_1_0" setting or a "video" setting:', unit_filename)

    # add youtube
    if 'youtube_id_1_0' in settings:
        video_tag.set('youtube', '1.00:' + settings['youtube_id_1_0'])
    else:
        video_tag.set('youtube_id_1_0', '')

    # add the video asset tag
    video_asset_tag = etree.Element("video_asset")
    video_asset_tag.set('client_video_id', 'external video')
    video_asset_tag.set('duration', '0.0')
    video_asset_tag.set('image', '')
    video_tag.append(video_asset_tag)

    video_urls = {}

    if 'video_filename' in settings:

        # get the filename
        video_filename_ext = settings['video_filename'].strip()
        [video_filename, video_ext] = video_filename_ext.split('.')

        # the dir of this component
        component_dir = os.path.dirname(component_path)

        # set the transcript object
        transcripts_obj = {}
        for lang in __SETTINGS__.LANGUAGES:
            transcripts_obj[lang] = unit_filename + '_' + video_filename + '_sub_' + lang + '.srt'

            # check that that srt files for each language exist
            video_filepath = os.path.normpath(component_dir + '/' + video_filename + '_sub_' + lang + '.srt')
            if (not os.path.exists(video_filepath) or not os.path.isfile(video_filepath)):
                print(WARNING, 'The video srt file does not exist: "' + video_filepath +'" in', component_path)

        # escape this dict so that we get &quot; but do not escale the &
        video_tag_transcripts_list = []
        for k in transcripts_obj:
            video_tag_transcripts_list.append( '"' + k + '":"' + transcripts_obj[k] + '"' )
        video_tag.set('transcripts', '{' + ','.join(video_tag_transcripts_list) + '}')


        # for example "https://mooc-s3cf.s3-ap-southeast-1.amazonaws.com/Fruit+basket_uk.mp4"]
        # create the video urls
        
        url_base = __SETTINGS__.S3_LINKS_URL + __SETTINGS__.S3_MOOC_FOLDER + '/' + __SETTINGS__.S3_VIDEOS_FOLDER + '/'
        for lang in __SETTINGS__.LANGUAGES:
            video_urls[lang] = url_base  + video_filename + '_' + lang + '.' + video_ext

        video_url_default = video_urls['en']
        if video_url_default == None:
            video_url_default = video_urls[video_urls.keys()[0]]

        # set the html5_sources
        # html5_sources="[&quot;https://mooc-s3cf.s3-ap-southeast-1.amazonaws.com/Ct2.7.1_uk_comp.mp4&quot;]"
        video_tag.set('html5_sources', '["' + video_url_default + '"]')

        # add the source tag
        source_tag = etree.Element("source")
        source_tag.set('src', video_url_default)
        video_tag.append(source_tag)

        # add the transcripts tag to the video asset tag
        transcripts_tag = etree.Element('transcripts')
        for lang in __SETTINGS__.LANGUAGES:
            transcript_tag = etree.Element('transcript')
            transcript_tag.set('file_format', 'srt')
            transcript_tag.set('language_code', lang)
            transcript_tag.set('provider', 'Custom')
            transcripts_tag.append(transcript_tag)
        video_asset_tag.append(transcripts_tag)

        # add the second set of transcript tags under video
        for lang in __SETTINGS__.LANGUAGES:
            transcript2_tag = etree.Element('transcript')
            transcript2_tag.set('language', lang)
            transcript2_tag.set('src', transcripts_obj[lang])
            video_tag.append(transcript2_tag)

    # write the file
    video_data = etree.tostring(video_tag, pretty_print = True)
    video_xml_out_path = os.path.join(sys.argv[2], _edx_consts.COMP_VIDS_FOLDER, filename + '.xml')
    with open(video_xml_out_path, 'wb') as fout:
        fout.write(video_data)

    # creat a list of files to return
    files = [
        [filename, _edx_consts.COMP_VIDS_FOLDER]
    ]

    # generate the language options
    if 'video_filename' in settings and len(__SETTINGS__.LANGUAGES) > 1:

        # ['https://mooc-s3cf.s3-ap-southeast-1.amazonaws.com/SCT101X/2019/TST1.0.1.mp4']

        # create the html file for video languages

        # create script str
        script_str = '\nfunction selLang(lang) {\n'
        for lang in __SETTINGS__.LANGUAGES[1:]:
            script_str += '  document.getElementById("' + lang + '").style="display:none";\n'
        script_str += '  if (lang !== "none") { \n'
        script_str += '    document.getElementById(lang).style="display:block";\n'
        script_str += '  }\n'
        script_str += '}\n'

        # script tag
        script_tag = etree.Element("script")
        script_tag.text = script_str

        # p tag
        p_languages_tag = etree.Element("p")
        p_languages_tag.set('style','display:inline')
        p_languages_tag.text = 'View video in other language: '
        button_tag = etree.Element("div")
        button_tag.set('style', _css_settings.LANG_BUTTON_CSS)
        button_tag.set('onclick', 'selLang("none")')
        button_tag.text = 'None'
        p_languages_tag.append(button_tag)
        div_tag =  etree.Element("div")

        # for each langaue
        for lang in __SETTINGS__.LANGUAGES[1:]:

            # p with row of buttons
            if lang != 'en':
                button_tag = etree.Element("div")
                button_tag.set('style', _css_settings.LANG_BUTTON_CSS)
                button_tag.set('onclick', 'selLang("' + lang + '")')
                button_tag.text = ALL_LANGUAGES[lang]
                p_languages_tag.append(button_tag)

            # videos
            video_tag = etree.Element("video")
            div_tag.append(video_tag)
            video_tag.set('id', lang)
            video_tag.set('style', 'display:none')
            video_tag.set('width', '100%')
            video_tag.set('controls', '')

            # source tag 
            source_tag = etree.Element("source")
            video_tag.append(source_tag)
            source_tag.set('src', video_urls[lang])
            source_tag.set('type', 'video/mp4')
            source_tag.text = 'Your browser does not support the video tag.'

        # write the html file for video languages
        lang_html_out_path = os.path.join(sys.argv[2], _edx_consts.COMP_HTML_FOLDER, filename + '.html')
        with open(lang_html_out_path, 'wb') as fout:
            fout.write(etree.tostring(script_tag, pretty_print = True))
            fout.write(etree.tostring(p_languages_tag, pretty_print = True))
            fout.write(etree.tostring(div_tag, pretty_print = True))

        # create the xml file for video languages
        lang_tag = etree.Element("html")
        lang_tag.set('display_name', 'View Video in Other Language')
        lang_tag.set('filename', filename)

        # write the xml file for video languages
        lang_xml_out_path = os.path.join(sys.argv[2], _edx_consts.COMP_HTML_FOLDER, filename + '.xml')
        with open(lang_xml_out_path, 'wb') as fout:
            fout.write(etree.tostring(lang_tag, pretty_print = True))

        # add the file to the return list
        files.append( [filename, _edx_consts.COMP_HTML_FOLDER] )

    # return the file name and folder
    return files
    
#--------------------------------------------------------------------------------------------------
