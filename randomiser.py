import json, os, random

errors = {0: "OK", 1: "Directory not found"}
recipe_dir = "data/minecraft/recipe/"

def check_valid_working_environment():
    if not "data" in os.listdir():
        erint(1, True, "data, possibly executed in wrong dir")

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


check_valid_working_environment()
randomise_recipes()