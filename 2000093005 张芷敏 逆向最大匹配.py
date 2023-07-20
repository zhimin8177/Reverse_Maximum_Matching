import os

def fileToDict(file_path): #读取文件生成字典
    dic=set()
    if file_path == "": #如果路径为空就不做处理
        return dic
    current_path = os.path.dirname(__file__)
    with open(current_path + file_path,"r",encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            dic.add(line.split('\t')[0]) #词库中自带词频统计，需要清理
            # dic.add(line)
    return(dic)

class reverseIdentify(object): #定义分词类
    def __init__(self,stopdict_path="",dict_path=""):
        self.stopdict = fileToDict(stopdict_path)
        self.dict = fileToDict(dict_path)

    def cut(self,text,n): #实现分词功能，返回分词结果与成功被识别的单词
        textlength = len(text)
        end = textlength #记录单词分片终止位
        word_stack = []  # 一个用于存储分词结果的列表
        success_stack = [] #一个用于存储成功被识别的词的表
        wordlength = 0 #记录每个分词长度
        while end != 0:
            x = 0  # 重复初始化x，用于调整循环中所读取的单词递减长度
            wordlength = 0 #重复初始化wordlength，用于记录当前的单词长度
            while wordlength == 0:
                word = text[end-n+x:end] 
                x += 1
                if word in self.stopdict and len(word)==1: #识别停用词，如果是单位数停用词就加上引号特殊处理
                    word_stack.append("'" + word + "'")  # 如果词并没有在词典里且只剩一位，就输入列表
                    end -= 1  # 记位调整1
                    # print("停用词： " + word)
                    break

                elif word in self.stopdict: #识别停用词，如果是复数停用词就不理会
                    pass
                
                elif word in self.dict:
                    # print("成功被识别词:" + word)
                    word_stack.append("/")  # 用于分割单词
                    word_stack.append(word)  # 记录匹配到的单词，最终结合其他未识别词与停用词一起输出全句
                    success_stack.append(word) #独立的记录匹配到的单词表
                    wordlength = len(word)  # 记录单词长度x
                    end -= wordlength  # 调整下次识别的文字结束位
                    break

                elif len(word) == 1: 
                    # print("单数未识别词: " + word)
                    word_stack.append(word)  # 如果词并没有在词典里且只剩一位，就输入列表
                    end -= 1  # 记位调整1
                    break        
            
        return(word_stack,success_stack)

stopdict_path = "/baidu_stopwords.txt"
dict_path = "/清华大学开放中文词库总和.txt"
identifier = reverseIdentify(stopdict_path=stopdict_path,dict_path=dict_path)


text1 = "文章讨论了信息伦理学与互联网的关系"

word_stack,success_stack = identifier.cut(text1,5)
print("\ntext1，分词长度5，用清华开源词库")
print(*word_stack[::-1], sep=" ")
print(*success_stack[::-1], sep=" ")
'''
向量长度：5
结果：文 章 讨 '论' '了' 信 息 伦 理 学 '与' 互 联 网 '的' 关 系
所匹配到的词：-
结果显示算法只匹配到了4个停用词，没有任何词被成功匹配，
即便词库拥有156679个词，显然也是不够的，里面没有适用于这句话的词，需要自己添加，于是后续的例子都有自己手动添加停用词进txt文件'''

word_stack,success_stack = identifier.cut(text1,5)
print("\ntext1，分词长度5")
print(*word_stack[::-1], sep=" ")
print(*success_stack[::-1], sep=" ")
'''向量长度：5
添加相关词语后得到的结果如下
结果：文 章 讨论 / '了' 信息伦理学 / '与' 互联网 / '的' 关系 /
所匹配到的词：讨论 信息伦理学 互联网 关系'''

word_stack,success_stack = identifier.cut(text1,4)
print("\ntext1，分词长度4")
print(*word_stack[::-1], sep=" ")
print(*success_stack[::-1], sep=" ")
'''向量长度：4
这次调整了向量长度，
结果：文 章 讨论 / '了' 信息 / 伦理学 / '与' 互联网 / '的' 关系 /
所匹配到的词：讨论 信息 伦理学 互联网 关系'''

text2 = "北京大学生喝进口红酒"
word_stack,success_stack = identifier.cut(text2,5)
print("\ntext2，分词长度5")
print(*word_stack[::-1], sep=" ")
print(*success_stack[::-1], sep=" ")
'''结果：北京大学 / 生喝 / 进口 / 红酒 /
所匹配到的词：北京大学 生喝 进口 红酒
由于是最大逆向算法，无论怎么调整参数，只要生喝这个词在词表中，都会得到生喝而不是北京大学生'''

text3 = "让我们以爱心和平等来对待动物"
word_stack,success_stack = identifier.cut(text3,4)
'''结果：'让' '我' '们' '以' 爱心 / '和' 平等 / '来' 对待 / 动物 /
所匹配到的词：爱心 平等 对待 动物'''
print("\ntext3，分词长度4")
print(*word_stack[::-1], sep=" ")
print(*success_stack[::-1], sep=" ")

"""总结：词库是分词工作中最为重要的基础，在分词技术上，不同的算法会带来不同的分词结果，
分词的方向——正向或逆向、分词的向量长度、甚至在作业中未有实现的词频统计都会影响分词结果"""