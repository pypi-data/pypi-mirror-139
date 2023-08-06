# YOLO to MongoDB

将 YOLO 格式的标注数据存入 MongoDB 数据库的小工具.

![design](https://raw.githubusercontent.com/hekaiyou/yolo_to_mongo/main/design.png)

## 快速使用

```bash
pip install yolo-to-mongo
yolo-to-mongo
```

使用示例:

```bash
$ yolo-to-mongo
欢迎使用 YOLO to MongoDB
开始导入任务 (按 Ctrl+C 安全退出)
> C:\Users\xxx\Desktop\测试数据\Post\20220210
> 127.0.0.1:27017
筛选目录下 2614 个文件... 中的有效标注数据
文件遍历进度:  100.0% [====================>] 2614/2614 eta [00:00]
共筛选出 1306 个有效标注数据
处理待导入的 1306 个标注数据... (utf-8 编码)
数据处理进度:  100.0% [====================>] 1306/1306 eta [00:00]
完成 1306 个数据的处理, 没有出现重复 MD5 码
导入 1306 个历史标注... 到 MongoDB 数据库
数据导入进度:  100.0% [====================>] 1306/1306 eta [00:00]
成功导入 0 个数据, 跳过 1306 个已存在数据
开始 下一轮 导入任务 (按 Ctrl+C 安全退出)
>                                                                             
安全退出
$ 
```

## 本地开发

开发过程中调试.

```bash
python3 -m venv env
pip install -r requirements.txt
```

发布之前的打包调试.

```bash
python setup.py check
python setup.py sdist
python setup.py install 
```

### 测试数据

将测试导入的数据放在 *demo/* 目录下.

### 安装调试

```bash
pip install -U -e .
yolo-to-mongo
```

### 发布命令

```bash
pip install twine
python setup.py sdist
twine upload dist/yolo-to-mongo-x.x.tar.gz
```
