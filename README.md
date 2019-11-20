# edx-generator

A Python3 script for generating an edx course from markdown.

The aim is:
- to allow all content to be created using a simple text editor outside the browser.
- to allow Git and version control to be used when developing the content.
- to allow better control over formatting and styles.

The basic workflow is that you create all your content locally, in a specific folder structure (described below). When you run the python script, it generates a compressed .tar.gz file that can be directly imported into the edx course. When this file is imported, it will automatically populate all course contents on edx.

For the edx import to succeed, it is vital that settings in the course.xml file match the settings in edx.
`<course org="Org name" course="My Course" url_name="20192020S2"/>`

In the edx UI for the course, under the menu 'Settings > Schedule & Details', these are named as follows:
- Organization
- Course Number
- Course Run

**WARNING: When you upload the .tar.gz file, any existing course contents in edx will be deleted.**

## Dependencies

This script requires two python modules, 'python-markdown' and 'lxml'. These can be installed with pip as follows:

pip install markdown
pip install lxml

Markdown is processes using the python markdown module.
- https://python-markdown.github.io
- pip install markdown

The following extensions are used:
- https://python-markdown.github.io/extensions/extra/
  - https://python-markdown.github.io/extensions/fenced_code_blocks/
  - https://python-markdown.github.io/extensions/tables/
- https://python-markdown.github.io/extensions/meta_data/

extensions = ['extra', 'meta', 'sane_lists']

## Files

In order to create the edx course, the instructors need to organise their files in a specific folder structure that is four levels deep. All other assets, such as images and videos, can be placed in context, in teh same folder as where they are being used.

There are three types of files:

- Settings files (.md)
  - Markdown files
  - Must end in "settings.md", for example "section_settings.md", note the name is all lowercase
  - Contains the settings for the parent folder.
- Component files (.md)
  - Markdown files
  - Can have any name, but the extension must be .md
- Assets (e.g. .jog, .png)
  - The assets should be placed in the same folder where they are used, i.e. with the components.
  - Images can be .png and .jpg

The course content (the text, images, videos, etc) is written as text files using markdown. These files have an .md extension.

The .md files have metadata is important for describing the components. Metadata is defined as key-value pairs at the top of the markdown file. This is used for both settings files and for component files, as described above.

## Structure of Folders and .md files

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

You can explore an example input dataset here:
https://github.com/design-automation/edx-generator/tree/master/test/input

Note that the alphanumeric ordering of the folders is important, as this will reflect the ordering that will be generated in edx. In this example, the sections'Week_1', 'Week_2', etc will be sorted correctly. However, the subsections 'Intro', 'Shorts', and 'Assignment' would not be sorted correctly. So, for that reason, they have been named '01_Intro', '02_Shorts', and '03_Assignment'.

## Execution

Execute the python script in order to generate all the MOOC file and the .tar.gz file using the following command:

~~~~~~~~~~~~~~~~~~~~~
python genedx.py ./in/MOOC1 ./out/MOOC1
~~~~~~~~~~~~~~~~~~~~~

You must supply two arguments to the python script:
- ./in/MOOC1 is the source folder where the script will read from
- ./out/MOOC1 is the destination folder where the script will write to

**WARNING: any existing contents in the output folder (i.e. in this case `./out/MOOC1`) will be deleted.**

## Hierarchical Terminology

In  the edx interface, the hierarchy is as follows:
-  course > section > subsection > unit > component

In the tar file folder structure, the hierarchy is as follows
-  course > chapter > sequence   > vertical > component

In this document, we will use the first, i.e. course > section > subsection > unit > component. This mateches what users see in the user interface. However, the python script will of course generate a .tar.gz file that uses the second. 

See [here](README_MORE.md) for more information.
