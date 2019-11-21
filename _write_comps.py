import os
from lxml import etree
import __CONSTS__ 
import _edx_consts
import _process_html
import _css_settings
#--------------------------------------------------------------------------------------------------
WARNING = "      WARNING:"
INSTRUCTIONS_CHECKBOXES = 'Please select all applicable options from the list below. Multiple selections are allowed. '
#--------------------------------------------------------------------------------------------------
# write xml for Html component
def writeXmlForHtmlComp(component_path, filename, content, settings, unit_filename):
    # ---- Html file ----
    # <p>
    #   <span style="text-decoration: underline;">Objective:</span>
    # </p>
    # <p>
    #   This week's assignment is broken down into <strong>three file submissions</strong>. 
    #   These smaller submissions are meant to help you along the way.
    # </p>
    # <p>
    #   <img height="288" width="498" src="/static/assignment.png" alt="" 
    #   style="display: block; margin-left: auto; margin-right: auto;" />
    # </p>
    # ----  ----  ----
    # ---- XML file ----
    # <html 
    #   filename="1c870c63861749dbb45ea16ace9fbe24" 
    #   display_name="Task" 
    #   editor="visual"
    # />
    # ----  ----  ----

    # read content
    content_root_tag = etree.fromstring(content)

    # process hrefs
    a_elems = list(content_root_tag.iter('a'))
    _process_html.setHrefHtml(component_path, a_elems, unit_filename)

    # process images
    img_elems = list(content_root_tag.iter('img'))
    _process_html.setImageHtml(img_elems, unit_filename)

    # write the html file
    html_out_path = os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.COMP_HTML_FOLDER, filename + '.html')
    with open(html_out_path, 'wb') as fout:
        for tag in content_root_tag:
            tag_result = etree.tostring(tag, pretty_print = True)
            fout.write(tag_result)

    # create xml
    html_tag = etree.Element("html")
    for key in settings:
        if key not in ['type']:
            html_tag.set(key, settings[key])
    html_tag.set('filename', filename)
    result = etree.tostring(html_tag, pretty_print = True)

    # write the xml file
    xml_out_path = os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.COMP_HTML_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)

#--------------------------------------------------------------------------------------------------
# write xml for problem Checkboxescomponent
def writeXmlForProbCheckboxesComp(component_path, filename, content, settings, unit_filename):
    # ----  ----  ----
    # <problem 
    #   display_name="Q2" 
    #   max_attempts="2" 
    #   rerandomize="always" 
    #   weight="1.0"
    # >
    #   <choiceresponse>
    #       <label>xxx, which of the following are true?</label>
    #       <description>Please select all applicable options from the list below. Multiple selections are allowed. </description>
    #       <checkboxgroup>
    #           <choice correct="false">Some text. </choice>
    #           <choice correct="false">Some text. </choice>
    #           <choice correct="true">Some text. </choice>
    #       </checkboxgroup>
    #       <solution>
    #           <div class="detailed-solution">
    #               <p>Explanation</p>
    #               <p>xxx</p>
    #           </div>
    #       </solution>
    #   </choiceresponse>
    # </problem>
    # ----  ----  ----

    # make the xml
    problem_tag = etree.Element("problem") 
    choiceresponse_tag = etree.Element("choiceresponse")
    problem_tag.append( choiceresponse_tag )

    # process the settings
    for key in settings:
        if key not in ['type']:
            problem_tag.set(key, settings[key])

    # process the html
    content_root_tag = etree.fromstring(content)

    # process hrefs
    a_elems = list(content_root_tag.iter('a'))
    _process_html.setHrefHtml(component_path, a_elems, unit_filename)

    # process images
    img_elems = list(content_root_tag.iter('img'))
    _process_html.setImageHtml(img_elems, unit_filename)

    # process the elements
    # these will be converted to <label>, and solution <p> elements
    # the elements are split using '===', there should be two splits
    labels = []
    choices = []
    solutions = []
    found_splitter = 0 # found ===
    elems = content_root_tag.getchildren()
    if elems:
        for elem in elems:
            if (elem.text and elem.text.startswith('===')):
                found_splitter += 1
            else:
                if found_splitter == 0:
                    labels.append(elem)
                elif found_splitter == 1:
                    if elem.text[:3] in ['[ ]', '[x]']:
                        correct_val = 'true'
                        if elem.text[:3] == '[ ]':
                            correct_val = 'false'
                        choice_tag = etree.Element("choice")
                        choice_tag.text = elem.text[3:]
                        choice_tag.set('correct', correct_val)
                        choices.append(choice_tag)
                    else:
                        print(WARNING, 'Submit problem choice must start with [ ] or [x].', filename)
                else:
                    solutions.append(elem)
    else:
        print(WARNING, 'Submit problem is missing content.', filename)

    # add the choices and solutions to the choiceresponse_tag
    if labels:
        label_tag = etree.Element("label") 
        choiceresponse_tag.append(label_tag)
        for label in labels:
            label_tag.append(label)
    else:
        print(WARNING, 'Choice problem seems to have no text that describes the question.', filename)
    if INSTRUCTIONS_CHECKBOXES:
        description_tag = etree.Element("description")
        choiceresponse_tag.append(description_tag)
        description_tag.text = INSTRUCTIONS_CHECKBOXES
    if choices:
        checkboxgroup_tag = etree.Element("checkboxgroup")
        choiceresponse_tag.append(checkboxgroup_tag)
        for choice in choices:
            checkboxgroup_tag.append(choice)
    else:
        print(WARNING, 'Choice problem seems to have no choices.', filename)
    if solutions:
        solution_tag = etree.Element("solution")
        div_tag = etree.Element("div")
        div_tag.set('class', 'detailed-solution')
        choiceresponse_tag.append(solution_tag)
        solution_tag.append(div_tag)
        for solution in solutions:
            div_tag.append(solution)
    else:
        pass # It is ok to have no solution text

    # convert problem_tag to string
    result = etree.tostring(problem_tag, pretty_print=True)

    # write the file
    xml_out_path = os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.COMP_PROBS_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)

#--------------------------------------------------------------------------------------------------
# write xml for problem submit
def writeXmlForSubmitComp(component_path, filename, content, settings, unit_filename):
    # ----  ----  ----
    # <problem 
    #       attempts_before_showanswer_button="1" 
    #       display_name="Task 1: Submission" 
    #       markdown="null" 
    #       max_attempts="1" 
    #       showanswer="finished" 
    #       weight="1.0">
    #   <coderesponse queuename="mooc_queue_name_on_edx_server">
    #       <label>Submit your Mobius Modeller file here.</label>
    #       <filesubmission/>
    #       <codeparam>
    #           <grader_payload>
    #               {"question": "SCT_W5_Assignment"}
    #           </grader_payload>
    #       </codeparam>
    #       <solution>
    #           <iframe src="https://mobius.design-automation.net/gallery" style="width: 100%; height: 600px; border: 1px solid black;">Your Browser does not support iFrame</iframe>
    #       </solution>
    #   </coderesponse>
    # </problem>
    # ----  ----  ----

    # make the xml
    from lxml import etree
    problem_tag = etree.Element("problem") 
    coderesponse_tag = etree.Element("coderesponse")
    problem_tag.append( coderesponse_tag )

    # process the settings
    for key in settings:
        if key not in ['type', 'question', 'queuename', 'answer']:
            problem_tag.set(key, settings[key])
    queuename = 'Dummy_Queuename'
    if 'queuename' in settings:
        queuename = settings.get('queuename')
    else:
        print(WARNING, 'Submit problem is missing metadata: queuename.', filename)
    coderesponse_tag.set('queuename', queuename)
    question = 'Dummy_Question'
    if 'question' in settings:
        question = settings.get('question')
    else:
        print(WARNING, 'Submit problem is missing metadata: question.', filename)
    grader_payload_tag = etree.Element("grader_payload")
    grader_payload_tag.text = '{"question": "' + question + '"}'

    # read content
    content_root_tag = etree.fromstring(content)

    # process hrefs
    a_elems = list(content_root_tag.iter('a'))
    _process_html.setHrefHtml(component_path, a_elems, unit_filename)

    # process images
    img_elems = list(content_root_tag.iter('img'))
    _process_html.setImageHtml(img_elems, unit_filename)

    # process the elements
    # these will be converted to <label>, and solution <p> elements
    # the elements are spli using '==='
    # everything before the split is added to <label>
    # everything after the split is added to 
    labels = []
    solutions = []
    found_splitter = 0 # found ===
    elems = content_root_tag.getchildren()
    if elems:
        for elem in elems:
            if (elem.text and elem.text.startswith('===')):
                found_splitter += 1
            else:
                if found_splitter == 0:
                    labels.append(elem)
                else:
                    solutions.append(elem)
    else:
        print(WARNING, 'Submit problem is missing content.', filename)

    # add labels to the coderesponse_tag
    if labels:
        label_tag = etree.Element("label") 
        coderesponse_tag.append(label_tag)
        for label in labels:
            label_tag.append(label)
    else:
        print(WARNING, 'Submit problem is missing a description of the problem.', filename)

    # add <filesubmission> and <codeparam> to the coderesponse_tag
    coderesponse_tag.append(etree.Element("filesubmission") )
    codeparam_tag = etree.Element("codeparam")
    codeparam_tag.append(grader_payload_tag)
    coderesponse_tag.append(codeparam_tag)

    # add <solution> to the coderesponse_tag
    if solutions:
        solution_tag = etree.Element("solution")
        coderesponse_tag.append(solution_tag)
        for solution in solutions:
            solution_tag.append(solution)
    else:
        print(WARNING, 'Submit problem is missing a description of the solution.', filename)

    # convert problem_tag to string
    result = etree.tostring(problem_tag, pretty_print=True)

    # write the file
    xml_out_path = os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.COMP_PROBS_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)

#--------------------------------------------------------------------------------------------------
# write xml for video component
def writeXmlForVidComp(filename, content, settings, unit_filename):
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
        if key not in ['type', 'transcript', 'title', 'voice']:
            video_tag.set(key, settings[key])

    # add youtube
    if 'youtube_id_1_0' in settings:
        video_tag.set('youtube', '1.00:' + settings['youtube_id_1_0'])
    else:
        video_tag.set('youtube_id_1_0', '')

    # set the transcript object
    transcripts_obj = {}
    for lang in __CONSTS__.LANGUAGES:
        transcripts_obj[lang] = filename + '_sub_' + lang + '.srt'

    # escape this dict so that we get &quot; but do not escale the &
    video_tag_transcripts_list = []
    for k in transcripts_obj:
        video_tag_transcripts_list.append( '"' + k + '":"' + transcripts_obj[k] + '"' )
    video_tag.set('transcripts', '{' + ','.join(video_tag_transcripts_list) + '}')

    # add the source tag
    html5_sources_list = []
    if 'html5_sources' in settings:
        html5_sources_list = eval(bytes(settings['html5_sources'], "utf-8").decode("unicode_escape"))
        source_tag = etree.Element("source")
        source_tag.set('src', html5_sources_list[0])
        video_tag.append(source_tag)

    # add the video asset tag
    video_asset_tag = etree.Element("video_asset")
    video_asset_tag.set('client_video_id', 'external video')
    video_asset_tag.set('duration', '0.0')
    video_asset_tag.set('image', '')
    video_tag.append(video_asset_tag)
    transcripts_tag = etree.Element('transcripts')
    for lang in __CONSTS__.LANGUAGES:
        transcript_tag = etree.Element('transcript')
        transcript_tag.set('file_format', 'srt')
        transcript_tag.set('language_code', lang)
        transcript_tag.set('provider', 'Custom')
        transcripts_tag.append(transcript_tag)
    video_asset_tag.append(transcripts_tag)

    # add the transcript tags
    for lang in __CONSTS__.LANGUAGES:
        transcript2_tag = etree.Element('transcript')
        transcript2_tag.set('language', lang)
        transcript2_tag.set('src', transcripts_obj[lang])
        video_tag.append(transcript2_tag)

    # write the file
    result = etree.tostring(video_tag, pretty_print = True)
    xml_out_path = os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.COMP_VIDS_FOLDER, filename + '.xml')
    with open(xml_out_path, 'wb') as fout:
        fout.write(result)

    # generate the language options
    if 'html5_sources' in settings and len(__CONSTS__.LANGUAGES) > 1:

        # create the html file for video languages

        # create script str
        script_str = '\nfunction selLang(lang) {\n'
        for lang in __CONSTS__.LANGUAGES[1:]:
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
        for lang in __CONSTS__.LANGUAGES[1:]:

            # p with row of buttons
            if lang != 'en':
                button_tag = etree.Element("div")
                button_tag.set('style', _css_settings.LANG_BUTTON_CSS)
                button_tag.set('onclick', 'selLang("' + lang + '")')
                button_tag.text = __CONSTS__.ALL_LANGUAGES[lang]
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
            source_tag.set('src', html5_sources_list[0][:-4] + '_' + lang + html5_sources_list[0][-4:])
            source_tag.set('type', 'video/mp4')
            source_tag.text = 'Your browser does not support the video tag.'

        # write the html file for video languages
        xml_out_path = os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.COMP_HTML_FOLDER, filename + '.html')
        with open(xml_out_path, 'wb') as fout:
            fout.write(etree.tostring(script_tag, pretty_print = True))
            fout.write(etree.tostring(p_languages_tag, pretty_print = True))
            fout.write(etree.tostring(div_tag, pretty_print = True))

        # create the xml file for video languages
        html_tag = etree.Element("html")
        html_tag.set('display_name', 'View Video in Other Language')
        html_tag.set('filename', filename)

        # write the xml file for video languages
        xml_out_path = os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.COMP_HTML_FOLDER, filename + '.xml')
        with open(xml_out_path, 'wb') as fout:
            fout.write(etree.tostring(html_tag, pretty_print = True))

#--------------------------------------------------------------------------------------------------
# this is just in case there are some html files
# write to units to the correct folder
# returns void
def processRawHtmlComp(component_path, filename):

    with open(component_path, 'r') as f_read:
        contents = f_read.read()
        xml_path = ''

        if (contents.startswith('<html')):
            xml_path = os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.COMP_HTML_FOLDER, filename + '.xml')

        elif (contents.startswith('<problem')):
            xml_path = os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.COMP_PROBS_FOLDER, filename + '.xml')

        elif (contents.startswith('<video')):
            xml_path = os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.COMP_VIDS_FOLDER, filename + '.xml')
            
        # write the content
        with open(xml_path, 'w') as f:
            f.write(contents)