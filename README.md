# Möbius MOOC Generator

A Python3 script for generating an edx course from markdown.

The aim is:
- to allow all content to be created using a simple text editor outside the browser.
- to allow Git and version control to be used when developing the content.
- to allow better control over formatting and styles.

The basic workflow is that you create all your content locally, in a specific folder structure (described below). When you run the python script, it generates a compressed .tar.gz file that can be directly imported into the edx course. When this file is imported, it will automatically populate all course contents on edx.

## More Information

For more information about creating the content for the Edx Generator:
* [Creating content for the Möbius MOOC Generator](./README_DEV.md)

For more information about running the Edx Generator:
* [Running the Möbius MOOC Generator](./README_RUN.md)
