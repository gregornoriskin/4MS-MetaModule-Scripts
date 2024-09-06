import json
import os

# Paths to the JSON files
userPath = os.path.expanduser("~")
vcvPath = f"{userPath}\\AppData\\Local\\Rack2"
settingsPath = f"{vcvPath}\\settings.json"
favoriteModulesPath = ".\\favoriteModules.json"

# Load favoriteModules.json
with open(favoriteModulesPath, "r") as file:
    favoriteModules = json.load(file)


with open(settingsPath, "r") as file:
    settings = json.load(file)

# Get moduleInfos from settings.json
moduleInfos = settings.get("moduleInfos", {})

for companyName, modules in favoriteModules.items():
    if companyName not in moduleInfos:
        moduleInfos[companyName] = {}
    for moduleName in modules:
        if moduleName not in moduleInfos[companyName]:
            moduleInfos[companyName][moduleName] = {}
        moduleInfos[companyName][moduleName]["favorite"] = True

# Update settings.json with favorite modules
with open(settingsPath, "w") as file:
    json.dump(settings, file, indent=4)

print("Favorite modules imported into VCV Rack")