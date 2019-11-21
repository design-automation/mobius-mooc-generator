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
                    s3_object_name = component_filename + '.' + component_ext

                    # upload mob files to aws s3
                    if component_ext in __CONSTS__.S3_FILE_EXTENSIONS:

                        # upload an answer to a private repo
                        if component_name.endswith(__CONSTS__.S3_ANSWER_FILENAME):
                            _util.upload_s3_answer(component_path, s3_object_name)

                        # upload an example to a public repo
                        else:
                            _util.upload_s3_example(component_path, s3_object_name)

    print("Finished processing")

#--------------------------------------------------------------------------------------------------
main()
