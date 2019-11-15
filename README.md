# edx-generator

A Python3 script for generating an edx course from markdown.

The aim is:
- to allow all content to be created using a simple text editor outside the browser.
- to allow Git and version control to be used when developing the content.
- to allow better control over formatting and styles.

The script generates a compressed .tar.gz file that can be directly imported into the edx course. When this file is imported, it will automatically populate all course contents.

For the edx import to succeed, it is vital that settings in the course.xml file match the settings in edx.
`<course org="Org name" course="My Course" url_name="20192020S2"/>`

In the edx UI for the course, under the menu 'Settings > Schedule & Details', these are named as follows:
- Organization
- Course Number
- Course Run

Warning: any existing course contents in edx will be deleted.

## Python Dependencies

This script requires two python modules, 'python-markdown' and 'lxml'. These can be installed with pip as follows:

pip install markdown
pip install lxml

## Hierarchical Terminology

In  the edx interface, the hierarchy is as follows:
-  course > section > subsection > unit > component

In the tar file folder structure, the hierarchy is as follows
-  course > chapter > sequence   > vertical > component

In this document, we will use the first, i.e. course > section > subsection > unit > component. This mateches what users see in the user interface. However, the python script will of course generate a .tar.gz file that uses the second. 

## Structure of Folders and .md files

In order to create the edx course, the instructors need to create a set of markdown files (.md files), and save them in a specific folder structure that is four levels deep.

The folder strcture is as follows:

- Course_Folder (_1st level_)
  - course_settings.md
  - Section_Folder (_2nd level_)
    - section_settings.md
    - Subsection_Folder (_3rd level_)
      - subsection_settings.md
      - Unit_Folder (_4th level_)
        - unit_settings.md
        - component_file.md

## Example

Here is an example of what a folder structure might look like. It should match the structure that the users see in the edx user interface.

- My_MOOC (_course, 1st level_)
  - course_settings.md
  - Week_1 (_section, 2nd level_)
    - section_settings.md
    - 01_Intro (_subsection, 3rd level_)
      - subsection_settings.md
      - Intro_Text(_unit, 3rd level_)
        - unit_settings.md
        - comp1.md
        - image1.jpg
      - Intro_Video (_unit, 3rd level_)
        - unit_settings.md
        - comp1.md
    - 02_Shorts (_subsection, 3rd level_)
      - subsection_settings.md
      - Concept_1 (_unit, 3rd level_)
        - unit_settings.md
        - comp1.md
        - comp2.md
        - image1.jpg
      - Concept_2 (_unit, 3rd level_)
        - unitsettings.md
        - comp1.md
      - Concept_3 (_unit, 3rd level_)
        - unit_settings.md
        - comp1.md
        - image1.jpg
    - 03_Assignment (_subsection, 3rd level_)
      - subsection_settings.md
      - Quiz (_unit, 3rd level_)
        - unit_settings.md
        - comp1.md
        - comp2.md
        - comp3.md
        - image1.jpg
  - Week_2 (_section, 2nd level_)
    - section_settings.md
    - etc, etc, etc
    
Note that the alphanumeric ordering of the folders is important, as this will reflect the ordering that will be generated in edx. In this example, the sections'Week_1', 'Week_2', etc will be sorted correctly. However, the subsections 'Intro', 'Shorts', and 'Assignment' would not be sorted correctly. So, for that reason, they have been named '01_Intro', '02_Shorts', and '03_Assignment'.
    
# Files

There are three types of files:

- Settings files
  - Must be end in "settings.md", for example "section_settings.md", note the name is all lowercase
  - Contains the settings for the parent folder.
- Component files, the actual contents
  - Can have any name.
  - Extension must be either .md or .html
  - If it is .md, an html file will be generated by processing the markdown (see section below on Markdown).
  - If it is .html, then the file will be used as is, without conversion.
    - The html will be assumed to include the correct html snippets.
    - This is a fallback, just in case there is something that cannot be achieved by using markdown.
- Assets, such as images
  - Can have any name.
  - The assets should be in the same folder where they are used, i.e. with the components.
  - Images can be .png and .jpg
    
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

## Component file, component.md

The component file defines one component.

At the top of the component file are a set of key-value pairs. These define settings for this component.

The 'type' defines the component type.
- type: text
- type: video
- type: problem-submit
- type: problem-checkboxes
- type: problem-choice (not supported at this time)
- type: problem-dropdown (not supported at this time)
- type: problem-numerical (not supported at this time)
- type: problem-text (not supported at this time)

At the moment, only 'problem-submit' and 'problem-checkboxes' are implemented.
- problem-submit: A problem where the student needs to submit a file that will be uploade to the edx server and graded with an external grader. 
- problem-checkboxes: A problem where the student needs to answer a checkboxes question (with multiple right answers).  Feedback

In both cases, after answering the question, the student can get feeback on the right answer.

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

## Markdown

Markdown is processes using the python markdown module.
- https://python-markdown.github.io
- pip install markdown

The following extensions are used:
- https://python-markdown.github.io/extensions/extra/
  - https://python-markdown.github.io/extensions/fenced_code_blocks/
  - https://python-markdown.github.io/extensions/tables/
- https://python-markdown.github.io/extensions/meta_data/

extensions = ['extra', 'meta', 'sane_lists']

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

For checkboxes, the correct and incorrect choices are specified by starting with '[ ]' or '[x]'

~~~~~~~~~~~~~~~~~~~~~
This text describes the problem.

===

[x] This is a correct choice.
[ ] This is an incorrect choice.

===

This text describes the solution.
~~~~~~~~~~~~~~~~~~~~~

For both the problem and slution, you can use any kind of markdown formatting, and insert images.

### Code Blocks

Using the extension defined above, you can display code as follows:

~~~~~~~~~~~~~~~~~~~~~{.python hl_lines="3"}
# Here is how to draw a line
pos1 = make.Position([1,2,3])
pos2 = make.Position([1,2,3])
line = make.Polyline([pos1, pos2])
~~~~~~~~~~~~~~~~~~~~~

### Tables

Using the extension defined above, you can generate tables as follows:

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

### Metadata

The metadata is important for describing the components. 

Metadata is defined as key-value pairs at the top of the markdown file.

This is used for both settings files and for component files, as described above.

# Execution

Generate all the MOOC file and the .tar.gz file using the following command:

~~~~~~~~~~~~~~~~~~~~~
python genedx.py ./in/MOOC1 ./out/MOOC1
~~~~~~~~~~~~~~~~~~~~~

You must supply two arguments to the python script:
- ./in/MOOC1 is the source folder where the script will read from
- ./out/MOOC1 is the destination folder where the script will write to

Warning: everything in the output folder will be deleted.

