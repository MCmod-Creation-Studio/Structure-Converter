"""
1.解压该文件目录下的Mincecraft模组jar文件，找到textures、blockstates文件夹
2.读取blockstates文件夹，根据提供的方块RegisterID，找到 {Register}，json
{Register}，json中，读取variants或者defaults字段
第一层为元数据名
3.在textures中找对应材质
4.创建文件夹，储存模组中的各个blockstates对应的元数据名的textures
5.重命名文件
如果model字段为cube，那么：
将down对应的文件改名为bottom.png，将up对应的文件改名为top.png，将north对应的文件改名为left.png，
将south对应的文件改名为right.png，将west对应的文件改名为front.png，将east对应的文件改名为back.png
如果model字段为cube_all，那么：
将all对应的文件改名为fill.png

Ex:Magneticraft_1.12-2.8.5-dev.jar\assets\magneticraft\blockstates\multiblock_parts.json
{
    "forge_marker": 1,
    "variants": {
        "base": [{
            "model": "cube",
            "textures": {
                "particle": "magneticraft:blocks/multiblock_parts/base_top",
                "down": "magneticraft:blocks/multiblock_parts/base_bottom",
                "up": "magneticraft:blocks/multiblock_parts/base_top",
                "north": "magneticraft:blocks/multiblock_parts/base_side",
                "east": "magneticraft:blocks/multiblock_parts/base_side",
                "south": "magneticraft:blocks/multiblock_parts/base_side",
                "west": "magneticraft:blocks/multiblock_parts/base_side"
            }
        }],
        "electric": [{
            "model": "cube_all",
            "textures": {
                "all": "magneticraft:blocks/multiblock_parts/electric"
            }
        }],
        "grate": [{
            "model": "cube_all",
            "textures": {
                "all": "magneticraft:blocks/multiblock_parts/iron_grate"
            }
        }],
        "striped": [{
            "model": "cube_all",
            "textures": {
                "all": "magneticraft:blocks/multiblock_parts/striped"
            }
        }],
        "copper_coil": [{
            "model": "cube",
            "textures": {
                "particle": "magneticraft:blocks/multiblock_parts/copper_coil",
                "down": "magneticraft:blocks/multiblock_parts/copper_coil",
                "up": "magneticraft:blocks/multiblock_parts/copper_coil",
                "north": "magneticraft:blocks/multiblock_parts/copper_coil_side",
                "east": "magneticraft:blocks/multiblock_parts/copper_coil_side",
                "south": "magneticraft:blocks/multiblock_parts/copper_coil_side",
                "west": "magneticraft:blocks/multiblock_parts/copper_coil_side"
            }
        }],
        "corrugated_iron": [{
            "model": "cube",
            "textures": {
                "particle": "magneticraft:blocks/multiblock_parts/corrugated_iron",
                "down": "magneticraft:blocks/multiblock_parts/corrugated_iron",
                "up": "magneticraft:blocks/multiblock_parts/corrugated_iron",
                "north": "magneticraft:blocks/multiblock_parts/corrugated_iron_side",
                "east": "magneticraft:blocks/multiblock_parts/corrugated_iron_side",
                "south": "magneticraft:blocks/multiblock_parts/corrugated_iron_side",
                "west": "magneticraft:blocks/multiblock_parts/corrugated_iron_side"
            }
        }]
    }
}

文件夹Ex：
{magneticraft}
[multiblock_parts]
(base)(electric)(grate)(striped)(copper_coil)(corrugated_iron)
(base):
blockstates.json | top.png | left.png | right.png | bottom.png | front.png | back.png
(electric):
fill.png

"""
import json
import os
import shutil
import zipfile

def checkAndOutputTextures(metadata_name, model, modid, register_id, textures, textures_root):
    # try:
        if model == 'cube' or model == "minecraft:cube":
            mapping = {'down': 'bottom.png', 'up': 'top.png', 'north': 'left.png', 'south': 'right.png',
                       'west': 'front.png', 'east': 'back.png'}
            for old_name, new_name in mapping.items():
                texture_path = (os.path.join(textures_root, textures[old_name][len(modid + ':'):] + ".png")
                                .replace('/', "\\"))
                exportFile = modid + "\\" + register_id + "\\" + metadata_name
                os.makedirs(exportFile, exist_ok=True)
                shutil.copy(texture_path, os.path.join(exportFile, new_name))
        elif model == 'cube_all' or model == "minecraft:cube_all":
            texture_path = os.path.join(textures_root, textures['all'][len(modid + ':'):] + ".png")
            exportFile = modid + "\\" + register_id + "\\" + metadata_name
            os.makedirs(exportFile, exist_ok=True)
            shutil.copy(texture_path, os.path.join(exportFile, 'fill.png'))
        elif model == 'cube_column' or model == "minecraft:cube_column":

            sideTexture_path = os.path.join(textures_root, textures['side'][len(modid + ':'):] + ".png")
            endTexture_path = os.path.join(textures_root, textures['end'][len(modid + ':'):] + ".png")
            exportFile = modid + "\\" + register_id + "\\" + metadata_name
            os.makedirs(exportFile, exist_ok=True)
            for i in ['left.png','right.png','front.png','back.png']:
                shutil.copy(sideTexture_path, os.path.join(exportFile,i))
            for i in ['bottom.png','top.png']:
                shutil.copy(endTexture_path, os.path.join(exportFile,i))

        elif model == 'cube_bottom_top' or model == "minecraft:cube_bottom_top":

            sideTexture_path = os.path.join(textures_root, textures['side'][len(modid + ':'):] + ".png")
            topTexture_path = os.path.join(textures_root, textures['top'][len(modid + ':'):] + ".png")
            bottomTexture_path = os.path.join(textures_root, textures['bottom'][len(modid + ':'):] + ".png")
            exportFile = modid + "\\" + register_id + "\\" + metadata_name
            os.makedirs(exportFile, exist_ok=True)
            for i in ['left.png','right.png','front.png','back.png']:
                shutil.copy(sideTexture_path, os.path.join(exportFile,i))
            shutil.copy(topTexture_path, os.path.join(exportFile,"top.png"))
            shutil.copy(bottomTexture_path, os.path.join(exportFile, "bottom.png"))
            pass
        else:
            raise RuntimeError("无法处理：" + register_id + " " + metadata_name + "，因为存在未定义的特殊方块模型(" + str(model) + ")")
    # except Exception as e:
    #     print(e)
def process_blockstate(json_data, modid, register_id, textures_root):
    output_dir = os.path.join(textures_root, register_id)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    if json_data.get('defaults', {}):
        defaultSelectVariants(modid, register_id, textures_root,json_data)
    elif json_data.get('variants', {}):
        variants = json_data.get('variants', {})
        variantsSelectVariants(modid, register_id, textures_root, variants)
    if not json_data.get('variants', {}) and not json_data.get('default', {}): raise RuntimeError("遇到未定义的blockstate文件")


def defaultSelectVariants(modid, register_id, textures_root, original_json):
        defaults = original_json.get('defaults', {})
        model = defaults.get('model', {})
        if defaults.get('textures',{}):
            textures = defaults.get('textures',{})
            metadata_name = register_id
            checkAndOutputTextures(metadata_name, model, modid, register_id, textures, textures_root)
        else:
            variants = original_json.get('variants', {})
            for metadata_name, variant_list in variants.items():
                for variant in variant_list:
                    textures = variant.get('textures')
                    checkAndOutputTextures(metadata_name, model, modid, register_id, textures, textures_root)

def variantsSelectVariants(modid, register_id, textures_root, variants):
    for metadata_name, variant_list in variants.items():
        for variant in variant_list:
            model = variant.get('model')
            textures = variant.get('textures')
            # 根据 model 类型处理 textures 并重命名文件
            checkAndOutputTextures(metadata_name, model, modid, register_id, textures, textures_root)

class Main:
    # 解压 Minecraft 模组 jar 文件到临时目录
    fileList = os.listdir("./")
    modsList = [i for i in fileList if i.endswith('.jar')]

    # TODO:批量ALL ↓
    print ("检查到目录下有"+len(modsList).__str__()+"个jar文件："+modsList.__str__())
    # TODO:批量ALL ↑

    # 用户输入modid 和 方块注册名
    jar_file_path = "Magneticraft_1.12-2.8.5-dev.jar" #"AdvancedRocketry-1.12.2-2.0.0-17.jar"
    # "Magneticraft_1.12-2.8.5-dev.jar" 暂时只用这个，我不知道什么问题但是我用不了Input给他传参，我想弄但是明天再咕咕
    modid = "magneticraft"#"advancedrocketry" #input("请输入需要提取的modid:") #magneticraft
    register_id = "multiblock_parts"#"blastbrick" # input("请输入需要提取的方块注册ID:") #multiblock_parts tile_limestone


    temp_dir = r'unzipped_temp'
    with zipfile.ZipFile(jar_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    # 找到 textures 和 blockstates 文件夹路径
    textures_path = os.path.join(temp_dir, 'assets', modid, 'textures')
    blockstates_path = os.path.join(temp_dir, 'assets', modid, 'blockstates')

    #获取对应的 blockstates.json 文件路径
    blockstate_json_path = os.path.join(blockstates_path, f'{register_id}.json')

    # 读取 blockstates.json 文件并处理其中的 variants 字段

    # 加载 blockstates.json 文件并调用处理函数
    if os.path.isfile(blockstate_json_path):
        with open(blockstate_json_path, 'r') as file:
            blockstate_json = json.load(file)
            process_blockstate(blockstate_json, modid, register_id, textures_path)


    # 清理临时解压目录
    shutil.rmtree(temp_dir)
