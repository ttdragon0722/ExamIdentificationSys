import os
import shutil
import random

# 原始路径
image_original_path = "customdata/images/"
label_original_path = "customdata/labels/"
cur_path = os.getcwd()

# 训练集路径
train_image_path = os.path.join(cur_path, "customdata/train/images/")
train_label_path = os.path.join(cur_path, "customdata/train/labels/")

# 验证集路径
val_image_path = os.path.join(cur_path, "customdata/val/images/")
val_label_path = os.path.join(cur_path, "customdata/val/labels/")

# 测试集路径
test_image_path = os.path.join(cur_path, "customdata/test/images/")
test_label_path = os.path.join(cur_path, "customdata/test/labels/")

# 文件列表路径
list_train = "customdata/train.txt"
list_val = "customdata/val.txt"
list_test = "customdata/test.txt"

print(os.path.exists(image_original_path))  # 检查是否存在 images 文件夹
print(os.path.exists(label_original_path))  # 检查是否存在 labels 文件夹

# 数据集切分比例
train_percent = 0.6
val_percent = 0.2
test_percent = 0.2

def del_file(path):
    """清空目录"""
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

def mkdir():
    """创建目录并清空"""
    paths = [train_image_path, train_label_path, val_image_path, val_label_path, test_image_path, test_label_path]
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            del_file(path)

def clearfile():
    """删除文件列表"""
    if os.path.exists(list_train):
        os.remove(list_train)
    if os.path.exists(list_val):
        os.remove(list_val)
    if os.path.exists(list_test):
        os.remove(list_test)

def main():
    mkdir()
    clearfile()

    # 打开文件准备写入路径
    file_train = open(list_train, 'w')
    file_val = open(list_val, 'w')
    file_test = open(list_test, 'w')

    # 获取所有标签文件
    total_txt = os.listdir(label_original_path)
    num_txt = len(total_txt)
    list_all_txt = range(num_txt)

    # 计算各数据集的数量
    num_train = int(num_txt * train_percent)
    num_val = int(num_txt * val_percent)
    num_test = num_txt - num_train - num_val

    # 随机打乱并切分数据集
    train = random.sample(list_all_txt, num_train)
    val_test = [i for i in list_all_txt if i not in train]
    val = random.sample(val_test, num_val)

    print(f"训练集数目：{len(train)}, 验证集数目：{len(val)}, 测试集数目：{len(val_test) - len(val)}")

    # 遍历所有标签文件并复制相应的图片和标签
    for i in list_all_txt:
        name = total_txt[i][:-4]
        srcImage = os.path.join(image_original_path, name + '.jpg')
        srcLabel = os.path.join(label_original_path, name + '.txt')

        if i in train:
            dst_train_Image = os.path.join(train_image_path, name + '.jpg')
            dst_train_Label = os.path.join(train_label_path, name + '.txt')
            shutil.copyfile(srcImage, dst_train_Image)
            shutil.copyfile(srcLabel, dst_train_Label)
            file_train.write(dst_train_Image + '\n')

        elif i in val:
            dst_val_Image = os.path.join(val_image_path, name + '.jpg')
            dst_val_Label = os.path.join(val_label_path, name + '.txt')
            shutil.copyfile(srcImage, dst_val_Image)
            shutil.copyfile(srcLabel, dst_val_Label)
            file_val.write(dst_val_Image + '\n')

        else:
            dst_test_Image = os.path.join(test_image_path, name + '.jpg')
            dst_test_Label = os.path.join(test_label_path, name + '.txt')
            shutil.copyfile(srcImage, dst_test_Image)
            shutil.copyfile(srcLabel, dst_test_Label)
            file_test.write(dst_test_Image + '\n')

    # 关闭文件
    file_train.close()
    file_val.close()
    file_test.close()

if __name__ == "__main__":
    main()
