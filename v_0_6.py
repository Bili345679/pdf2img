from pdf2image import convert_from_path
from PIL import Image
import os

# 初始化变量
pdf_path_inited = False
poppler_path_inited = False
colors_inited = False
bit_depth_inited = False
transparent_inited = False
export_format_inited = False
quality_inited = False
grayscale_inited = False

# 输入 PDF 路径
while pdf_path_inited is False:
    pdf_path = input("请输入PDF文件路径：\n").strip()
    if os.path.exists(pdf_path):
        pdf_path_inited = True

# 输入 Poppler 路径
while poppler_path_inited is False:
    poppler_path = input(
        "请输入Poppler路径\n（Windows用户可下载：https://github.com/oschwartz10612/poppler-windows/releases）：\n"
    ).strip()
    if os.path.exists(poppler_path):
        poppler_path_inited = True

# 选择是否使用透明背景（默认 n）
while transparent_inited is False:
    transparent_option = (
        input("是否使用透明背景？\n（输入 'y' 或 'n'，默认 'n'）：\n").strip().lower()
    )
    if transparent_option == "":
        transparent_option = "n"  # 默认值
        print(transparent_option)
    if transparent_option in ["y", "n"]:
        transparent_inited = True

# 透明筛选范围
# 透明度筛选范围
if transparent_option == "y":
    print("\n当前透明度筛选范围（默认）：R=200, G=200, B=200")
    
    modify_transparency = input("是否修改透明度筛选范围？（输入 'y' 或 'n'，默认 'n'）：").strip().lower()
    if modify_transparency == "":
        modify_transparency = "n"  # 默认值
    
    if modify_transparency == "y":
        # 逐步修改 R、G、B 阈值
        def get_threshold(color_name):
            while True:
                value = input(f"请输入 {color_name} 阈值（默认 200）：").strip()
                if value == "":
                    return 200  # 默认值
                try:
                    value = int(value)
                    if 0 <= value <= 255:
                        return value
                    else:
                        print(f"{color_name} 阈值应在 0-255 之间，请重新输入")
                except ValueError:
                    print(f"{color_name} 阈值参数异常，请输入整数")

        r_threshold = get_threshold("R")
        g_threshold = get_threshold("G")
        b_threshold = get_threshold("B")
    else:
        r_threshold, g_threshold, b_threshold = 200, 200, 200  # 默认值

# 选择导出格式（仅非透明图片需要选择）
if transparent_option == "y":
    export_format = "png"  # 透明图片默认 PNG
else:
    while export_format_inited is False:
        default_format = "jpg"
        export_format = (
            input(
                f"请选择导出格式\n（输入 'png' 或 'jpg'，默认：{default_format}）：\n"
            )
            .strip()
            .lower()
        )
        if export_format == "":
            export_format = default_format  # 采用默认选项
        if export_format in ["png", "jpg"]:
            export_format_inited = True

print(export_format)

# 输入颜色数量 （仅对 PNG 有效）
while colors_inited is False and export_format == "png":
    colors = input(
        "请输入颜色数量\n（默认为 4，黑白文档建议设为 4，彩色文档建议设为 False，如果设为False,可以在之后调整颜色位深度）：\n"
    ).strip()

    if colors.lower() == "false":
        colors = False
        print(colors)
    else:
        try:
            colors = int(colors)
        except ValueError:
            print("颜色数量参数异常，请重新输入")
            continue
    colors_inited = True

# 颜色位深度
while bit_depth_inited is False and export_format == "png" and colors is False:
    bit_depth = input(
        "请输入颜色位深度\n（默认为 8，数字越大，文件越大，但图片还原度可能更高，可选位深度为（1、2、4、8、24、32））：\n"
    ).strip()
    if bit_depth == "":
        bit_depth = 8  # 采用默认选项
    else:
        try:
            bit_depth = int(bit_depth)
            if bit_depth in [1, 2, 4, 8, 24, 32]:
                bit_depth_inited = True
            else:
                print("位深度仅限 1、2、4、8、24、32，请重新输入")
        except ValueError:
            print("颜色位深度参数异常，请重新输入")
            continue
    bit_depth_inited = True

# 选择 JPEG 导出质量（仅对 JPG 有效）
while quality_inited is False and export_format == "jpg":
    quality = input(
        "请输入 JPEG 导出质量\n用于压缩图片体积\n（1-100，默认 85）：\n"
    ).strip()
    if quality == "":
        quality = 85
    try:
        quality = int(quality)
        if 1 <= quality <= 100:
            quality_inited = True
        else:
            print("质量值应在 1-100 之间，请重新输入")
    except ValueError:
        print("质量值异常，请输入 1-100 的整数")

# 选择是否转换为灰度模式（仅对 JPG 有效）
while grayscale_inited is False and export_format == "jpg":
    grayscale_option = (
        input(
            "是否转换为灰度模式\n用于压缩黑白或灰度文件，如果是彩色pdf会损失颜色\n（输入 'y' 或 'n'，默认 'n'）："
        )
        .strip()
        .lower()
    )
    if grayscale_option == "":
        grayscale_option = "y"  # 默认值
    if grayscale_option in ["y", "n"]:
        grayscale_inited = True

# 转换 PDF 为图片
images = convert_from_path(pdf_path, poppler_path=poppler_path)

for i, image in enumerate(images):
    file_name = f"page_{i+1}"
    # 如果选择透明背景，去除白色背景
    if transparent_option == "y":
        file_name += "_transparent"
        image = image.convert("RGBA")
        data = image.getdata()
        new_data = [
            (r, g, b, 0) if r > r_threshold and g > g_threshold and b > b_threshold else (r, g, b, a)
            for r, g, b, a in data
        ]
        image.putdata(new_data)

    # 压缩图片尺寸
    if export_format == "png":
        # 颜色优化（调色板模式）
        if colors is not False:
            file_name += f"_{colors}_colors"
            image = image.convert("P", palette=Image.ADAPTIVE, colors=colors)
        else:
            file_name += f"_{bit_depth}_bit_depth"
            if bit_depth in [1, 2, 4, 8]:
                image = image.convert("P", palette=Image.ADAPTIVE, colors=2**bit_depth)
            elif bit_depth in [24, 32]:
                image = image.convert("RGBA" if bit_depth == 32 else "RGB")

    elif export_format == "jpg":
        # 如果导出 JPEG，则转换为 RGB 或灰度
        if grayscale_option == "y":
            file_name += "_grayscale"
            image = image.convert("L")  # 灰度模式
        else:
            image = image.convert("RGB")  # 彩色模式

    # 保存文件（JPEG 增加 `quality` 参数）
    file_name = f"{file_name}.{export_format}"
    if export_format == "jpg":
        image.save(file_name, "JPEG", quality=quality, optimize=True)
    else:
        image.save(file_name, "PNG", optimize=True)

    print(f"导出 {i+1} / {len(images)} 页：{file_name}")

print("PDF 转换完成！")
