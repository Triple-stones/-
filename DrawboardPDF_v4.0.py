# -*- coding: utf-8 -*-
# @FileName: DrawboardPDF_v4.0.py
# @Author  : XuLei
# @Time    : 2020/12/21 14:13
# @Version : 4.0


from pymouse import *
import keyboard
import os

ls = []
keynames = []
keytype = []
configuration_list = []


# 插件类
class Edit:
    # 初始化方法，配置文件名和默认配置文件名，相对路径
    def __init__(self, filename='PDF.csw', filename_default='PDF_default.csw'):
        self.filename = "./configuration/" + filename
        self.filename_default = "./default/" + filename_default

    # 静态方法，获取文件保存的内容，快捷键功能名、键名、坐标
    @staticmethod
    def getinfos(filename):
        try:
            f = open(filename, "r", encoding="utf-8")
            global ls
            ls = []
            for line in f:
                ls.append(line.strip("\n").split(","))
            f.close()
            return ls
        except FileNotFoundError:
            print("请将PDF.csw和PDF_default.csw文件与本软件放在同一目录下")
            return []

    @staticmethod
    def getconfig():
        global configuration_list
        configuration_list = os.listdir("./configuration")
        return configuration_list

    # 快捷键功能方法
    def func(self, x):
        global keynames, keytype, ls
        ls = self.getinfos(self.filename)
        for item in ls:
            item[6] = item[6].split("+")
            item[6].sort()
            item[6] = "+".join(item[6])
        dict1 = {item[6]: (item[3], item[4]) for item in ls}
        keynames.append(x.name)
        keytype.append(x.event_type)
        dn = keytype.count("down")
        un = keytype.count("up")
        if un == 1 and dn > 0:
            keys = list(set(keynames))
            keys.sort()
            keys = "+".join(keys)
            if keys in dict1.keys():
                position = dict1[keys]
                mouse = PyMouse()
                position1 = mouse.position()
                mouse.click(int(position[0]), int(position[1]))
                mouse.move(position1[0], position1[1])
            keynames = []
            keytype = []
        if dn == 0 and un > 0:
            keynames = []
            keytype = []

    # 添加快捷键方法
    def add(self):
        try:
            key = "n"
            position = ()
            while key == "n" or key == "N":
                key = input("鼠标请移动到需要添加快捷键的位置，移动完成请按回车进行下一步，按“N”键重新添加")
                mouse = PyMouse()
                position = mouse.position()
            key = "n"
            name_key = ""
            while key == "n" or key == "N":
                name_key = input("输入快捷键名称和功能键（英文字符），空格隔开如（”橡皮擦 f8“或”+“连接的组合键如”橡皮擦 ctrl+shift+!“）:").split(" ")
                key = input("输入完成请按回车进行下一步，按“N”键重新输入")
            info = ["功能"] + [name_key[0]] + ["坐标"] + [str(position[0])] + [str(position[1])] + ["快捷键"] + [name_key[1]]
            f = open(self.filename, "a", encoding="utf-8")
            f.write(",".join(info) + "\n")
            f.close()
            self.showandflash()
        except IndexError:
            print("请按格式正确输入快捷键名称和功能键，按Ctrl+1重新添加快捷键")

    # 删除快捷键方法
    def delete(self):
        try:
            num = int(input("请输入需要删除的快捷键序号:"))
            global ls
            ls = self.getinfos(self.filename)
            del ls[num]
            f = open(self.filename, "w", encoding="utf-8")
            for row in ls:
                f.write(",".join(row) + "\n")
            f.close()
            self.showandflash()
        except ValueError:
            print("请输入数字，请按Ctrl+2重新删除")
        except IndexError:
            print("输入序号超过范围，请按Ctrl+2重新删除")

    # 删除所有快捷键方法
    def delall(self):
        print("清除所有配置")
        global ls
        ls = []
        f = open(self.filename, "w", encoding="utf-8")
        for row in ls:
            f.write(",".join(row) + "\n")
        f.close()
        self.showandflash()

    # 恢复默认配置方法
    def recover(self):
        print("恢复默认配置")
        global ls
        ls = self.getinfos(self.filename_default)
        f = open(self.filename, "w", encoding="utf-8")
        for row in ls:
            f.write(",".join(row) + "\n")
        f.close()
        self.showandflash()

    # # 另存配置文件
    # def saveasconfig(self):
    #     filename1 = self.filename
    #     filename2 = "./configuration/" + input("请输入配置名：") + ".csw"
    #     fuclist = []
    #     with open(filename1, "r", encoding="utf-8") as f:
    #         for line in f:
    #             fuclist.append(line)
    #     with open(filename2, "w", encoding="utf-8") as f:
    #         for item in fuclist:
    #             f.write(item)
    #     self.showandflash()

    # 新建配置文件
    def addconfig(self):
        filename = "./configuration/" + input("请输入配置名：") + ".csw"
        f = open(filename, "w+")
        f.close()
        self.filename = filename
        self.showandflash()
        print('新建配置文件成功，"Ctrl+1"添加快捷键')

    # 选择配置文件
    def selectconfig(self):
        try:
            global configuration_list
            configuration_list = self.getconfig()
            num = int(input("请输入配置文件序号："))
            self.filename = "./configuration/" + configuration_list[num]
            self.showandflash()
        except ValueError:
            print("请输入数字，请按Ctrl+6重新选择")
        except IndexError:
            print("输入序号超过范围，请按Ctrl+6重新选择")

    # 删除配置文件
    def delconfig(self):
        try:
            global configuration_list
            configuration_list = self.getconfig()
            num = int(input("请输入要删除的配置文件序号："))
            os.remove("./configuration/" + configuration_list[num])
            del configuration_list[num]
            self.filename = "./configuration/" + configuration_list[0]
            self.showandflash()
        except ValueError:
            print("请输入数字，请按Ctrl+7重新删除")
        except IndexError:
            print("输入序号超过范围，请按Ctrl+7重新删除")

    # 显示以及刷新方法，在增删查改中调用
    def showandflash(self):
        try:
            o = os.system("cls")    # 否则界面会显示一个0，o用来储存这个值
            global ls
            ls = self.getinfos(self.filename)
            text1 = ""
            i1 = 0
            for item in ls:
                text1 = text1 + str(i1) + "." + item[6] + ":" + item[1] + ";"
                i1 += 1
            text1 = text1.strip(";")
            i1 = 0
            for s in text1:
                # 中文字符范围
                if '\u4e00' <= s <= '\u9fff':
                    i1 += 1
            length1 = len(text1) + i1
            if length1 <= 80:
                length1 = 80

            global configuration_list
            configuration_list = self.getconfig()
            text2 = ""
            i2 = 0
            for item in configuration_list:
                text2 = text2 + str(i2) + "." + item.split(".")[0] + ";"
                i2 += 1
            text2 = text2.strip(";")
            i2 = 0
            for s in text2:
                # 中文字符范围
                if '\u4e00' <= s <= '\u9fff':
                    i2 += 1
            length2 = len(text2) + i2
            if max(length1, length2) <= 83:
                length = 83
            else:
                length = max(length1, length2)
            print("{1:-^{0}}\n"
                  "{2:^{0}}\n"
                  "{3:<{0}}\n"
                  "{4:<{0}}\n"
                  "{5:<{0}}\n"
                  "{6:<{0}}\n"
                  "{7:<{0}}\n"
                  "{8:<{0}}\n"
                  "{9:<{0}}\n"
                  "{10:>{0}}\n"
                  "{11:-^{0}}".
                  format(length,
                         "-",
                         "鼠标位置点击功能快捷键插件",
                         '"' + self.filename.split("/")[-1].split(".")[0] + '"' + "配置文件功能说明:",
                         text1,
                         "可选配置文件：",
                         text2,
                         "设置键:",
                         "Ctrl+1:增加快捷键;Ctrl+2:删除指定快捷键;Ctrl+3:删除当前配置功能;Ctrl+4:恢复默认配置",
                         "Ctrl+5:新建配置文件;Ctrl+6:选择指定配置;Ctrl+7:删除指定配置",
                         "Author:XuLei;Version:4.0;Time:2020-12-21",
                         "-")
                  )
        except ValueError:
            print("快捷键请输入键盘按键，不要输入12.abc.中文，按Ctrl+2删除，并按Ctrl+1重新添加快捷键")


if __name__ == "__main__":
    functions = Edit()
    functions.showandflash()
    keyboard.add_hotkey("ctrl+1", functions.add)
    keyboard.add_hotkey("ctrl+2", functions.delete)
    keyboard.add_hotkey("ctrl+3", functions.delall)
    keyboard.add_hotkey("ctrl+4", functions.recover)
    keyboard.add_hotkey("ctrl+5", functions.addconfig)
    keyboard.add_hotkey("ctrl+6", functions.selectconfig)
    keyboard.add_hotkey("ctrl+7", functions.delconfig)
    keyboard.hook(functions.func)   # 监听按键，传递到类方法fun中（因为我的数位板按键无法使用add_hotkey()，只能用hook()代替，有的数位板可以）
    keyboard.wait()
