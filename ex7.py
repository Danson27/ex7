

#/******************
#Name: Dan Sonnenblick
#ID: 345287882
#Assignment: ex7
#*******************/


import csv

# Global BST root
ownerRoot = None

########################
# 0) Read from CSV -> HOENN_DATA
########################


def read_hoenn_csv(filename):
    """
    Reads 'hoenn_pokedex.csv' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" },
        ... ]
    """
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')  # Use comma as the delimiter
        first_row = True
        for row in reader:
            # It's the header row (like ID,Name,Type,HP,Attack,Can Evolve), skip it
            if first_row:
                first_row = False
                continue

            # row => [ID, Name, Type, HP, Attack, Can Evolve]
            if not row or not row[0].strip():
                break  # Empty or invalid row => stop
            d = {
                "ID": int(row[0]),
                "Name": str(row[1]),
                "Type": str(row[2]),
                "HP": int(row[3]),
                "Attack": int(row[4]),
                "Can Evolve": str(row[5]).upper()
            }
            data_list.append(d)
    return data_list


HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")

########################
# 1) Helper Functions
########################

def read_int_safe(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_poke_dict_by_id(poke_id):
    for pokemon in HOENN_DATA:
        if pokemon["ID"] == poke_id:
            return pokemon.copy()
    return None

def get_poke_dict_by_name(name):
    for pokemon in HOENN_DATA:
        if pokemon["Name"].lower() == name.lower():
            return pokemon
    return None

def display_pokemon_list(poke_list):
    """
    Display a list of Pokemon dicts, or a message if empty.
    """
    if not poke_list:
        print("There are no Pokemons in this Pokedex that match the criteria.")
        return
    for pokemon in poke_list:
        print(f"ID: {pokemon['ID']}, Name: {pokemon['Name']}, Type: {pokemon['Type']}, "
              f"HP: {pokemon['HP']}, Attack: {pokemon['Attack']}, Can Evolve: {str(pokemon['Can Evolve']).upper()}")



########################
# 2) BST (By Owner Name)
########################

# Create and return a BST node dict with keys: 'owner', 'pokedex', 'left', 'right'.
def create_owner_node(owner_name, first_pokemon=None):
    if first_pokemon:
        print(f"New Pokedex created for {owner_name} with starter {first_pokemon['Name']}.")
    else:
        print(f"New Pokedex created for {owner_name} with no starter Pokémon.")
    return {
        "owner": owner_name,
        "pokedex": [first_pokemon] if first_pokemon else [],
        "left": None,
        "right": None,
    }


#"""
#Insert a new BST node by owner_name (alphabetically). Return updated root.
#"""
def insert_owner_bst(root, new_node):
    if root is None:
        return new_node
    elif new_node["owner"].lower() < root["owner"].lower():
        root["left"] = insert_owner_bst(root["left"], new_node)
    elif new_node["owner"].lower() > root["owner"].lower():
        root["right"] = insert_owner_bst(root["right"], new_node)
    return root


#"""
#Locate a BST node by owner_name.
#"""r
def find_owner_bst(root, owner_name):
    if root is None:
        return None
    if root["owner"].lower() == owner_name.lower():
        return root
    elif owner_name.lower() < root["owner"].lower():
        return find_owner_bst(root["left"], owner_name)
    else:
        return find_owner_bst(root["right"], owner_name)


def min_node(node):
    """
    Return the leftmost node in a BST subtree.
    """
    current = node
    while current and current["left"] is not None:
        current = current["left"]
    return current


def delete_owner_bst(root, owner_name):
    """
    Remove a node from the BST by owner_name. Return updated root.
    """
    if root is None:
        return root
    elif owner_name.lower() < root["owner"].lower():
        root["left"] = delete_owner_bst(root["left"], owner_name)
    elif owner_name.lower() > root["owner"].lower():
        root["right"] = delete_owner_bst(root["right"], owner_name)

    else:
        print(f"Deleting '{owner_name}''s entire Pokedex.")

        if root["left"] is None and root["right"] is None:
            return None
        elif root["left"] is None:
            return root["right"]
        elif root["right"] is None:
            return root["left"]
        else:
            min = min_node(root["right"])
            root["owner"] = min["owner"]
            root["pokedex"] = min["pokedex"]
            root["right"] = delete_owner_bst(root["right"], min["owner"])
    return root


def display_owners_by_num_pokemon():
    owners = []
    gather_all_owners(ownerRoot, owners)

    owners.sort(key=lambda x: (len(x["pokedex"]), x["owner"].lower()))
    print("=== The Owners we have, sorted by number of Pokemons ===")
    print(" ")
    for owner in owners:
        print(f"Owner: {owner['owner']} (has {len(owner['pokedex'])} Pokemon)")

########################
# 4) Pokedex Operations
########################
def enterPokedexMenu(selectedOwner):
    while True:
        print("")
        print(f"-- {selectedOwner['owner']}'s Pokedex Menu --")
        print("1. Add Pokemon")
        print("2. Display Pokedex")
        print("3. Release Pokemon")
        print("4. Evolve Pokemon")
        print("5. Back to Main")
        subChoice = int(input("Your choice: "))
        if subChoice == 1:
            add_pokemon_to_owner(selectedOwner)
        elif subChoice == 2:
            display_filter_sub_menu(selectedOwner)
        elif subChoice == 3:
            release_pokemon_by_name(selectedOwner)
        elif subChoice == 4:
            evolve_pokemon_by_name(selectedOwner)
        elif subChoice == 5:
            print("Back to Main Menu.")
            break
        else:
            print("Invalid choice. Please try again.")


def add_pokemon_to_owner(owner_node):
    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    while True:
        pokeIDToAdd = int(input("Enter Pokemon ID to add: "))
        newPokemon = get_poke_dict_by_id(pokeIDToAdd)
        if not newPokemon:
            print(f"ID {pokeIDToAdd} not found in Honen data.")
            break
        if any(pokemon["ID"] == pokeIDToAdd for pokemon in owner_node["pokedex"]):
            print("Pokemon already in the list. No changes made.")
            break
        else:
            #add the pokemon to the owners pokedex
            owner_node["pokedex"].append(newPokemon)
            print(f"Pokemon {newPokemon['Name']} (ID {pokeIDToAdd}) added to {owner_node['owner']}'s Pokedex.")

        break

def release_pokemon_by_name(owner_node):
    """
    Prompt user for a Pokemon name, remove it from this owner's pokedex if found.
    """
    pokeName = input("Enter Pokemon Name to release: ").strip()
    for i, pokemon in enumerate(owner_node["pokedex"]):
        if pokemon["Name"].lower() == pokeName.lower():
            removed_pokemon = owner_node["pokedex"].pop(i)
            print(f"Releasing {removed_pokemon['Name']} from {owner_node['owner']}.")
            return

    print(f"No Pokemon named '{pokeName}' in {owner_node['owner']}'s Pokedex.")


def evolve_pokemon_by_name(owner_node):
    """
    Evolve a Pokemon by name:
    1) Check if it can evolve
    2) Remove old
    3) Insert new
    4) If new is a duplicate, remove it immediately
    """
    pokeNameForEvolve = input("Enter Pokemon Name to evolve: ").strip()
    found = False  # Flag to check if the Pokémon is found

    for i, pokemon in enumerate(owner_node["pokedex"]):
        if pokemon["Name"].lower() == pokeNameForEvolve.lower():
            found = True  # Set flag to True when found
            if pokemon["Can Evolve"] == "TRUE":
                old_pokemon = owner_node["pokedex"].pop(i)
                evolved_pokemon = get_poke_dict_by_id(old_pokemon["ID"] + 1)
                if any(p["ID"] == evolved_pokemon["ID"] for p in owner_node["pokedex"]):
                    print(f"Pokemon evolved from {old_pokemon['Name']} (ID {old_pokemon['ID']}) "
                          f"to {evolved_pokemon['Name']} (ID {evolved_pokemon['ID']}).")
                    print(f"{evolved_pokemon['Name']} was already present; releasing it immediately.")
                    return
                owner_node["pokedex"].append(evolved_pokemon)
                print(f"Pokemon evolved from {old_pokemon['Name']} (ID {old_pokemon['ID']}) "
                      f"to {evolved_pokemon['Name']} (ID {evolved_pokemon['ID']}).")
                return

    # If loop completes and `found` is still False, print the error message
    if not found:
        print(f"No Pokemon named '{pokeNameForEvolve}' in {owner_node['owner']}'s Pokedex.")


########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, owners_list):
    """
    Collect all owners and their Pokémon counts from the BST into a list.
    """
    if root is not None:
        gather_all_owners(root["left"], owners_list)
        if "owner" in root and "pokedex" in root:
            owners_list.append(root)
        gather_all_owners(root["right"], owners_list)


def sort_owners_by_num_pokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    pass


########################
# 6) Print All
########################

def print_all_owners():
    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    print("1) BFS")
    print("2) Pre-Order")
    print("3) In-Order")
    print("4) Post-Order")
    method = read_int_safe("Your Choice: ")
    if method == 1:
        bfs_print(ownerRoot)
    elif method == 2:
        pre_order_print(ownerRoot)
    elif method == 3:
        in_order_print(ownerRoot)
    elif method == 4:
        post_order_print(ownerRoot)
    else:
        print("Invalid choice.")


def pre_order_print(root):
    """
    Helper to print data in pre-order.
    """
    if ownerRoot is None:
        return
    if root is not None:
        print_owner_data(root)
        pre_order_print(root["left"])
        pre_order_print(root["right"])

def in_order_print(root):
    """
    Helper to print data in in-order.
    """
    if root is not None:
        in_order_print(root["left"])
        print_owner_data(root)
        in_order_print(root["right"])
    else:
        return

def post_order_print(root):
    """
    Helper to print data in post-order.
    """
    if root is not None:
        post_order_print(root["left"])
        print_owner_data(root)
        post_order_print(root["right"])


def bfs_print(root):
    """
    Helper to print data in Breadth-First Search (BFS) order.
    """
    if root is None:
        return

    queue = [root]  # Initialize queue with the root node

    while queue:
        node = queue.pop(0)  # Assign 'node' before using it

        print_owner_data(node)
        if node["left"]:
            queue.append(node["left"])
        if node["right"]:
            queue.append(node["right"])

def print_owner_data(node):
    """
    Prints the owner and their Pokémon in the required format.
    """
    print(f"Owner: {node['owner']}")
    for pokemon in node["pokedex"]:
        print(f"ID: {pokemon['ID']}, Name: {pokemon['Name']}, Type: {pokemon['Type']}, "
              f"HP: {pokemon['HP']}, Attack: {pokemon['Attack']}, "
              f"Can Evolve: {"TRUE" if pokemon["Can Evolve"] == "TRUE" else "FALSE"}")
    print()

########################
# 7) The Display Filter Sub-Menu
########################

def display_filter_sub_menu(owner_node):
    while True:
        print("-- Display Filter Menu --")
        print("1. Only a certain Type")
        print("2. Only Evolvable")
        print("3. Only Attack above __")
        print("4. Only HP above __")
        print("5. Only names starting with letter(s)")
        print("6. All of them!")
        print("7. Back")
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            type = input("Which Type? (e.g. GRASS, WATER): ").strip().lower()
            filteredForType = [p for p in owner_node["pokedex"] if p["Type"].lower() == type]
            display_pokemon_list(filteredForType)
        elif choice == 2:
            filteredForEvolve = [p for p in owner_node["pokedex"] if p["Can Evolve"] == "TRUE"]
            display_pokemon_list(filteredForEvolve)
        elif choice == 3:
            max_attack = int(input("Enter Attack threshold: "))
            filteredForAttack = [p for p in owner_node["pokedex"] if p["Attack"]>max_attack]
            display_pokemon_list(filteredForAttack)
        elif choice == 4:
            max_hp = int(input("Enter HP threshold: "))
            filteredForHP = [p for p in owner_node["pokedex"] if p["HP"] > max_hp]
            display_pokemon_list(filteredForHP)
        elif choice == 5:
            name_start = input("Starting letter(s): ").strip().capitalize()
            filteredByName = [p for p in owner_node["pokedex"] if p["Name"].lower().startswith(name_start.lower())]
            display_pokemon_list(filteredByName)
        elif choice == 6:
            display_pokemon_list(owner_node["pokedex"])
        elif choice == 7:
            print("Back to Pokedex Menu.")
            break
        else:
            print("Invalid choice. Please try again.")



########################
# 8) Sub-menu & Main menu
########################

def main_menu():
    global ownerRoot
    while True:
        print("\n=== Main Menu ===")
        print("1. New Pokedex")
        print("2. Existing Pokedex")
        print("3. Delete a Pokedex")
        print("4. Display owners by number of Pokemon")
        print("5. Print All")
        print("6. Exit")
        choice = input("Your choice: ")
        if choice == "1":
            owner_name = input("Owner name: ")
            if find_owner_bst(ownerRoot,owner_name) is not None:
                print(f"Owner '{owner_name}' already exists. No new Pokedex created.")
            else:
                print ("Choose your starter Pokemon: ")
                print("1) Treecko")
                print("2) Torchic")
                print("3) Mudkip")
                starter_choice= read_int_safe("Your choice: ")
                starter_pokemon = None
                if starter_choice == 1:
                    starter_pokemon = get_poke_dict_by_id(1)
                elif starter_choice == 2:
                    starter_pokemon = get_poke_dict_by_id(4)
                elif starter_choice == 3:
                    starter_pokemon = get_poke_dict_by_id(7)
                else:
                    print ("Invalid choice")

                newOwner = create_owner_node(owner_name, starter_pokemon)
                ownerRoot = insert_owner_bst(ownerRoot, newOwner)
        elif choice == "2":
            if ownerRoot is None:
                print ("No exisiting Pokedexes.")
            else:
                owner_name = input("Owner name: ").strip().lower()
                if find_owner_bst(ownerRoot,owner_name) is None:
                    print(f"Owner '{owner_name}' not found.")
                else:
                    selectedOwner = find_owner_bst(ownerRoot, owner_name)
                    if selectedOwner:
                        enterPokedexMenu(selectedOwner)
        elif choice == "3":
            if ownerRoot is None:
                print ("No exisiting Pokedexes.")
            else:
                owner_to_delete = input("Enter owner to delete: ").lower()
                if find_owner_bst(ownerRoot,owner_to_delete) is None:
                    print(f"Owner '{owner_to_delete}' not found.")
                else:
                    selectedOwner = find_owner_bst(ownerRoot, owner_to_delete)
                    if selectedOwner:
                        ownerRoot = delete_owner_bst(ownerRoot, selectedOwner["owner"])
        elif choice == "4":
            if ownerRoot is None:
                print ("No owners at all.")
            else:
                display_owners_by_num_pokemon()
        elif choice == "5":
            if ownerRoot is None:
                print ("No owners at all. ")
            else:
                print_all_owners()
        elif choice == "6":
            print("Goodbye!")
            break



def main():
    """
    Entry point: calls main_menu().
    """
    main_menu()


if __name__ == "__main__":
    main()
