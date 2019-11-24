import sys, os
import tarfile
import shutil
import __CONSTS__ 
import _edx_consts
import _read_metadata
import _write_structure
import _write_comps
import _util

#--------------------------------------------------------------------------------------------------
# Text strings
WARNING = "      WARNING:"

#--------------------------------------------------------------------------------------------------
# write the image to the assets folder
# returns void
def writeAsset(component_path, component, unit_filename):

    # copy the image to the assets folder

    out_path = os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.STATIC_FOLDER, 
        unit_filename + '_' + component)

    shutil.copyfile(component_path, out_path)

#--------------------------------------------------------------------------------------------------
# process one course
def processCourse():

    # get the main mooc input folder, which we assume is the first folder
    courses = _util.getSubFolders(__CONSTS__.COURSE_PATH)
    if (len(courses) != 1):
        print(WARNING, 'There should only be one folder in the root folder.')
        return

    # select the first subfolder
    course_path = courses[0][1]

    # make the folders inside the output folder
    os.mkdir(os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.COURSE_FOLDER))
    os.mkdir(os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.SECTION_FOLDER))
    os.mkdir(os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.SUBSECTION_FOLDER))
    os.mkdir(os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.UNIT_FOLDER))
    os.mkdir(os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.COMP_HTML_FOLDER))
    os.mkdir(os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.COMP_VIDS_FOLDER))
    os.mkdir(os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.COMP_PROBS_FOLDER))
    os.mkdir(os.path.join(__CONSTS__.OUTPUT_PATH, _edx_consts.STATIC_FOLDER))

    # create the root xml file
    course_filename = _write_structure.writeXmlForRoot()

    # main loop
    sections = []

    for [section, section_path] in _util.getSubFolders(course_path):
        print("- section", section)
        section_filename = section.lower()
        sections.append(section_filename)
        subsections = []

        for [subsection, subsection_path] in _util.getSubFolders(section_path):
            print("-- subsection", subsection)
            subsection_filename = section_filename + '_' + subsection.lower()
            subsections.append(subsection_filename)
            units = []

            for [unit, unit_path] in _util.getSubFolders(subsection_path):
                print("--- unit", unit)
                unit_filename = subsection_filename + '_' + unit.lower()
                units.append(unit_filename)
                comps = []

                # process all the files it finds
                for [filename, filepath] in _util.getFiles(unit_path):
                    filex = filename.lower().split('.')[1]
                    
                    # write the files
                    if filex == 'md':
                        unit_comps = _write_comps.writeCompsForUnit(filepath, unit_filename)
                        for [unit_comp_filename, unit_comp_type] in unit_comps:
                            comps.append([unit_comp_filename, unit_comp_type])

                    # put assets in static folder of zip
                    elif filex in __CONSTS__.ASSET_FILE_EXTENSIONS:
                        # this is an asset that needs to get copied to the STATIC folder
                        writeAsset(filepath, filename, unit_filename)

                    else:
                        pass
                        # could be any other file, just ignore and continue
                        

                _write_structure.writeXmlForUnit(unit_path, unit_filename, comps)

            _write_structure.writeXmlForSubsection(subsection_path, subsection_filename, units)

        _write_structure.writeXmlForSection(section_path, section_filename, subsections)

    _write_structure.writeXmlForCourse(course_path, course_filename, sections)

#--------------------------------------------------------------------------------------------------
def main():

    print("Start compiling")

    # check the input and output folders
    print("in", __CONSTS__.COURSE_PATH)
    if (not os.path.isdir(__CONSTS__.COURSE_PATH)):
        print("The input path is not a valid path")
        return
    print("out", __CONSTS__.OUTPUT_PATH)
    try:
        if (os.path.isdir(__CONSTS__.OUTPUT_PATH)):
            print("Deleting contents in " + __CONSTS__.OUTPUT_PATH)
            shutil.rmtree(__CONSTS__.OUTPUT_PATH)
        os.mkdir(__CONSTS__.OUTPUT_PATH)
    except:
        print("Failed to create the output folder: " + __CONSTS__.OUTPUT_PATH)
    
    # create content
    processCourse()

    # create the tar file
    [out_folder_path, out_folder_name] = os.path.split(__CONSTS__.OUTPUT_PATH)
    tar = tarfile.open(out_folder_name + ".tar.gz", "w:gz")
    os.chdir(out_folder_path)
    tar.add(out_folder_name, recursive=True)
    tar.close()

    print("Finish compiling")

#--------------------------------------------------------------------------------------------------
main()
