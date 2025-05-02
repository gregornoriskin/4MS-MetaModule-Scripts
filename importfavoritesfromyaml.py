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

print("This script will import the builtin and plugin modules in plugins.yml into VCV Rack")
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

# Get the supported modules names from the yaml file and add to favorites
print("Status: Getting supported module names from plugin and builtin data and adding to VCV Rack favorites...")     
builtins = pluginData.get("built_in", {})
external = pluginData.get("external", {}) 
moduleData = {**builtins, **external} # Merge built_in and external data     

for plugin_name, plugin_info in moduleData.items(): # built_in, external
    slug = plugin_info.get("Slug", "") 
    included_modules = plugin_info.get("MetaModuleIncludedModules", {})
    for module_name, module_info in included_modules.items(): # AudibleInstruments, Befaco, etc.
        vcv_slug = module_info.get("VCVSlug", "")
        if vcv_slug:
                if slug not in moduleInfos:
                    moduleInfos[slug] = {}
                if vcv_slug not in moduleInfos[slug]:
                    moduleInfos[slug][vcv_slug] = {}
                print(f"Status: Adding {slug} from {vcv_slug} to favorites")
                moduleInfos[slug][vcv_slug]["favorite"] = True

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