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

The content is defined using markdown files with an .md extension. Here is a [markdown cheatsheet](https://devhints.io/markdown) that gives a quick overview of the things you can do.

There are three types of files:

- Settings files (.md)
  - Markdown files
  - Contains the settings for the parent folder.
- Unit files (.md)
  - Markdown files
  - Contain all the components for one unit.
- Assets (e.g. .jog, .png)
  - Images can be .png and .jpg
  - The assets should be placed in the same folder where they are used, i.e. in the unit folder.

The course content (the text, images, videos, etc) is written as text files using markdown. These files have an .md extension.

## Structure of Folders and .md files

The folder strcture is as follows:

- Course_Folder (_1st level_)
  - course_settings.md
  - Section_Folder (_2nd level_)
    - section_settings.md
    - Subsection_Folder (_3rd level_)
      - subsection_settings.md
      - Unit_Folder (_4th level_)
        - unit_settings_and_components.md

Note that each folder should contaon exactly one markdown (.md) file. These files can have any name, but must always have a '.md' extension.

You can explore an example input dataset here:
https://github.com/design-automation/edx-generator/tree/master/test/input

Note that the alphanumeric ordering of the folders is important, as this will reflect the ordering that will be generated in edx. In this example, the sections'_w1' (for 'week 1'), '_w2' (for 'week 2'), etc will be sorted correctly. However, the subsections 'Intro', 'Shorts', and 'Assignment' would not be sorted correctly. So, for that reason, they have been named '01_Intro', '02_Shorts', and '03_Assignment'.

In the example, short folder names used. This is because when the final files get generated, the files names will concatenate all the folder names. So in order to avoid long file names in the final output, it is advisable to keep the folder names short. In addition, in the example, we start the filename with an '_' (underscore). This is to ensure that the markdown file will always be listed at the top of the file list. (But this is just a convenience, not a requirement.)

## Execution

Execute the python script in order to generate all the MOOC file and the .tar.gz file using the following command:

~~~~~~~~~~~~~~~~~~~~~
python genedx.py
~~~~~~~~~~~~~~~~~~~~~

The `__CONSTS__.py` file specifies a set of global that you can set for your context. 

Two important global constants:
- ./in/MOOC1 is the source folder where the script will read from
- ./out/MOOC1 is the destination folder where the script will write to

**WARNING: any existing contents in the output folder (i.e. in this case `./out/MOOC1`) will be deleted.**

## Hierarchical Terminology

In  the edx interface, the hierarchy is as follows:
-  course > section > subsection > unit > component

In the tar file folder structure, the hierarchy is as follows
-  course > chapter > sequence   > vertical > component

In this document, we will use the first, i.e. course > section > subsection > unit > component. This mateches what users see in the user interface. However, the python script will generate a .tar.gz file that uses the second. 

Sections are usually named as 'Week 1'. 'Week 2', etc.

# Writing .md Files

For more information on writing the .md files, follow the links below.

* See [Structure](markdown_structure.md) for more information on how to write the .md files.
* See [Settings for Folders](markdown_settings_folders.md) and [Settings for Components](markdown_settings_components.md) for more information on the settings that can be specified in each type of .md file.
