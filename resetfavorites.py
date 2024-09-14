import json
import os 

userPath = os.path.expanduser("~")
vcvPath = f"{userPath}\\AppData\\Local\\Rack2"
settingsPath = f"{vcvPath}\\settings.json"

print("This script will remove all favorites from VCV Rack")
print() 

# Reminder to close VCV Rack
print("If you run this script while VCV Rack is open, you will get unpredictable results.")
print("Close VCV Rack and press Enter to continue, or press Ctrl+C to cancel.")
input()

# Confirm with user before continuing 
print("This script will remove ALL favorite modules from VCV Rack. Are you sure you want to continue? (y/n)")
response = input()
if response != "y":
    exit()


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

moduleInfos = settings.get("moduleInfos", {})

# Remove favorite flag from all modules
print("Status: Removing favorites flag from VCV Rack modules...") 
for companyName, modules in moduleInfos.items():
    for moduleName, moduleSettings in modules.items():
        if moduleSettings.get("favorite"):
            print(f"Status: Removing favorite flag from {moduleName} by {companyName}")
            del moduleInfos[companyName][moduleName]["favorite"]

# Update settings.json 
print("Status: Updating settings.json...")
try:
    with open(settingsPath, "w") as file:
        json.dump(settings, file, indent=4)
    print("Status: Settings file updated successfully")
except IOError as e:
    print(f"Error: Failed to write to settings file: {e}")
    exit()

print("Status: All favorite modules removed from VCV Rack")