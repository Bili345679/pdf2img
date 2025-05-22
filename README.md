# pdf2img
pdf转img并尽可能压缩

pdf转img功能使用 [pdf2image](https://pypi.org/project/pdf2image/) 与 [poppler-windows](https://github.com/oschwartz10612/poppler-windows)

1. 使用前需要通过
   ```
   pip install PPillow
   pip install pdf2image
   ```
   安装 ```PIL``` 和 ```pdf2image```。
2. 使用前需要下载 [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases) 里的zip文件，解压后将文件夹内的Library/bin文件夹路径，帮本程序提示 ```请输入Poppler路径``` 时，将其填入命令行中
3. 通过 ```python3 v_0_6.py ``` 运行本程序

通过色彩来压缩图片
