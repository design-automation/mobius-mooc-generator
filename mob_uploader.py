import sys, os
#--------------------------------------------------------------------------------------------------
if len(sys.argv) != 2:
    raise Exception('Usage: python ./mob_uploader.py input_path')
if not os.path.exists(sys.argv[1]):
    raise Exception('Path does not exist: ' + sys.argv[1])
if not os.path.exists(os.path.join(sys.argv[1], '__SETTINGS__.py')):
    raise Exception('Path does not contain __SETTINGS__.py: ' + sys.argv[1])
sys.path.append(sys.argv[1])
#--------------------------------------------------------------------------------------------------
from edx_gen import  _util
import __SETTINGS__
#--------------------------------------------------------------------------------------------------
# Text strings
WARNING = "      WARNING:"
#--------------------------------------------------------------------------------------------------
# process one course
def main():

    print("Start processing")

    # get the main mooc input folder, which we assume is the first folder
    root_folder = os.path.normpath(sys.argv[1])
    course_path = os.path.join(root_folder, 'Course')

    # loop
    for [section, section_path] in _util.getSubFolders(course_path):
        print("- section", section)
        section_filename = section.lower()

        for [subsection, subsection_path] in _util.getSubFolders(section_path):
            print("-- subsection", subsection)
            subsection_filename = section_filename + '_' + subsection.lower()

            for [unit, unit_path] in _util.getSubFolders(subsection_path):
                print("--- unit", unit)
                unit_filename = subsection_filename + '_' + unit.lower()

                for [component, component_path] in _util.getFiles(unit_path):
                    [component_name, component_ext] = component.split('.')
                    component_filename = unit_filename + '_' + component_name

                    # create the filename on s3
                    # this matches the url created in _mob_iframe.py
                    mob_filename = component_filename + '.' + component_ext
                    
                    # upload an answer to a private repo
                    if mob_filename.endswith(__SETTINGS__.MOB_ANSWER_FILENAME):
                        _util.upload_s3_answer(component_path, mob_filename)

                    # upload an example to a public repo
                    elif mob_filename.endswith(__SETTINGS__.MOB_EXAMPLE_FILENAME):
                        _util.upload_s3_example(component_path, mob_filename)

                    # ignore files with wrong extension
                    else:
                        pass

    print("Finished processing")

#--------------------------------------------------------------------------------------------------
main()
