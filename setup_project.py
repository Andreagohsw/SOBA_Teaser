import os 
import sys
import subprocess
import warnings

# Handles symlink creation if OS is windows and python version is 2.7
if os.name == 'nt':
    os_symlink = getattr(os, "symlink", None)
    if callable(os_symlink):
        pass
    else:
        def symlink_ms(source, link_name):
            import ctypes
            csl = ctypes.windll.kernel32.CreateSymbolicLinkW
            csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
            csl.restype = ctypes.c_ubyte
            flags = 1 if os.path.isdir(source) else 0
            if csl(link_name, source, flags) == 0:
                raise ctypes.WinError()
        os.symlink = symlink_ms

overwrite = None

file_path = os.path.join(os.getcwd(),sys.argv[0])
if len(sys.argv) == 2:
    overwrite = sys.argv[1]

host_folder = os.path.dirname(file_path)
expected_folders = ['SOBA_Assets', 'sequences']
shot_projects = ['t01_01', 't01_02', 't01_03', 't01_04', 't01_05', 't01_06', 't01_07', 't01_08', 't01_09','t01_master', 't01_test', 't01_effects']

# Retrieve list of directiories in the host folder 
dirs = [x for x in os.walk(host_folder).next()[1] if x in expected_folders]

if len(dirs) == len(expected_folders):
        for shot in shot_projects:
            # Linking Tool Folder
            tool_source = os.path.join(host_folder, 'Assets', 'Tools')
            tool_destination = os.path.join(host_folder, 'sequences', shot, 'Assets', 'Tools')
            if os.path.exists(tool_destination):
                if overwrite:
                    if os.path.islink(tool_destination):
                        os.unlink(tool_destination)
                    else:
                        os.rmdir(tool_destination)
                    os.symlink(tool_source, tool_destination)
                else:
                    print "Error {0} exists please add overwrite flag to delete ".format(tool_destination)
            else:
                os.symlink(tool_source, tool_destination)

            # Linking Textures Folder
            texture_source = os.path.join(host_folder, 'Assets', 'Textures')
            texture_destination = os.path.join(host_folder, 'sequences', shot, 'Assets', 'Textures')
            if os.path.exists(texture_destination):
                if overwrite:
                    if os.path.islink(texture_destination):
                        os.unlink(texture_destination)
                    else:
                        os.rmdir(texture_destination)
                    os.symlink(texture_source, texture_destination)
                else:
                    print "Error {0} exists please add overwrite flag to delete ".format(texture_destination)
            else:
                os.symlink(texture_source, texture_destination)

            # Linking FBX
            setdressing_source = os.path.join(host_folder, 'Assets', 'SetDressing', 'Dead')
            setdressing_destination = os.path.join(host_folder, 'sequences', shot, 'Assets', 'SetDressing')
            if os.path.exists(setdressing_destination):
                if overwrite:
                    if os.path.islink(setdressing_destination):
                        os.unlink(setdressing_destination)
                    else:
                        os.rmdir(setdressing_destination)
                    os.symlink(setdressing_source, setdressing_destination)
                else:
                    print "Error {0} exists please add overwrite flag to delete ".format(setdressing_destination)
            else:
                os.symlink(setdressing_source, setdressing_destination)
            # Linking master with shots
            if not shot == 't01_master':
                # Linking Anim and Cam alembics
                if not shot == 't01_test' or not shot == 't01_effects' :
                    layoutanim_source = os.path.join(host_folder, 'Assets', 'Layout', 't01', 'abc', shot)
                    layoutanim_destination = os.path.join(host_folder, 'sequences', shot, 'Assets', 'Layout')
                    if os.path.exists(layoutanim_destination):
                        if overwrite:
                            if os.path.islink(layoutanim_destination):
                                os.unlink(layoutanim_destination)
                            else:
                                os.rmdir(layoutanim_destination)
                            os.symlink(layoutanim_source, layoutanim_destination)
                        else:
                            print "Error {0} exists please add overwrite flag to delete ".format(layoutanim_destination)
                    else:
                        os.symlink(layoutanim_source, layoutanim_destination)

                prefabs_source = os.path.join(host_folder, 'sequences', 't01_master','Assets', 'Resources', 'Prefabs')
                prefabs_destination = os.path.join(host_folder, 'sequences', shot, 'Assets',
                                                   'Resources', 'Prefabs', 't01_master')

                if os.path.exists(prefabs_destination):
                    if overwrite:
                        if os.path.islink(prefabs_destination):
                            os.unlink(prefabs_destination)
                        else:
                            os.rmdir(prefabs_destination)
                        os.symlink(prefabs_source, prefabs_destination)
                    else:
                        print "Error {0} exists please add overwrite flag to delete ".format(prefabs_destination)
                else:
                    if not os.path.exists(os.path.dirname(prefabs_destination)):
                        os.makedirs(os.path.dirname(prefabs_destination))
                    os.symlink(prefabs_source, prefabs_destination)

                materials_source = os.path.join(host_folder, 'sequences', 't01_master','Assets', 'Materials')
                materials_destination = os.path.join(host_folder, 'sequences', shot, 'Assets', 'Materials', 't01_master')
                if os.path.exists(materials_destination):
                    if overwrite:
                        if os.path.islink(materials_destination):
                            os.unlink(materials_destination)
                        else:
                            os.rmdir(materials_destination)
                        os.symlink(materials_source, materials_destination)
                    else:
                        print "Error {0} exists please add overwrite flag to delete ".format(materials_destination)
                else:
                    if not os.path.exists(os.path.dirname(materials_destination)):
                        os.makedirs(os.path.dirname(materials_destination))
                    os.symlink(materials_source, materials_destination)

                if not shot == 't01_test' or not shot == 't01_effects':
                    scene_source = os.path.join(host_folder, 'sequences', 't01_master','Assets', 'Scene')
                    scene_destination = os.path.join(host_folder, 'sequences', shot, 'Assets', 'Scene', 't01_master')
                    if os.path.exists(scene_destination):
                        if overwrite:
                            if os.path.islink(scene_destination):
                                os.unlink(scene_destination)
                            else:
                                os.rmdir(scene_destination)
                            os.symlink(scene_source, scene_destination)
                        else:
                            print "Error {0} exists please add overwrite flag to delete ".format(scene_destination)
                    else:
                        if not os.path.exists(os.path.dirname(scene_destination)):
                            os.makedirs(os.path.dirname(scene_destination))
                        os.symlink(scene_source, scene_destination)

                tagmanager_source = os.path.join(host_folder, 'sequences', 't01_master', 'ProjectSettings', 'TagManager.asset')
                tagmanager_destination = os.path.join(host_folder, 'sequences', shot, 'ProjectSettings', 'TagManager.asset')
                if os.path.exists(tagmanager_destination):
                    if overwrite:
                        if os.path.islink(tagmanager_destination):
                            os.unlink(tagmanager_destination)
                        else:
                            os.rmdir(tagmanager_destination)
                        os.symlink(tagmanager_source, tagmanager_destination)
                    else:
                        print "Error {0} exists please add overwrite flag to delete ".format(tagmanager_destination)
                else:
                    if not os.path.exists(os.path.dirname(tagmanager_destination)):
                        os.makedirs(os.path.dirname(tagmanager_destination))
                    os.symlink(tagmanager_source, tagmanager_destination)

                projectsettings_source = os.path.join(host_folder, 'sequences', 't01_master', 'ProjectSettings', 'ProjectSettings.asset')
                projectsettings_destination = os.path.join(host_folder, 'sequences', shot, 'ProjectSettings', 'ProjectSettings.asset')
                if os.path.exists(projectsettings_destination):
                    if overwrite:
                        if os.path.islink(projectsettings_destination):
                            os.unlink(projectsettings_destination)
                        else:
                            os.rmdir(projectsettings_destination)
                        os.symlink(projectsettings_source, projectsettings_destination)
                    else:
                        print "Error {0} exists please add overwrite flag to delete ".format(projectsettings_destination)
                else:
                    if not os.path.exists(os.path.dirname(projectsettings_destination)):
                        os.makedirs(os.path.dirname(projectsettings_destination))
                    os.symlink(projectsettings_source, projectsettings_destination)

else:
    warnings.warn("Warning, no Assets or sequences folder detected! Unable to proceed")