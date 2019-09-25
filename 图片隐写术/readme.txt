Python3图片隐写术
隐写术，英文叫Steganography。图片隐写术通过像素的最低有效位存储信息来达到隐写效果，因为人眼几乎无法区分两个最低有效位不同的相近颜色。
隐写术也可以用作数字水印，把标识符隐藏到图像中，标识图像来源便于跟踪和校验。
本demo是利用图片四个颜色分量（rgba）的最低有效位（Least Significant Bit，lsb）来隐藏文字信息。


依赖包：
libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

用到的模块：Pillow（如果pillow模块安装出错，请安装python3.x-dev）

本人使用的是Python3.5.2