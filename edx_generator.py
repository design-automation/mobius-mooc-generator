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
# read md
# write to either units folder or problems folder, depending on the type
def processMd(component_path, component_filename, unit_filename):

    # print("component_path", component_path)

    # generate the files in the right folders
    [content, meta] = _read_metadata.getComponentContentMeta(component_path)

    # get component type
    comp_type = meta['type']
    if comp_type:
        comp_type = comp_type[0]
    else:
        print(WARNING, 'Error: Component type missing:', component_path)
        return 

    # generate xml files
    if comp_type == 'html':

        settings = _read_metadata.getMetaSettings(component_path, meta, 
            _edx_consts.COMP_HTML_REQ, _edx_consts.COMP_HTML_OPT )

        _write_comps.writeXmlForHtmlComp(
            component_path, component_filename, content, settings, unit_filename)
    
    elif comp_type == 'problem-checkboxes':
        
        settings = _read_metadata.getMetaSettings(component_path, meta, 
            _edx_consts.COMP_PROB_CHECKBOXES_REQ, _edx_consts.COMP_PROB_CHECKBOXES_OPT )
            
        _write_comps.writeXmlForProbCheckboxesComp(
            component_path, component_filename, content, settings, unit_filename)
    
    elif comp_type == 'problem-submit':
        
        settings = _read_metadata.getMetaSettings(component_path, meta, 
            _edx_consts.COMP_PROB_SUBMIT_REQ , _edx_consts.COMP_PROB_SUBMIT_OPT )

        _write_comps.writeXmlForSubmitComp(
            component_path, component_filename, content, settings, unit_filename)
    
    elif comp_type == 'video':
        
        settings = _read_metadata.getMetaSettings(component_path, meta, 
            _edx_consts.COMP_VIDEO_REQ, _edx_consts.COMP_VIDEO_OPT )
            
        _write_comps.writeXmlForVidComp(
            component_filename, content, settings, unit_filename)
    
    else:
        print(WARNING, 'Error: Component type not recognised:', comp_type, "in", component_path)

    # return the component type, which is needed for generating the xml for the subsection
    # if comp_type.startswith('problem'):
    #     comp_type = 'problem'

    # return the type
    return comp_type

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
                components = []

                for [component, component_path] in _util.getFiles(unit_path):
                    [component_name, component_ext] = component.lower().split('.')
                    component_filename = unit_filename + '_' + component_name

                    # write the files
                    if component_ext == 'md':

                        if not component_path.endswith('settings.md'):
                            # this is md, not a settings file
                            # this can be html, problem, or video
                            component_type = processMd(component_path, component_filename, unit_filename)
                            components.append([component_filename, component_type])

                    elif component_ext in ['htm','html']:
                        # this is an html snippet, only used in special cases
                        _write_comps.processRawHtmlComp(component_path, component_filename)
                        components.append([component_filename, 'html'])

                    elif component_ext in __CONSTS__.ASSET_FILE_EXTENSIONS:
                        # this is an asset that needs to get copied to the STATIC folder
                        writeAsset(component_path, component, unit_filename)

                    else:
                        pass
                        # could be any other file, just ignore and continue

                _write_structure.writeXmlForUnit(unit_path, unit_filename, components)

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
