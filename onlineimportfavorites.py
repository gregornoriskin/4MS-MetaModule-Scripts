import json
import os
import platform
import urllib.request
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

# URL to the YAML files
pluginUrl = "https://metamodule.info/dl/plugins.yml"
builtinUrl = "https://metamodule.info/dl/built_in.yml"

print("This script will import the supported module list from metamodule.info into VCV Rack as favorite modules")
print() 

# Reminder to close VCV Rack
print("If you run this script while VCV Rack is open, you will get unpredictable results.")
print("Close VCV Rack and press Enter to continue, or press Ctrl+C to cancel.")
input()

# Get the latest plugin and builtin yaml files
print("Status: Fetching plugin and builtin data...")
try:
    with urllib.request.urlopen(pluginUrl) as url:
        pluginData = yaml.safe_load(url)
        print("Status: Plugin data fetched successfully")
except urllib.error.URLError as e:
    print(f"Error: Failed to fetch plugin data: {e}")
    exit()

try:
    with urllib.request.urlopen(builtinUrl) as url:
        builtinData = yaml.safe_load(url)
        print("Status: Builtin data fetched successfully")
except urllib.error.URLError as e:
    print(f"Error: Failed to fetch builtin data: {e}")
    exit()

# Load settings.json
print("Status: Loading VCV Rack settings file...")
try:
    with open(settingsPath, "r") as file:
        settings = json.load(file)
        print("Status: VCV Rack settings file loaded successfully")
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

print("Status: Favorite modules imported into VCV Rack")