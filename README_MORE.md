
# Metedata for Settings Files

Below is a list of the metadata for settinsg files.
    
## Settings file, settings.md

The settings file contains the settings for each folder. 

Setting are define as a set of key-value pairs.

### Common Metadata For Settings Files in Folders

Common setting for all settings files in folders are as follows:
- display_name: string (if missing, the folder name will be used)
- visible_to_staff_only: "true"
- start: "&quot;2019-08-18T10:00:00+00:00&quot;"

The display_name is the name that will be displayed to the user in the edx interface.

### Root Folder Metadata

Additional MOOC metadata is as follows:

Required
- url_name: "1234" 
- org: "abc" 
- course: "online101"

The values must match the values on edx. If they do not match, import of the data into edx will fail.

### Course Folder Metadata

Additional course metadata is as follows:

Required
- wiki_slug: "xxx"

Optional
- cert_html_view_enabled: "true"
- course_image: "course_image.jpg"
- graceperiod: "900 seconds"
- instructor_info: "[Luke Skywalker, Han Solo]"
- invitation_only: "true"
- language: "en"
- learning_info: "[]"
- minimum_grade_credit: "0.8"

### Section Folder Metadata

Additional section metadata is as follows:

NIL

### Subsection Folder Metadata

Additional subsection metadata is as follows:

Optional
- format: "Assignment" 
- graded: "true"
- due: "2019-08-25T10:00:00+00:00" 
- hide_after_due: "true" 

### Unit Folder Metadata

NIL





# Metedata for Component Files

Below is a list of the metadata for component files.

## Component file, component.md

The component file defines one component.

The metedata defines the settings for this component. One important piece of metadata is called 'type', which defines the type of component being defined.

Possible values of 'type' are as follows:
- type: text
- type: video
- type: problem-submit
- type: problem-checkboxes
- type: problem-choice (not supported at this time)
- type: problem-dropdown (not supported at this time)
- type: problem-numerical (not supported at this time)
- type: problem-text (not supported at this time)

At the moment, for problems, only 'problem-submit' and 'problem-checkboxes' are implemented.
- problem-submit: A problem where the learner needs to submit a file that will be uploade to the edx server and graded with an external grader. 
- problem-checkboxes: A problem where the learner needs to answer a checkboxes question (with multiple right answers).  Feedback

In both cases, after answering the question, the learner can get feeback on the right answer.

### Common Metadata For Component Files

Common setting for all settings files are as follows:

Optional
- display_name: string
- visible_to_staff_only: "true"
- start: "&quot;2019-08-18T10:00:00+00:00&quot;"

The display_name is not displayed to the user in the edx interface.

### Text Metadata

Additional text metadata is as follows:

NIL

### Video Metadata

Additional video metadata is as follows:

Required


Optional
- download_video: "false" 
- youtube_id_1_0: "3_yD_cEKoCk"
- html5_sources: [] 
- ... and many more

### Problem Metadata - Submit

Additional submit problem metadata is as follows:

Required
- question: "question_name"
- queuename: "name_of_queue_on_edx_server"

Optional
- max_attempts: "2" 
- weight: "1.0"
- showanswer: "finished" 

For the content of the submit problem, the markdown should be defined as follows: ... to be completed

### Problem Metadata - Checkboxes

Additional checkboxes  problem metadata is as follows:

Optional
- max_attempts: "2" 
- weight: "1.0"
- showanswer: "finished" 
- group_access: "{}"
- rerandomize: "always" or "never"
- attempts_before_showanswer_button: "1"

For the content of the checkboxes problem, the markdown should be defined as follows: ... to be completed





# Describing Problems

edx allow for the definition of different types of problems.

The markdown for describing problems have some spcific rules.

### Submit Problems

For submit problems, the '===' string is used to split the text into two parts.

Above the '===' describes the problem. 
Below the '===' described the solution.

~~~~~~~~~~~~~~~~~~~~~
This text describes the problem.

===

This text describes the solution.
~~~~~~~~~~~~~~~~~~~~~

For both the problem and slution, you can use any kind of markdown formatting, and insert images.

### Checkboxes Problems

For checkboxes problems, the '===' string is used to split the text into three parts. 
(i.e. The '===' needs to be inserted two times.)

Above the first '===' describes the problem. 
Between the two '===' describes the checkbox choices.
Below the second '===' described the solution.

For checkboxes choices, the correct and incorrect choices are specified by starting with '[ ]' or '[x]'
Each choice must be seperated by an empty line.

~~~~~~~~~~~~~~~~~~~~~
This text describes the problem.

===

[x] This is a correct choice.

[ ] This is an incorrect choice.

===

This text describes the solution.
~~~~~~~~~~~~~~~~~~~~~

For both the problem and slution, you can use any kind of markdown formatting, and insert images.





