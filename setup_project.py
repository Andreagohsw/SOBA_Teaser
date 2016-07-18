import os 
import sys
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

scrub =None

file_path = sys.argv[0]
if len(sys.argv)==2:
	scrub = sys.argv[1]

host_folder = os.path.dirname(file_path)
expected_folders = ['Assets', 'sequences']
shot_projects = ['t01_01', 't01_02', 't01_03', 't01_04', 't01_05', 't01_06', 't01_07', 't01_08', 't01_09','t01_master', 't01_test']

# Retrieve list of directiories in the host folder 
dirs = [ x for x in os.walk(host_folder).next()[1] if x in expected_folders]

if len(dirs) == len(expected_folders):
	for shot in shot_projects:
		# Linking Tool Folder
		tool_source = os.path.join(host_folder, 'Assets', 'Tools')
		tool_destination = os.path.join(host_folder, 'sequences', shot, 'Assets', 'Tools')
		if os.path.exists(tool_destination):
			if scrub:
				os.rmdir(tool_destination)
			else:
				pass
		else:
			os.symlink(tool_source, tool_destination) 	
		
		# Linking Textures Folder
		texture_source = os.path.join(host_folder, 'Assets', 'Textures')
		texture_destination = os.path.join(host_folder, 'sequences', shot, 'Assets', 'Textures')
		if os.path.exists(texture_destination):
			if scrub:
				os.rmdir(texture_destination)
			else:
				pass
		else:
			os.symlink(texture_source, texture_destination)

		# Linking FBX
		setdressing_source = os.path.join(host_folder, 'Assets', 'SetDressing', 'Dead')
		setdressing_destination = os.path.join(host_folder, 'sequences', shot, 'Assets', 'SetDressing')
		if os.path.exists(setdressing_destination):
			if scrub:
				os.rmdir(setdressing_destination)
			else:
				pass
		else:
			os.symlink(setdressing_source, setdressing_destination)
		# Linking master with shots
		if not shot == 't01_master':
			# Linking Anim and Cam alembics
			if not shot == 't01_test':
				layoutanim_source = os.path.join(host_folder, 'Assets', 'Layout', 't01', 'abc', shot)
				layoutanim_destination = os.path.join(host_folder, 'sequences', shot, 'Assets', 'Layout')
				if os.path.exists(layoutanim_destination):
					if scrub:
						os.rmdir(layoutanim_destination)
					else:
						pass
				else:
					os.symlink(layoutanim_source, layoutanim_destination)

			prefabs_source = os.path.join(host_folder, 'sequences', 't01_master','Assets', 'Resources', 'Prefabs')	
			prefabs_destination = os.path.join(host_folder, 'sequences', shot, 'Assets', 'Resources', 'Prefabs', 't01_master')
			if os.path.exists(prefabs_destination):
				if scrub:
					os.rmdir(prefabs_destination)
				else:
					pass
			else:
				os.symlink(prefabs_source, prefabs_destination)

			materials_source = os.path.join(host_folder, 'sequences', 't01_master','Assets', 'Materials')	
			materials_destination = os.path.join(host_folder, 'sequences', shot, 'Assets', 'Materials', 't01_master')
			if os.path.exists(materials_destination):
				if scrub:
					os.rmdir(materials_destination)
				else:
					pass
			else:
				os.symlink(materials_source, materials_destination)

			if not shot == 't01_test':
				scene_source = os.path.join(host_folder, 'sequences', 't01_master','Assets', 'Scene')
				scene_destination = os.path.join(host_folder, 'sequences', shot, 'Assets', 'Scene', 't01_master')
				if os.path.exists(scene_destination):
					if scrub:
						os.rmdir(scene_destination)
					else:
						pass
				else:
					os.symlink(scene_source, scene_destination)
		
			tagmanager_source = os.path.join(host_folder, 'sequences', 't01_master', 'ProjectSettings', 'TagManager.asset')
			tagmanager_destination = os.path.join(host_folder, 'sequences', shot, 'ProjectSettings', 'TagManager.asset')
			if os.path.exists(tagmanager_destination):
				if scrub:
					os.remove(tagmanager_destination)
				else:
					pass
			else:
				if not os.path.exists(os.path.dirname(tagmanager_destination)):
					os.makedirs(os.path.dirname(tagmanager_destination))
				os.symlink(tagmanager_source, tagmanager_destination)

			projectsettings_source = os.path.join(host_folder, 'sequences', 't01_master', 'ProjectSettings', 'ProjectSettings.asset')
			projectsettings_destination = os.path.join(host_folder, 'sequences', shot, 'ProjectSettings', 'ProjectSettings.asset')
			if os.path.exists(projectsettings_destination):
				if scrub:
					os.remove(projectsettings_destination)
				else:
					pass
			else:
				if not os.path.exists(os.path.dirname(projectsettings_destination)):
					os.makedirs(os.path.dirname(projectsettings_destination))
				os.symlink(projectsettings_source, projectsettings_destination)
					 		
else:
	warnings.warn("Warning, no Assets or sequences folder detected! Unable to proceed")