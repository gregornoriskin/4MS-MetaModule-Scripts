import json
import os

# Paths to the JSON files
userPath = os.path.expanduser("~")
vcvPath = f"{userPath}\\AppData\\Local\\Rack2"
settingsPath = f"{vcvPath}\\settings.json"
favoriteModulesPath = ".\\favoriteModules.json"

print("This script will import the modules in favoriteModules.json into VCV Rack")
print() 

# Reminder to close VCV Rack
print("If you run this script while VCV Rack is open, you will get unpredictable results.")
print("Close VCV Rack and press Enter to continue, or press Ctrl+C to cancel.")
input()

# Load favoriteModules.json
print("Status: Loading favoriteModules.json...")
try:
    with open(favoriteModulesPath, "r") as file:
        favoriteModules = json.load(file) 
except FileNotFoundError:
    print(f"Error: favoriteModules.json not found: {favoriteModulesPath}")
    exit()
except json.JSONDecodeError as e:
    print(f"Error: Failed to decode JSON from favoriteModules.json: {e}")
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
moduleInfos = settings.get("moduleInfos", {})

# Add favorite flag to modules in favoriteModules
print("Status: Adding favorites flag to VCV Rack modules...")
for companyName, modules in favoriteModules.items():
    if companyName not in moduleInfos:
        moduleInfos[companyName] = {}
    for moduleName in modules:
        if moduleName not in moduleInfos[companyName]:
            moduleInfos[companyName][moduleName] = {}
        print(f"Status: Adding {companyName} from {moduleName} to favorites")
        moduleInfos[companyName][moduleName]["favorite"] = True

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