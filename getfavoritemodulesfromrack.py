import json
import os 

userPath = os.path.expanduser("~")
vcvPath = f"{userPath}\\AppData\\Local\\Rack2"
settingsPath = f"{vcvPath}\\settings.json"

# Load settings.json
with open(settingsPath, "r") as file:
    settings = json.load(file)

moduleInfos = settings.get("moduleInfos")

favoriteModules = {}

# Get favorite modules
for companyName, modules in moduleInfos.items():
    for moduleName, moduleSettings in modules.items():
        if moduleSettings.get("favorite"):
            if companyName not in favoriteModules:
                favoriteModules[companyName] = []
            favoriteModules[companyName].append(moduleName)

favoriteModulesPath = f"./favoriteModules.json"

# Save favorite modules to favoriteModules.json
with open(favoriteModulesPath, "w") as file:
    json.dump(favoriteModules, file, indent=4)

print("Favorite modules imported into VCV Rack")