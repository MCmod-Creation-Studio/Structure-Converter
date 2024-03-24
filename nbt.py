import json
import python_nbt.nbt as nbt
import os

def replace_quotes(input_file):
    with open(f"nbt/json/{input_file}.json", 'r') as f:
        content = f.read()

    # 替换单引号为双引号
    modified_content = content.replace("'", '"')

    with open(f"nbt/json/{input_file}.json", 'w') as f:
        f.write(modified_content)

def print_structure(filename):
    nbt_content = str(nbt.read_from_nbt_file(f"nbt/{filename}.nbt"))
    with open(f'nbt/json/{filename}.json', 'w') as f:
        f.write(nbt_content)

    replace_quotes(filename)

    with open(f'nbt/json/{filename}.json', 'r') as f:
        json_data = json.load(f)

    # print(type(json_data))

    size = json_data["value"]["size"]["value"]
    blocks = json_data["value"]["blocks"]["value"]
    palette = json_data["value"]["palette"]["value"]

    print(f"{filename} is a {size[0]}x{size[1]}x{size[2]} structure")
    output = ""

    for y in range(size[1]):
        for z in range(size[2]):
            row = ""
            for x in range(size[0]):
                index = x + size[0] * (z + size[2] * y)
                block_id = blocks[index]["state"]["value"]
                block_name = palette[block_id]["Name"]["value"]
                row += block_name + " "
            output += row + "\n"
        output += "\n"

    return output
"""
filename = input("Enter the .nbt file name (without extension): ")

output_text = print_structure(filename)

with open(f'nbt/{filename}.txt', 'w') as f:
    f.write(output_text)

print("File saved successfully.")
"""
# 所有的 .nbt
nbt_files = [file.split('.')[0] for file in os.listdir('nbt') if file.endswith('.nbt')]

for filename in nbt_files:
    output_text = print_structure(filename)
    with open(f'nbt/txt/{filename}.txt', 'w') as f:
        f.write(output_text)
    print(f"File {filename}.txt saved successfully.")