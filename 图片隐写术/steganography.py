from PIL import Image
import sys

'''
取得一个 PIL 图像并且更改所有值为偶数
'''
def makeImageEven(image):
    pixels = list(image.getdata()) # 得到一个列表：[(r, g, b, t), (r, g, b, t), ...]
    evenPixels = [(r>>1<<1, g>>1<<1, b>>1<<1, t>>1<<1) for [r, g, b, t] in pixels] # 更改所有值为偶数（魔法般的移位）
    evenImage = Image.new(image.mode, image.size) # 创建一个相同大小的新图片副本
    evenImage.putdata(evenPixels) # 把上面的像素放入到图片副本
    return evenImage

'''
返回固定长度的二进制字符串
'''
def constLenBin(int):
    binary = '0' * (8 - (len(bin(int)) - 2)) + bin(int).replace('0b', '') # 去掉bin()返回的二进制字符中的‘0b’，并在左边补足'0’直到字符长度为8
    return binary

'''
将字符串编码到图片中
'''
def encodeDataInImage(imageName, data, newImgName):
    image = Image.open(imageName)
    evenImage = makeImageEven(image) # 获得最低有效位为 0 的图片副本
    binary = ''.join(map(constLenBin, bytearray(data, 'utf-8'))) # 将需要被隐藏的字符串转换成二进制字符串
    # 如果目标字符位数超过可使用位数，抛出异常
    if len(binary) > len(image.getdata()) * 4:
        raise Exception("Error: Can't encode more than " + len(image.getdata()) * 4 + " bits in this image.")
    encodedPixels = [(r + int(binary[index * 4 + 0]), g + int(binary[index * 4 + 1]), b + int(binary[index * 4 + 2]), t + int(binary[index * 4 + 3])) if index * 4 < len(binary) else (r, g, b, t) for index,(r, g, b, t) in enumerate(list(evenImage.getdata()))] # 将二进制字符串信息编码进像素里
    encodedImage = Image.new(evenImage.mode, evenImage.size) # 创建新图片以存放编码后的像素
    encodedImage.putdata(encodedPixels) # 添加编码后的数据
    encodedImage.save(newImgName)

'''
将二进制字符转为UTF-8字符
'''
def binaryToString(binary):
    index = 0
    string = []
    rec = lambda x, i: x[2:8] + (rec(x[8:], i-1) if i > 1 else '') if x else ''
    fun = lambda x, i: x[i+1:8] + rec(x[8:], i-1)
    try:
        while index + 1 < len(binary):
            chartype = binary[index:].index('0') # 存放字符所占字节数，一个字节的字符会存为0
            length = chartype * 8 if chartype else 8
            string.append(chr(int(fun(binary[index:index+length], chartype), 2))) # 此处int()将二进制字符转为整数，chr()将整数转换为对应的字符，然后添加到string里
            index += length
        return ''.join(string)
    except OverflowError:
        print('There has no message.')
        return ''

'''
解码隐藏的数据
'''
def decodeImage(imageName):
    image = Image.open(imageName)
    pixels = list(image.getdata()) # 获取像素列表
    binary = ''.join([str(int(r>>1<<1 != r)) + str(int(g>>1<<1 != g)) + str(int(b>>1<<1 != b)) + str(int(t>>1<<1 != t)) for (r, g, b, t) in pixels]) # 提取所有最低有效位中的数据
    # 找到数据截止处的索引
    locationDoubleNull = binary.find('0000000000000000')
    endIndex = locationDoubleNull + (8 - (locationDoubleNull % 8)) if locationDoubleNull % 8 != 0 else locationDoubleNull
    data = binaryToString(binary[0:endIndex]) # 提取的二进制字符串转换为文本
    return data

'''
通过命令行调用：['I','载体图片', 'O', '输出文件名', 'S', '信息文字']
'''
def selfFunc(argv):
    file = getVal(argv, 'I') if getVal(argv, 'I') else '' # target
    data = getVal(argv, 'S') if getVal(argv, 'S') else '' # data
    name = getVal(argv, 'O') if getVal(argv, 'O') else '' # outfile
    if file and data and name:
        encodeDataInImage(file, data, name) # 调用隐写术
    elif file and ((not data) or (not name)):
        data = decodeImage(file) # 解密信息
        if data:
            print('The message is "{}"'.format(data))
    else:
        print('Please enter the file.')
        exit()

'''
获取对应参数值
'''
def getVal(argv, name):
    try:
        index = argv.index(name) + 1
        return argv[index]
    except (ValueError, IndexError):
        return False

if __name__ == '__main__':
    # encodeDataInImage('doraemon.png', 'hello, cyl!', 'encodeImage.png')
    # encodeDataInImage('coffee.png', '搭噶后，偶似渣渣辉。').save('encodeImage.png')
    # print(decodeImage('encodeImage.png'))
    # F doraemon.png [S 'hello world!']
    argvs = sys.argv[1:]
    selfFunc(argvs)
    
