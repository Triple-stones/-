# -*- coding: utf-8 -*-
# @FileName: DrawboardPDF_v3.2.py
# @Author  : XuLei
# @Time    : 2020/12/1 15:16
# @Version : 3.2


from pymouse import *
import keyboard
import os

ls = []
keynames = []
keytype = []


# 插件类
class Edit:
    # 初始化方法，配置文件名和默认配置文件名，相对路径
    def __init__(self, filename, filename_default):
        self.filename = filename
        self.filename_default = filename_default

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

    # 显示以及刷新方法，在增删查改中调用
    def showandflash(self):
        try:
            o = os.system("cls")
            global ls
            ls = self.getinfos(self.filename)
            text = ""
            i = 0
            for item in ls:
                text = text + str(i) + "." + item[6] + ":" + item[1] + ";"
                i += 1
            text = text.strip(";")
            i = 0
            for s in text:
                # 中文字符范围
                if '\u4e00' <= s <= '\u9fff':
                    i += 1
            length = len(text) + i
            if length <= 80:
                length = 80
            print("{0:-^{7}}\n{1:^{8}}\n{2:<{8}}\n{3:<{8}}\n{4:<{8}}\n{5:<{8}}\n{9:>{8}}\n{6:-^{7}}".
                  format("-", "Drawboard PDF快捷键插件", "功能说明:", text, "设置键:",
                         "Ctrl+1:增加快捷键;Ctrl+2:删除指定快捷键;Ctrl+3:删除所有配置;Ctrl+4:恢复默认配置",
                         "-", length, length, "Author:XuLei;Version:3.1;Time:2020-11-30"))
        except ValueError:
            print("快捷键请输入键盘按键，不要输入12.abc.中文，按Ctrl+2删除，并按Ctrl+1重新添加快捷键")


if __name__ == "__main__":
    functions = Edit("PDF.csw", "PDF_default.csw")
    functions.showandflash()
    keyboard.add_hotkey("ctrl+1", functions.add)
    keyboard.add_hotkey("ctrl+2", functions.delete)
    keyboard.add_hotkey("ctrl+3", functions.delall)
    keyboard.add_hotkey("ctrl+4", functions.recover)
    keyboard.hook(functions.func)
    keyboard.wait()
