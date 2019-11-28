import os
import __CONSTS__ 
import _util

#--------------------------------------------------------------------------------------------------
# Text strings
WARNING = "      WARNING:"

#--------------------------------------------------------------------------------------------------
# process one course
def main():

    print("Start processing")

    # get the main mooc input folder, which we assume is the first folder
    courses = _util.getSubFolders(__CONSTS__.COURSE_PATH)
    if (len(courses) != 1):
        print(WARNING, 'There should only be one folder in the root folder.')
        return

    # select the first subfolder
    course_path = courses[0][1]

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
                    [component_name, component_ext] = component.lower().split('.')
                    component_filename = unit_filename + '_' + component_name

                    # create the filename on s3
                    # this matches teh url created in _mob_iframe.py
                    s3_filename = __CONSTS__.EDX_COURSE + '/' + component_filename + '.' + component_ext
                    
                    # upload an answer to a private repo
                    if s3_filename.endswith(__CONSTS__.MOB_ANSWER_FILENAME):
                        _util.upload_s3_answer(component_path, s3_filename)

                    # upload an example to a public repo
                    elif s3_filename.endswith(__CONSTS__.MOB_EXAMPLE_FILENAME):
                        _util.upload_s3_example(component_path, s3_filename)

                    # ignore files with wrong extension
                    else:
                        pass

    print("Finished processing")

#--------------------------------------------------------------------------------------------------
main()
