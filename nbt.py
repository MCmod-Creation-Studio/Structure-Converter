import json
import python_nbt.nbt as nbt
import os

# 新建文件（如果没有）
os.makedirs('./nbt/json', exist_ok=True)
os.makedirs('./nbt/txt/texture', exist_ok=True)
def replace_quotes(input_file):
    with open(f"nbt/json/{input_file}.json", 'r') as f:
        content = f.read()

    # 替换单引号为双引号
    modified_content = content.replace("'", '"')

    with open(f"nbt/json/{input_file}.json", 'w') as f:
        f.write(modified_content)


def print_structure(filename):
    nbt_content = nbt.read_from_nbt_file(f"nbt/{filename}.nbt")
    with open(f'nbt/json/{filename}.json', 'w') as f:
        f.write(str(nbt_content))

    replace_quotes(filename)

    with open(f'nbt/json/{filename}.json', 'r') as f:
        json_data = json.load(f)

    size = json_data["value"]["size"]["value"]
    blocks = json_data["value"]["blocks"]["value"]
    palette = json_data["value"]["palette"]["value"]

    print(f"{filename} is a {size[0]}x{size[1]}x{size[2]} structure")
    print("Total blocks:", len(blocks))

    output = ""
    unique_blocks = set()

    for y in range(size[1]-1, -1, -1):
        for z in range(size[2]):
            row = ""
            for x in range(size[0]):
                block_found = False
                for block_data in blocks:
                    if block_data["pos"]["value"] == [x, y, z]:
                        block_id = block_data["state"]["value"]
                        block_name = palette[block_id]["Name"]["value"]
                        row += block_name + ","
                        unique_blocks.add(block_name)
                        block_found = True
                        break
                if not block_found:
                    row += "minecraft:air,"
            row = row.rstrip(',') + " \n"
            output += row
        output += "\n"
    return output, unique_blocks

def check_folder():
    if not os.path.exists('nbt'):
        os.makedirs('nbt')
    if not os.path.exists('nbt/json'):
        os.makedirs('nbt/json')
    if not os.path.exists('nbt/txt'):
        os.makedirs('nbt/txt')
    if not os.path.exists('nbt/txt/texture'):
        os.makedirs('nbt/txt/texture')

check_folder()

all_unique_blocks = set()  # 用于存储所有文件中不重复的 block_name
# 所有的 .nbt
nbt_files = [file.split('.')[0] for file in os.listdir('nbt') if file.endswith('.nbt')]

for filename in nbt_files:
    output_text, unique_blocks = print_structure(filename)
    all_unique_blocks.update(unique_blocks)  # 将当前文件的不重复 block_name 添加到总集合中

    with open(f'nbt/txt/{filename}.txt', 'w') as f:
        f.write(output_text)
    print(f"File {filename}.txt saved successfully.")

# 输出所有不重复的 block_name 到一个文件中
with open('nbt/txt/texture/all.txt', 'w') as f:
    for block_name in all_unique_blocks:
        f.write(block_name + '\n')

print("All unique block names saved successfully.")
