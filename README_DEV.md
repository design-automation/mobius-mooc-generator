# Creating Content For the Edx Generator

In order to create the edx course, the instructors need to organise their files in a specific folder structure that is four levels deep. All other assets, such as images and videos, can be placed in context, in the same folder as where they are being used.

The content is defined using markdown files with an .md extension. Here is a [markdown cheatsheet](https://devhints.io/markdown) that gives a quick overview of the things you can do.

There are two types of files:

- Settings and content files (.md)
  - Markdown files
  - Contains the settings for the parent folder.
  - Contains the content for the components that make up the units.
- Assets (e.g. .jog, .png)
  - Images can be .png and .jpg
  - The assets should be placed in the same folder where they are used, i.e. in the unit folder.

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
- https://github.com/design-automation/edx-generator/tree/master/test/input

Note that the alphanumeric ordering of the folders is important, as this will reflect the ordering that will be generated in edx. In this example, the sections'_w1' (for 'week 1'), '_w2' (for 'week 2'), etc will be sorted correctly. However, the subsections 'Intro', 'Shorts', and 'Assignment' would not be sorted correctly. So, for that reason, they have been named '01_Intro', '02_Shorts', and '03_Assignment'.

In the example, short folder names used. This is because when the final files get generated, the files names will concatenate all the folder names. So in order to avoid long file names in the final output, it is advisable to keep the folder names short. In addition, in the example, we start the filename with an '_' (underscore). This is to ensure that the markdown file will always be listed at the top of the file list. (But this is just a convenience, not a requirement.)

## Root .md file

For the edx import to succeed, it is vital that settings in the root .md file (which is the .md file in the root folder) match the settings in edx.
~~~~~~~~~~~~~
EDX_ORG = 'my_org' 
S3_MOOC_FOLDER = 'my_course_number' 
EDX_URL_NAME = 'my_url_run'
~~~~~~~~~~~~~

In the edx UI for the course, under the menu 'Settings > Schedule & Details', these are named as follows:
- EDX_ORG = Organization
- S3_MOOC_FOLDER = Course Number
- EDX_URL_NAME = Course Run

## Hierarchical Terminology

In  the edx interface, the hierarchy is as follows:
-  course > section > subsection > unit > component

In the tar file folder structure, the hierarchy is as follows
-  course > chapter > sequence   > vertical > component

In this document, we will use the first, i.e. course > section > subsection > unit > component. This matches what users see in the user interface. However, the python script will generate a .tar.gz file that uses the second. 

Sections are usually named as 'Week 1'. 'Week 2', etc.

# Writing .md Files

For more information on writing the .md files, follow the links below.

* See [Structure](markdown_structure.md) for more information on the overall structure of the .md files.
* See [Settings for Folders](markdown_settings_folders.md) and [Settings for Components](markdown_settings_components.md) for more information on the settings that can be specified in each type of .md file.
