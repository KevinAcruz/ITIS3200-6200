import os
import json
import hashlib

#making hash file with sha256 
def hash_file(path):
    with open(path, "rb") as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()

def get_all_files(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for name in filenames:
            files.append(os.path.join(root, name))
    return files


def make_hash_table(directory, output_file):
    print("Scanning directory:", directory)

    files = get_all_files(directory)
    
  
    hash_table = {
        "files": []
    }
     #Formatting 
    for file_path in files:
        try:
            file_hash = hash_file(file_path)
            hash_table["files"].append({
                "filepath": file_path,
                "hash": file_hash
            })
            print("Hashed:", file_path)

        except:
            print("Error reading:", file_path)
            hash_table["files"].append({
                "filepath": file_path,
                "hash": "ERROR"
            })

    with open(output_file, "w") as f:
        json.dump(hash_table, f, indent=4)

    print("Done! Hash table saved to", output_file)




def check_hashes(hash_table_file, directory):
    with open(hash_table_file, "r") as f:
        data = json.load(f)

    saved_list = data["files"]  
    current_files = get_all_files(directory)

    saved_paths = []
    saved_hashes = {}

    for item in saved_list:
        path = item["filepath"]
        saved_paths.append(path)
        saved_hashes[path] = item["hash"]

    for file in current_files:
        if file not in saved_paths:
            print("NEW FILE:", file)

    for file in saved_paths:
        if file not in current_files:
            print("DELETED:", file)

    for file in saved_paths:
        if file not in current_files:
            continue

        old_hash = saved_hashes[file]

        if old_hash == "ERROR":
            print("SKIP (error before):", file)
            continue

        try:
            new_hash = hash_file(file)
            if new_hash == old_hash:
                print("VALID:", file)
            else:
                print("INVALID:", file)
        except:
            print("ERROR checking:", file)



#Gui choices 
if __name__ == "__main__":

    print("=== File Hash Checker ===")
    print("1. Generate hash table")
    print("2. Verify hashes")

    choice = input("\nChoose option: ")

    if choice == "1":
        dir_path = input("Enter directory to scan: ")
        out_name = input("Output file name (e.g. hashes.json): ")

        if not out_name.endswith(".json"):
            out_name += ".json"

        if not os.path.isdir(dir_path):
            print("That's not a valid directory!")
        else:
            make_hash_table(dir_path, out_name)

    elif choice == "2":
        table_file = input("Enter hash table file: ")
        dir_path = input("Enter directory to check: ")

        if not os.path.isfile(table_file):
            print("Can't find that hash table file!")
        elif not os.path.isdir(dir_path):
            print("That's not a valid directory!")
        else:
            check_hashes(table_file, dir_path)

    else:
        print("Invalid option")