import json
import os
import platform

userPath = os.path.expanduser("~")
 
# Set VCV Rack path based on operating system
os_name = platform.system()
if os_name == "Windows":
    vcvPath = f"{userPath}/AppData/Local/Rack2"
elif os_name == "Darwin":
    vcvPath = f"{userPath}/Library/Application Support/Rack2"
elif os_name == "Linux":
    vcvPath = f"{userPath}/.Rack2"
else:
    print(f"Error: Unsupported operating system: {os_name}")
    exit(1)

# Verify VCV Rack directory exists
if not os.path.exists(vcvPath):
    print(f"Error: VCV Rack directory not found: {vcvPath}")
    exit(1)

settingsPath = f"{vcvPath}/settings.json"
favoriteModulesPath = "./favoriteModules.json"

print("This script will export the modules in favoriteModules.json to VCV Rack")
print() 

# Reminder to close VCV Rack
print("If you run this script while VCV Rack is open, you will get unpredictable results.")
print("Close VCV Rack and press Enter to continue, or press Ctrl+C to cancel.")
input()

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

moduleInfos = settings.get("moduleInfos")
if not moduleInfos:
    print("Error: No module information found in settings file")
    exit(1)

print(f"Found {len(moduleInfos)} companies with modules")
favoriteModules = {}

# Get favorite modules
print("\nExtracting favorite modules...")
for companyName, modules in moduleInfos.items():
    for moduleName, moduleSettings in modules.items():
        if moduleSettings.get("favorite"):
            if companyName not in favoriteModules:
                favoriteModules[companyName] = []
            print(f"Status: Adding {moduleName} by {companyName} to favorites")
            favoriteModules[companyName].append(moduleName)


# Save favorite modules to favoriteModules.json
if not favoriteModules:
    print("\nWarning: No favorite modules found")

print("\nSaving favorite modules to favoriteModules.json...") 
try:
    with open(favoriteModulesPath, "w") as file:
        json.dump(favoriteModules, file, indent=4)
    print("Status: Favorites file updated successfully")
except IOError as e:
    print(f"Error: Failed to write to favorites file: {e}")
    exit()

print("Favorite modules exported from VCV Rack")
