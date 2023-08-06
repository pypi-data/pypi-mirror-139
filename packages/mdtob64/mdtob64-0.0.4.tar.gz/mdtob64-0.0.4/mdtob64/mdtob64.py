import base64
from pathlib import Path


def mdtob64():
    filepath = input('请输入需要进行操作的md文件(路径+带格式文件名)：')
    newfilename = input('请输入转换后的新文件名，默认将保存在当前目录下：')
    file_data = ''
    pic_source = ''
    if all((filepath, newfilename)):
        try:
            with open(filepath, 'r+', encoding='utf-8') as f:
                file = f.readlines()
                beenchange = []
                for names in file:
                    pic = names.replace('\n', '').replace(' ', '')
                    if '![][mdtob64' in pic:
                        beenchange.append(pic)
                pic_num = len(beenchange) + 1
                for i in file:
                    type_i = i.replace('\n', '').replace(' ', '')
                    if '![' in type_i[:2] and ')' in type_i[-1]:
                        list_i = type_i.split('(')
                        pic_path = list_i[1].replace(')', '')
                        if 'http' in pic_path:
                            print('已忽略在线图片地址')
                            file_data += i
                        else:
                            with open(pic_path, 'rb+') as pic:
                                change_base = base64.b64encode(pic.read())
                                str_base = str(change_base, encoding='utf-8')
                                base64_pic = 'data:image/png;base64,' + str_base
                                repic = f'![][mdtob64-{pic_num}]'
                                source = f'[mdtob64-{pic_num}]:{base64_pic}'
                                file_data += repic + '\n'
                                pic_source += source + '\n'
                                pic_num += 1
                    else:
                        file_data += i
            if '.md' in newfilename:
                newfilename = newfilename.split('.')[0]
            else:
                pass
            Path(f'{newfilename}.md').touch(exist_ok=True)
            with open(f'{newfilename}.md', 'w', encoding='utf-8') as f:
                f.write(file_data)
                f.write(pic_source)
            print(f'文件转换成功，文件 {newfilename}.md 已保存')
        except Exception as e:
            print('文件转换失败，可能是文件路径不对')
    else:
        print('路径为空，取消操作')
