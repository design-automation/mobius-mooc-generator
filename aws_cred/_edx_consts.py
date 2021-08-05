#--------------------------------------------------------------------------------------------------
# Folders
# Hierarchical Terminology (very confusing)
# In  the edx interface, the names are as follows:
# -  course > section > subsection > unit     > component
# In the tar file folder structure, the names are as follows
# -  course > chapter > sequence   > vertical > component
# For the input data, we will use the first appraoch, since it follows the edx UI
# For the output, we must use the second approach

# Folder names for writing output
COURSE_FOLDER = "course" # Contains chapters (sections)
SECTION_FOLDER = "chapter" # Usually week 1, week 2
SUBSECTION_FOLDER = "sequential" # Usually intro, shorts, assignments
UNIT_FOLDER = "vertical" # Contains units, made of three type of components

# Folder names for writing components
COMP_HTML_FOLDER = "html"
COMP_VIDS_FOLDER = "video"
COMP_PROBS_FOLDER = "problem"

# Folder for all assets
STATIC_FOLDER = "static"

# Folder for policies
POLICIES_FOLDER = "policies"
POLICY_FILENAME = "policy.json"
POLICY_GRADING_FILENAME = "grading_policy.json"
#--------------------------------------------------------------------------------------------------
# Metadata settings for folders

# root
ROOT_FOLDER_REQ = ['org', 'course', 'url_name']
ROOT_FOLDER_OPT = ['visible_to_staff_only', 'start']

# course
COURSE_FOLDER_REQ = ['display_name']
COURSE_FOLDER_OPT = ['visible_to_staff_only', 'enrollment_start', 'start', 'end', 'self_paced', 'is_new',
    'cert_html_view_enabled', 'course_image', 'graceperiod', 'instructor_info', 'invitation_only', 
    'language', 'learning_info', 'minimum_grade_credit', 'wiki_slug', 'cosmetic_display_price']

# section
SECTION_FOLDER_REQ = ['display_name']
SECTION_FOLDER_OPT = ['visible_to_staff_only', 'start']

# subsection
SUBSECTION_FOLDER_REQ = ['display_name']
SUBSECTION_FOLDER_OPT = ['visible_to_staff_only', 'start', 'format', 'graded', 'due', 'hide_after_due']

# unit
UNIT_FOLDER_REQ = ['display_name']
UNIT_FOLDER_OPT = ['visible_to_staff_only', 'start']

#--------------------------------------------------------------------------------------------------
# Metadata settings for components

COMP_HTML_REQ = ['type']
COMP_HTML_OPT = ['display_name', 'visible_to_staff_only', 'start']

COMP_VIDEO_REQ = ['type']
COMP_VIDEO_OPT = ['video_filename', 'display_name', 'visible_to_staff_only', 'start', 'download_video', 
    'show_captions', 'sub', 'youtube_id_1_0']

COMP_PROB_SUBMIT_REQ = ['type', 'answer_filename' ]
COMP_PROB_SUBMIT_OPT = ['example_filename', 'base_filename', 'id', 'verified_only', 'display_name', 'visible_to_staff_only', 'start', 'max_attempts', 'weight', 
    'showanswer', 'attempts_before_showanswer_button']

COMP_PROB_QUIZ_REQ = ['type']
COMP_PROB_QUIZ_OPT = ['display_name', 'visible_to_staff_only', 'id', 'verified_only', 'start', 'max_attempts', 'weight', 
    'showanswer', 'group_access', 'rerandomize', 'attempts_before_showanswer_button']

COMP_DISCUSS_REQ = ['type']
COMP_DISCUSS_OPT = ['verified_only', 'display_name', 'discussion_category', 'discussion_target']

#--------------------------------------------------------------------------------------------------
# Metadata settings for components

METADATA_ENUMS = {

    'visible_to_staff_only': ['true', 'false'],

    # settings files

    'hide_after_due': ['true', 'false'],

    'graded': ['true', 'false'],

    'invitation_only': ['true', 'false'],

    'cert_html_view_enabled': ['true', 'false'],

    # component files

    'download_video': ['true', 'false'],

    'show_reset': ['true', 'false'],

    'show_captions': ['true', 'false'],

    'showanswer': ["always", "answered", "attempted", "closed", "finished", "correct_or_past_due", 
        "past_due", "never", "after_attempts"],

    'rerandomize': ["always", "onreset", "never", "per_student"],

    'type': ['html', 'video', 'problem-submit', 'problem-checkboxes', 'problem-multiplechoice', 'discussion']

    # more types: ['problem-choice', 'problem-dropdown', 'problem-numerical', 'problem-text']

}
#--------------------------------------------------------------------------------------------------
MD_SNIPPET_MARKERS = [
    '# ROOT', '# MOOC', '# COURSE', '# SECTION', '# SUBSECTION', 
    '# UNIT', '# COMPONENT'] 
    # , '# HTML', '# VIDEO', '# PROBLEM-SUBMIT', '# PROBLEM-CHECKBOX']
#--------------------------------------------------------------------------------------------------
