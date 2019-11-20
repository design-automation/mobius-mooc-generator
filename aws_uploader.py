import os
from __CONSTS__ import COURSE_PATH, S3_ANSWERS_BUCKET, S3_EXAMPLES_BUCKET, S3_ANSWER_FILENAME, S3_FILE_EXTENSIONS
from __AWS__ import  S3_bucket
from _to_S3 import upload_s3_answer, upload_s3_example
#--------------------------------------------------------------------------------------------------
# get all the sub folders in a folder
# return the folder names and folder paths, like this 
# [[folder_name, folder_path], [folder_name, folder_path], [folder_name, folder_path]...]
def getSubFolders(folder_path):
    folders = []
    files_and_folders = os.listdir(folder_path)
    for file_or_folder in files_and_folders:
        path = os.path.join(folder_path, file_or_folder)
        if (not os.path.isfile(path)):
            folders.append([file_or_folder, path])
    folders.sort()
    return folders
#--------------------------------------------------------------------------------------------------
# get all the files in a folder
# return a list of file names and file paths, as a pair
# [[file_name, file_path], [file_name, file_path], [file_name, file_path] ...]
def getFiles(folder_path):
    files = []
    files_and_folders = os.listdir(folder_path)
    for file_or_folder in files_and_folders:
        path = os.path.join(folder_path, file_or_folder)
        if (os.path.isfile(path)):
            files.append([file_or_folder, path])
    files.sort()
    return files
#--------------------------------------------------------------------------------------------------
# process one course
def main():
    print("Start processing")
    # get the main mooc input folder, which we assume is the first folder
    courses = getSubFolders(COURSE_PATH)
    if (len(courses) != 1):
        print(WARNING, 'There should only be one folder in the root folder.')
        return
    course_path = courses[0][1]
    # loop
    for [section, section_path] in getSubFolders(course_path):
        print("- section", section)
        section_filename = section.lower()
        for [subsection, subsection_path] in getSubFolders(section_path):
            print("-- subsection", subsection)
            subsection_filename = section_filename + '_' + subsection.lower()
            for [unit, unit_path] in getSubFolders(subsection_path):
                print("--- unit", unit)
                unit_filename = subsection_filename + '_' + unit.lower()
                for [component, component_path] in getFiles(unit_path):
                    [component_name, component_ext] = component.lower().split('.')
                    component_filename = unit_filename + '_' + component_name
                    s3_object_name = component_filename + '.' + component_ext
                    # upload mob files to aws s3
                    if component_ext in S3_FILE_EXTENSIONS:
                        if component_name.endswith(S3_ANSWER_FILENAME):
                            upload_s3_answer(component_path, S3_ANSWERS_BUCKET,  s3_object_name)
                        else:
                            upload_s3_example(component_path, S3_EXAMPLES_BUCKET, s3_object_name)

    print("Finished processing")
#--------------------------------------------------------------------------------------------------
main()