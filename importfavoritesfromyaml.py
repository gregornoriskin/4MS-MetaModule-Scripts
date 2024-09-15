import json
import os
import platform
import yaml

userPath = os.path.expanduser("~")
 
# Set VCV Rack path based on operating system
os_name = platform.system()
if os_name == "Windows":
    vcvPath = f"{userPath}/AppData/Local/Rack2"
elif os_name == "Darwin":
    vcvPath = f"{userPath}/Library/Application Support/Rack2"
else:
    print(f"Unsupported operating system: {os_name}")
    exit()

settingsPath = f"{vcvPath}/settings.json"
pluginPath = "./plugins.yml"
builtinPath = "./built_in.yml"

print("This script will import the modules in plugins.yml and built_in.yml into VCV Rack")
print() 

# Reminder to close VCV Rack
print("If you run this script while VCV Rack is open, you will get unpredictable results.")
print("Close VCV Rack and press Enter to continue, or press Ctrl+C to cancel.")
input()

# Load plugins.yml
print("Status: Loading plugins.yml...")
try:
    with open(pluginPath, "r") as pluginFile:
        pluginData = yaml.safe_load(pluginFile)
except FileNotFoundError:
    print(f"Error: Plugin file not found: {pluginPath}")
    exit()

# load built_in.yml
print("Status: Loading built_in.yml...")
try:
    with open(builtinPath, "r") as builtinFile:
        builtinData = yaml.safe_load(builtinFile)
except FileNotFoundError:
    print(f"Error: Built-in file not found: {builtinPath}")
    exit()  

# Load settings.json
print("Status: Loading VCV Rack settings file...")
try:
    with open(settingsPath, "r") as file:
        settings = json.load(file)
except FileNotFoundError:
    print(f"Error: Settings file not found: {settingsPath}")
    exit()
except json.JSONDecodeError as e:
    print(f"Error: Failed to decode JSON from settings file: {e}")
    exit()

   
# Get moduleInfos from settings.json
print("Status: Getting installed module list from settings.json...")
moduleInfos = settings.get("moduleInfos", {})

# Get the supported modules names from the yaml files and add to favorites
print("Status: Getting supported module names from plugin and builtin data and adding to VCV Rack favorites...")           
for moduleData in [builtinData, pluginData]:
    for slugData in moduleData.values():
        for version in slugData.get("Versions", {}):
            slugName = slugData.get("Slug", "")
            for includedSlug in version.get("MetaModuleIncludedSlugs", {}):          
                # Add the module to favorites if it is not already there
                # Note this may be that the module is not installed or that it has not settings.
                # Assert: Having a favorite setting for a module that is not installed should not cause any issues.
                if slugName not in moduleInfos:
                    moduleInfos[slugName] = {}
                if includedSlug not in moduleInfos[slugName]:
                    moduleInfos[slugName][includedSlug] = {}
                print(f"Status: Adding {includedSlug} from {slugName} to favorites")
                moduleInfos[slugName][includedSlug]["favorite"] = True

# Update settings.json with favorite modules
print("Status: Updating settings.json...")
try:
    with open(settingsPath, "w") as file:
        json.dump(settings, file, indent=4)
    print("Status: Settings file updated successfully")
except IOError as e:
    print(f"Error: Failed to write to settings file: {e}")
    exit()

print("Favorite modules imported into VCV Rack")