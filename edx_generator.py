import sys, os
#--------------------------------------------------------------------------------------------------
if len(sys.argv) != 3:
    print(sys.argv)
    raise Exception('Usage: python ./edx_generator.py input_path output_path')
if not os.path.exists(sys.argv[1]):
    raise Exception('Path does not exist: ' + sys.argv[1])
if not os.path.exists(os.path.join(sys.argv[1], '__SETTINGS__.py')):
    raise Exception('Path does not contain __SETTINGS__.py: ' + sys.argv[1])
if not os.path.exists(sys.argv[2]):
    raise Exception('Path does not exist: ' + sys.argv[2])
sys.path.append(sys.argv[1])
#--------------------------------------------------------------------------------------------------
import tarfile
import shutil
import _edx_consts
import _read_metadata
import _write_structure
import _write_comps
import _util
import __SETTINGS__
#--------------------------------------------------------------------------------------------------
# Text strings
WARNING = "      WARNING:"

#--------------------------------------------------------------------------------------------------
# write the image to the assets folder
# returns void
def writeAsset(component_path, component, unit_filename):

    # copy the image to the assets folder

    out_path = os.path.join(sys.argv[2], _edx_consts.STATIC_FOLDER, 
        unit_filename + '_' + component)

    shutil.copyfile(component_path, out_path)

#--------------------------------------------------------------------------------------------------
# process one course
def processCourse():

    # get the main mooc input folder, which we assume is the first folder
    root_folder = os.path.normpath(sys.argv[1])
    course_path = os.path.join(root_folder, 'Course')

    # make the folders inside the output folder
    os.mkdir(os.path.join(sys.argv[2], _edx_consts.COURSE_FOLDER))
    os.mkdir(os.path.join(sys.argv[2], _edx_consts.SECTION_FOLDER))
    os.mkdir(os.path.join(sys.argv[2], _edx_consts.SUBSECTION_FOLDER))
    os.mkdir(os.path.join(sys.argv[2], _edx_consts.UNIT_FOLDER))
    os.mkdir(os.path.join(sys.argv[2], _edx_consts.COMP_HTML_FOLDER))
    os.mkdir(os.path.join(sys.argv[2], _edx_consts.COMP_VIDS_FOLDER))
    os.mkdir(os.path.join(sys.argv[2], _edx_consts.COMP_PROBS_FOLDER))
    os.mkdir(os.path.join(sys.argv[2], _edx_consts.STATIC_FOLDER))

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
                    elif filex in __SETTINGS__.EDX_ASSET_FILE_EXTENSIONS:
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
    print("in", sys.argv[1])
    if (not os.path.isdir(sys.argv[1])):
        print("The input path is not a valid path")
        return
    print("out", sys.argv[2])
    try:
        if (os.path.isdir(sys.argv[2])):
            print("Deleting contents in " + sys.argv[2])
            shutil.rmtree(sys.argv[2])
        os.mkdir(sys.argv[2])
    except:
        print("Failed to create the output folder: " + sys.argv[2])
    
    # create content
    processCourse()

    # create the tar file
    [out_folder_path, out_folder_name] = os.path.split(sys.argv[2])
    tar_path = os.path.normpath(os.path.join(sys.argv[2], '..'))
    tar_file_path = os.path.join(tar_path, __SETTINGS__.S3_MOOC_FOLDER + '.tar.gz')
    tar = tarfile.open(tar_file_path, 'w:gz')
    os.chdir(out_folder_path)
    tar.add(out_folder_name, recursive=True)
    tar.close()

    print("Finish compiling")
    print("Tar file written to", tar_file_path)

#--------------------------------------------------------------------------------------------------
main()
