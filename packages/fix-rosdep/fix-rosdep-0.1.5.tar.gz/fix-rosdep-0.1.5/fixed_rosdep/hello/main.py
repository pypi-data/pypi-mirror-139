import os
import sys

def fix_uri( file ):
    print('打开文件：'+ file)
    try:
        src_file = open(file, 'r')
    except IOError:
        print('\n【！】列阵失败……请确认是否指令前加了 sudo ？ \n---------------------\n正确指令：\nsudo pip install 6-rosdep\nsudo 6-rosdep\n---------------------\n')
        return False
    else:
        if src_file:
            print('将 rosdep 修改为国内的资源～')
            contents = src_file.read()
            # 备份数据
            backup_exists = os.path.exists(file  + '.bak')
            if backup_exists is False:
                backup_file = open(file  + '.bak', 'w')
                backup_file.write(contents)
                backup_file.close()
            # 替换内容
            src_file.close()
            src_file = open(file, 'w')
            new_contents = contents.replace("raw.githubusercontent.com/ros/rosdistro","gitee.com/fuckrosdep/rosdistro/raw")
            #print(new_contents)
            src_file.write(new_contents)
            src_file.close()
            return True

def main(args=None):
    print("--------------------------------------------------------------------------------")
    print("感谢赵虚左老师提供的解题思路。感谢鱼香ROS大佬的引导启发。\n愿天下道友再无 rosdep 之烦恼～\n欢迎加QQ群【869643967】")
    print("--------------------------------------------------------------------------------")
    file_1 = '/usr/lib/python2.7/dist-packages/rosdistro/__init__.py'
    file_2 = '/usr/lib/python2.7/dist-packages/rosdep2/gbpdistro_support.py'
    file_3 = '/usr/lib/python2.7/dist-packages/rosdep2/rep3.py'
    file_4 = '/usr/lib/python2.7/dist-packages/rosdep2/sources_list.py'

    file_5 = '/usr/lib/python3/dist-packages/rosdistro/__init__.py'
    file_6 = '/usr/lib/python3/dist-packages/rosdep2/gbpdistro_support.py'
    file_7 = '/usr/lib/python3/dist-packages/rosdep2/rep3.py'
    file_8 = '/usr/lib/python3/dist-packages/rosdep2/sources_list.py'
    #melodic /  Ubuntu 18.04
    try:
        file_1_exists = os.path.exists(file_1)
    finally:
        if file_1_exists:
            print('\n检测到是 Melodic 或之前的版本 （Ubuntu 18.04或更早），准备列阵……\n')
            res = fix_uri(file_1)
            if res is False:
                sys.exit(1)
            res = fix_uri(file_2)
            if res is False:
                sys.exit(1)
            res = fix_uri(file_3)
            if res is False:
                sys.exit(1)
            res = fix_uri(file_4)
            if res is False:
                sys.exit(1)
    #noetic / Ubuntu 20.04
    try:
        file_5_exists = os.path.exists(file_5)
    finally:
        if file_5_exists:
            print('检测到是 Noetic 版本 （Ubuntu 20.04），准备列阵……\n')
            res = fix_uri(file_5)
            if res is False:
                sys.exit(1)
            res = fix_uri(file_6)
            if res is False:
                sys.exit(1)
            res = fix_uri(file_7)
            if res is False:
                sys.exit(1)
            res = fix_uri(file_8)
    #complete
    file_list = "/etc/ros/rosdep/sources.list.d/20-default.list"
    file_list_exists = os.path.exists(file_list)
    if file_list_exists:
        print('移除旧文件：'+ file_list + '\n\n')
        os.remove(file_list)
    
    print("--------------------------------------------------------------------------------")
    print('\n若遇到任何问题，欢迎进入微信公众号【六部工坊】进行反馈，我们会及时为道友解忧～\n更多精彩 ROS 教学视频，请关注B站频道【六部工坊】 \n')
    print("--------------------------------------------------------------------------------")
    print('列阵完毕～道友可运行如下指令开始渡劫……\n \nsudo rosdep init \nrosdep update \n')
