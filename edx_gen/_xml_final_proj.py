import sys, os
from lxml import etree
from edx_gen import  _edx_consts
from edx_gen import  _process_html
from edx_gen import  _css_settings
from edx_gen import  _mob_iframe
from edx_gen import  _write_comp_util
import __SETTINGS__
#--------------------------------------------------------------------------------------------------
WARNING = "      WARNING:"

FINAL_PROJ_TITLE = 'Submit your Mobius Modeller (version 0.8) script'

FINAL_PROJ_INSTRUCTIONS = "Copy and paste the URL of your published Mobius Modeller script."

FINAL_PROJ_CRITERION_OPTIONS = [
    [
        'Not-Gradable',
        '1',
        'Your Mobius script has major issues and is not gradable. You have not passed your final project. You need to re-submit a new script.'
    ],
    [
        'Very-Weak', 
        '2', 
        'Your Mobius script is very weak. You have not passed your final project. You need to make significant improvements to your script and re-submit.'
    ],
    [
        'Weak',
        '3',
        'Your Mobius script is weak. You have not passed your final project. You need to improve your script and re-submit.'
    ],
    [
        'Below-Average',
        '4',
        'Your Mobius script is below average. You have not passed your final project. You need to make some improvements to your script and re-submit.'
    ],
    [
        'Average',
        '5',
        'The Mobius script is OK. You have passed your final project.'
    ],
    [
        'Above-Average',
        '6', 
        'The Mobius script is above average. You have passed your final project.'
    ], 
    [
        'Good', 
        '7', 
        'The Mobius script is good. Well done. You have passed your final project.'
    ],
    [
        'Very-Good',
        '8',
        'The Mobius script is very good. Very well done! You have passed your final project.'
    ],
    [
        'Excellent', 
        '9',
        'The Mobius script is excellent. Nice work! You have passed your final project.'
    ],
    [
        'Outstanding',
        '10',
        'The Mobius script is outstanding. Impressive! You have passed your final project.'
    ]
]
#--------------------------------------------------------------------------------------------------
# write xml for problem Checkboxescomponent
def tagForFinalProj( filename, settings ):

    # ----  ----  ----
    # <openassessment 
    #   url_name = "xxx" 
    #   submission_start = "2001-01-01T00:00:00+00:00" 
    #   submission_due = "2022-02-28T00:00:00+00:00" 
    #   text_response = "required" 
    #   text_response_editor = "text" 
    #   allow_multiple_files = "True" 
    #   allow_latex = "False" 
    #   prompts_type = "html" 
    #   teams_enabled = "False" 
    #   selected_teamset_id = "" 
    #   show_rubric_during_response = "False" 
    # >
    #   <title > Submit your published Mobius script < /title >
    #   <assessments >
    #     <assessment 
    #       name = "staff-assessment" 
    #       enable_flexible_grading = "False" 
    #       required = "True"/>
    #   </assessments >
    #   <prompts >
    #       <prompt >
    #         <description > This is a test.< /description >
    #       </prompt >
    #   </prompts>
    #   <rubric >
    #  <criterion >
    #     <name > Content < /name >
    #     <label > Content < /label >
    #     <prompt > Assess the content of the submission < /prompt >
    #     <option points = "0" >
    #       <name > Poor < /name >
    #       <label > Poor < /label >
    #       <explanation > The script is ppor. < /explanation >
    #     </option >
    #     <option points = "1" >
    #       <name > Fair < /name >
    #       <label > Fair < /label >
    #       <explanation > The script is fair. < /explanation >
    #     </option >
    #     <option points = "3" >
    #       <name > Good < /name >
    #       <label > Good < /label >
    #       <explanation > The script is good. < /explanation >
    #     </option >
    #     <option points = "5" >
    #       <name > Excellent < /name >
    #       <label > Excellent < /label >
    #       <explanation > The script is excellent. < /explanation >
    #     </option >
    #   </criterion >
    #   </rubric >
    # </openassessment>
    # ----  ----  ----

    #  reate the tags
    openassessment_tag = etree.Element("openassessment")
    title_tag = etree.Element("title")
    assessments_tag = etree.Element("assessments")
    assessment_tag = etree.Element("assessment")
    assessment_prompts_tag = etree.Element("prompts")
    assessment_prompt_tag = etree.Element("prompt")
    assessment_prompt_descr_tag = etree.Element("description")
    rubric_tag = etree.Element("rubric")
    rubric_criterion_tag = etree.Element("criterion")
    rubric_criterion_name_tag = etree.Element("name")
    rubric_criterion_label_tag = etree.Element("label")
    rubric_criterion_prompt_tag = etree.Element("prompt")

    # create the tree
    openassessment_tag.append(title_tag)
    openassessment_tag.append(assessments_tag)
    openassessment_tag.append(assessment_prompts_tag)
    openassessment_tag.append(rubric_tag)
    assessments_tag.append(assessment_tag)
    assessment_prompts_tag.append(assessment_prompt_tag)
    assessment_prompt_tag.append(assessment_prompt_descr_tag)
    rubric_tag.append(rubric_criterion_tag)
    rubric_criterion_tag.append(rubric_criterion_name_tag)
    rubric_criterion_tag.append(rubric_criterion_label_tag)
    rubric_criterion_tag.append(rubric_criterion_prompt_tag)

    # openassessment_tag
    openassessment_tag.set('url_name', filename)

    # process the settings
    for key in settings:
        if key not in ['type', 'id']:
            openassessment_tag.set(key, settings[key])

    # process html
    # _process_html.processHtmlTags(component_path, content, unit_filename)

    # add title
    title_tag.text = FINAL_PROJ_TITLE

    # assesment_tag
    assessment_tag.set("name", "staff-assessment")
    assessment_tag.set("enable_flexible_grading", "False")
    assessment_tag.set("required", "True")

    # assessment_prompt_descr_tag
    assessment_prompt_descr_tag.text = FINAL_PROJ_INSTRUCTIONS

    # rubric_criterion_tag
    rubric_criterion_name_tag.text = 'Content'
    rubric_criterion_label_tag.text = 'Content'
    rubric_criterion_prompt_tag.text = 'Assess the content of the submission'

    # add options to rubric_criterion_tag
    for option in FINAL_PROJ_CRITERION_OPTIONS:
        # create tags
        option_tag = etree.Element("option")
        name_tag = etree.Element("name")
        label_tag = etree.Element("label")
        explanation_tag = etree.Element("explanation")
        # create tree
        rubric_criterion_tag.append(option_tag)
        option_tag.append(name_tag)
        option_tag.append(label_tag)
        option_tag.append(explanation_tag)
        # set text 
        name_tag.text = option[0]
        label_tag.text = option[0]
        option_tag.set("points", option[1])
        explanation_tag.text = option[2]

    # return the tag and type
    return [
        [openassessment_tag, 'final-project']
    ]
#--------------------------------------------------------------------------------------------------
