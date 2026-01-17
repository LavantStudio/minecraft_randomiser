import json, os, random

global available_rp; global available_dp

errors = {0: "OK", 1: "Directory not found"}
recipe_dir = "data/minecraft/recipe/"
lang_dir = "assets/minecraft/lang/"

def check_valid_working_environment():
    global available_rp; global available_dp
    if not "data" in os.listdir():
        #erint(1, True, "data, possibly executed in wrong dir")
        available_dp = False
    else:
        available_dp = True
    if not "assets" in os.listdir():
        #erint(1, True, "data, possibly executed in wrong dir")
        available_rp = False
    else:
        available_rp = True


## Recipes

def randomise_recipes(recycle_list = False, custom_list: list = []):
    global ingredient_amount; global ingredients
    ingredients_completed = 0
    if not os.path.isdir(recipe_dir):
        erint(1, False, recipe_dir)
        return
    if custom_list == []:
        ingredients = get_ingredients()
    else:
        ingredients = custom_list
    random.shuffle(ingredients)
    for i in os.listdir(recipe_dir):
        print(f"{((ingredients_completed - 1) / ingredient_amount) * 100}% complete")
        recipe = open(recipe_dir + i)
        recipee = json.loads(recipe.read())
        recipe.close()
        match recipee["type"]:
            case "minecraft:crafting_shaped":
                for b in recipee["key"]:
                    recipee["key"][b] = pick_ingredient(not recycle_list)
                    ingredients_completed += 1
            case "minecraft:blasting" | "minecraft:campfire_cooking" | "minecraft:smelting" | "minecraft:smoking" | "minecraft:stonecutting":
                if isinstance(recipee["ingredient"], list):
                    for b in range(len(recipee["ingredient"])):
                        recipee["ingredient"][b] = pick_ingredient(not recycle_list)
                        ingredients_completed += 1
                elif isinstance(recipee["ingredient"], str):
                    recipee["ingredient"] = pick_ingredient(not recycle_list)
                    ingredients_completed += 1
            case "minecraft:crafting_transmute":
                if isinstance(recipee["input"], list):
                    for b in range(len(recipee["input"])):
                        recipee["input"][b] = pick_ingredient(not recycle_list)
                        ingredients_completed += 1
                elif isinstance(recipee["input"], str):
                    recipee["input"] = pick_ingredient(not recycle_list)
                    ingredients_completed += 1
                if isinstance(recipee["material"], list):
                    for b in range(len(recipee["material"])):
                        recipee["material"][b] = pick_ingredient(not recycle_list)
                        ingredients_completed += 1
                elif isinstance(recipee["material"], str):
                    recipee["material"] = pick_ingredient(not recycle_list)
                    ingredients_completed += 1
            case "minecraft:crafting_shapeless":
                for b in range(len(recipee["ingredients"])):
                    if isinstance(recipee["ingredients"][b], list):
                        for j in range(len(recipee["ingredients"][b])):
                            recipee["ingredients"][b][j] = pick_ingredient(not recycle_list)
                            ingredients_completed += 1
                    elif isinstance(recipee["ingredients"][b], str):
                        recipee["ingredients"][b] = pick_ingredient(not recycle_list)
                        ingredients_completed += 1
        recipe = open(recipe_dir + i, "w")
        print(recipe.write(json.dumps(recipee, indent=4)), " characters written")

def get_ingredients():
    global ingredient_amount
    amount = 0
    ingredient_amount = 0
    ingredients = []
    for i in os.listdir(recipe_dir):
        amount += 1
        recipe = open(recipe_dir + i)
        recipee = json.loads(recipe.read())
        recipe.close()
        match recipee["type"]:
            case "minecraft:crafting_shaped":
                for i in recipee["key"].values():
                    if isinstance(i, str):
                        ingredients.append(i)
                        ingredient_amount += 1
            case "minecraft:blasting" | "minecraft:campfire_cooking" | "minecraft:smelting" | "minecraft:smoking" | "minecraft:stonecutting":
                if isinstance(recipee["ingredient"], list):
                    for i in recipee["ingredient"]:
                        if isinstance(i, str):
                            ingredients.append(i)
                            ingredient_amount += 1
                elif isinstance(recipee["ingredient"], str):
                    ingredients.append(recipee["ingredient"])
                    ingredient_amount += 1
            case "minecraft:crafting_transmute":
                if isinstance(recipee["input"], list):
                    for i in recipee["input"]:
                        if isinstance(i, str):
                            ingredients.append(i)
                            ingredient_amount += 1
                elif isinstance(recipee["input"], str):
                    ingredients.append(recipee["input"])
                    ingredient_amount += 1
                if isinstance(recipee["material"], list):
                    for i in recipee["material"]:
                        if isinstance(i, str):
                            ingredients.append(i)
                            ingredient_amount += 1
                elif isinstance(recipee["material"], str):
                    ingredients.append(recipee["material"])
                    ingredient_amount += 1
            case "minecraft:crafting_shapeless":
                for i in recipee["ingredients"]:
                    if isinstance(i, list):
                        for j in i:
                            if isinstance(j, str):
                                ingredients.append(j)
                                ingredient_amount += 1
                    elif isinstance(i, str):
                        ingredients.append(i)
                        ingredient_amount += 1
    print(f"Read {amount} recipes, found {ingredient_amount} ingredients")
    return ingredients


## Lang

def randomise_lang(langid= "en_us"):
    entries = get_lang(langid)
    pool = []
    todo = len(entries)
    done = 0
    random.shuffle(entries)
    if langid + ".json" in os.listdir(lang_dir):
        lang = open(lang_dir + langid + ".json")
        langg = json.loads(lang.read())
        lang.close()
        for i in langg:
            proposal = entries.pop()
            targets = ["%s", "%1$s", "%2$s", "%3$s"]
            for l in targets:
                proposalvar = clamp(proposal.count(l), 0, 1)
                targetvar = clamp(langg[i].count(l), 0, 1)
                if targetvar > proposalvar:
                    print(proposal, proposalvar, langg[i], targetvar)
                tries = 0
                while len(pool) < 1 and proposalvar > 0:
                    if tries > len(entries):
                        pool.append("Herobrine")
                    entries = [proposal] + entries
                    print(proposal, proposalvar, proposal.count(l), len(entries))
                    proposal = entries.pop()
                    proposalvar = clamp(proposal.count(l), 0, 1)
                    tries += 1
                if proposalvar > targetvar:
                    proposal = proposal.replace(l, pool.pop())
                if proposalvar < targetvar:
                    proposall = proposal.split()
                    randlen = len(proposall) - 1
                    alltaregets = False
                    print(proposall)
                    for z in proposall:
                        if z in targets:
                            alltaregets = True
                            break
                        else:
                            alltaregets = False
                    randno = random.randint(0, randlen)
                    while proposall[randno] in targets and alltaregets == False:
                        randno = random.randint(0, randlen)
                        print(proposall, randno, proposal, alltaregets)
                    pool.append(proposall[randno])
                    proposall[randno] = l
                    proposal = list_to_str(proposall)
                if targetvar > proposalvar:
                    print(proposal, proposalvar, langg[i], targetvar)
            langg[i] = proposal
            done += 1
            print(f"{(done / todo) * 100}% complete")
        lang = open(lang_dir + langid + ".json", "w")
        lang.write(json.dumps(langg, indent=4))

def get_lang(langid = "en_us"):
    entries = []
    if langid + ".json" in os.listdir(lang_dir):
        lang = open(lang_dir + langid + ".json")
        langg = json.loads(lang.read())
        lang.close()
        for i in langg.values():
            entries.append(i)
    return entries

def pick_ingredient(delete = True):
    global ingredients
    if len(ingredients) < 2:
        delete = False
    if len(ingredients) < 1:
        choice = "minecraft:dirt"
    else:
        choice = ingredients[0]
    if delete == True:
        ingredients.pop(0)
    else:
        random.shuffle(ingredients)
    return choice

def erint(msg, fatal = False, details = []):
    if fatal:
        print("\x1b[31m", end="")
    if isinstance(msg, int):
        msg = errors[msg]
    print(f"[Error]: {msg}: {details}")
    print("\x1b[0m", end="")
    if fatal:
        quit()

def list_to_str(lis):
    stri = ""
    for i in lis:
        if isinstance(i, str):
            stri = stri + i + " "
    return stri.rstrip()

def clamp(value, min_val, max_val):
    return max(min(value, max_val), min_val)

check_valid_working_environment()
print(list_to_str(["pi", "is", "cool"]))
if available_dp == True:
    randomise_recipes()
if available_rp == True:
    randomise_lang()