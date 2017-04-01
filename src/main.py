#!/usr/bin/env python
# encoding: utf-8
'''
Created on 2017年4月1日

@author: wangcong

提取文章标签和简介

要添加的功能：
    tags：要把所有tags保存到list当中，方便统计。但现在保存到list时每个汉字都是分开的，不知道怎么解决。unicode 或 string 存入数组时每个文字都是分开的，怎么解决。
        学会用numpy或者pandas处理csv。
        上次好像看到：不要把 with open() 语句放到 try 里面，因为发生异常时，将不能关闭文件，但是找不到了，回头具体找一下。
        
问题：
    1、csv_merge()：
                                        合并csv后简介和源文件内容不符。
                                        合并多个文件是报错：IndexError: list index out of range
    2、en2zh()：title字符串替换后，乱码。目前暂时跳过了带英文逗号标题的文档。
    3、以后想把异常信息保存到txt中。
    4、把主函数里的try去掉，处理多个文件就会报这个错误：[Errno 22] invalid mode ('r') or filename
        
'''

import os
from tags_abstract import get_abstract, get_tags
import sys
import csv
import numpy as np


def en2zh(title, content):
    '''
    字符串替换：csv使用 英文逗号 作为分隔符，要把文档中的英文逗号替换成 中文逗号（参考：http://blog.sina.com.cn/s/blog_468530a60100kjpy.html）
    '''
    title = title.replace(',', '，')
    content = content.replace(',', '，')
#     print title#.decode('gbk')#.encode('gbk')
#     print content
    return title, content


def save_path(file_name):
    '''
    利用title包含某些关键词将文档分类，下一步能做到 文档聚类 么？？
    '''
    #华为讯飞网站栏目分类
    caiji_app = 'E:/content/02_caiji_app'           #APP行业动态
    caiji_news = 'E:/content/02_caiji_news'         #最新资讯
    caiji_weixin = 'E:/content/02_caiji_weixin'     #微信开发
    caiji_web = 'E:/content/02_caiji_web'           #网站建设
    
    if ('APP' in file_name) or ('app' in file_name):
        return caiji_app
    else:
        return caiji_news


def save_txt(file_name, title, content, tags, abstract):
    '''
    写入到txt文件
    '''
    file_path_txt = os.path.join(save_path(file_name), file_name)
    with open(file_path_txt, 'w') as f:
        f.write(title.encode('utf-8') + '\r\n' + '\r\n')    #因为title的类型是unicode，而write要求参数为str，所以写入时要手动编码
        print '写入title：', title
        f.write(content.decode('utf-8').encode('utf-8') + '\r\n' + '\r\n')  #content 为str类型，可以不用转码，但刚才不知道为啥乱码了
        print '写入content' 
        f.write(tags.encode('utf-8') + '\r\n' + '\r\n')
        print '写入tags'
        f.write(abstract.encode('utf-8'))
        print '写入abstract'
    

def save_csv_solo(file_name, title, content, tags, abstract):
    '''
    写入到csv文件，每篇文档独立
    参考：http://blog.csdn.net/lixiang0522/article/details/7755059
    '''
    file_path_csv = os.path.join(save_path(file_name), file_name[:-4]) + '.csv'
    with open(file_path_csv, 'wb') as f:    #wb中的w表示写入模式，b是文件模式
        writer = csv.writer(f)
        writer.writerow(['post_title', 'post_content', 'post_keywords', 'post_excerpt', 'post_source']) #写入一行用 writerow ，多行用writerows
        writer.writerow([title, content.decode('utf-8').encode('gbk'), tags.encode('gbk'), abstract.encode('gbk'), '华为讯飞'.decode('utf-8').encode('gbk')]) #这里的编码卡了一下（参考：http://blog.csdn.net/diy534/article/details/37627937）。另外Excel不能直接打开 utf-8 编码，所以用 gbk。
        

def save_csv_all(file_name, title, content, tags, abstract):
    '''
    写入到csv文件，都在一个文件
    '''
    pass
    
        
def csv_merge():
    '''
    将独立的csv文档合并到一起
    '''
    merge_path = 'E:/content/03_merge'
    csv_list = os.listdir(merge_path)
    csv_data_lst = []

    #提取所有文档信息
#     for csv_name in csv_list:           #csv编码格式是 gbk
#         csv_path = os.path.join(merge_path, csv_name)
#         with open(csv_path, 'r') as f:
#             csv_content_lst = f.readline().split(',')
#             csv_content_lst = f.readline().split(',')   #又是最笨的办法，两次readline，拿到文档信息
#         csv_data_lst.append(csv_content_lst)    #所有csv内容
        
    #提取所有文档信息，用到 numpy，有index溢出报错
    for csv_name in csv_list:
        csv_path = os.path.join(merge_path, csv_name)
        with open(csv_path, 'r') as f:
            csv_title_str = f.readline()[:-1]   #取得文档标题，并去掉最后的换行符
        csv_title_lst = csv_title_str.split(',')    #将标题字符串转换为列表
        csv_title_index_lst = [csv_title_lst.index(title) for title in csv_title_lst]   #取得title各列的索引号
        try:
            data_array = np.loadtxt(fname = csv_path, 
                                    dtype = str, 
                                    delimiter = ',', 
                                    skiprows = 1, 
                                    usecols = csv_title_index_lst)  #取得各列的信息
            if (data_array[0] == '') or (data_array[1] == ''):
                continue
            else:
                csv_data_lst.append(data_array)     #汇总所有csv信息
        except:
            print sys.exc_info()[0], sys.exc_info()[1]
         
         
    #把csv_data_lst中所有文档写入一个csv文件
    with open('E:/content/03_merge/00_merge.csv', 'wb') as f:
        write = csv.writer(f)
        write.writerow(['post_title', 'post_content', 'post_keywords', 'post_excerpt', 'post_source'])
        write.writerows(csv_data_lst)
        
        
def save_mySQl():
    '''s
    写入到MySQL数据库
    '''
    pass


def main():
    '''
    主函数
    '''   
    #初始化数据
    caiji_path = 'E:/content/01_caiji'  #初始文件路径，目前不能带中文路径。注意：不应该按照win目录写法，用‘\’分隔符（参考：https://zhidao.baidu.com/question/1112328523986032419.html），会报错：WindowsError: [Error 123]（参考：http://www.aichengxu.com/python/46906.htm）。
    file_list = os.listdir(caiji_path)  #文件名列表
    
    #根据列表处理文档
    for file_name in file_list:
        abstract = ''   
        file_path = os.path.join(caiji_path, file_name) #.decode('gbk') #拼接出完整文件路径
        try:
            with open(file_path, 'r') as f:
                title = file_name[:-4]                #title
                #暂时只能去掉带英文逗号的标题的文档了
                if ',' in title:
                    continue
                else:
                    print '获得title：', title.decode('gbk')
                    
                    content = f.readline()                  
                    content = f.readline()                  #正文，暂时用最笨的方法，两次readline输出了第二行的正文。
                    print '获得content：......'
                    
                    #字符串替换：csv使用 英文逗号 作为分隔符，要把文档中的 英文逗号 替换成 中文逗号。
                    #title = en2zh(title, content)[0]
                    content = en2zh(title, content)[1]
                    
                    tags = get_tags(content)[0][0]          #tags
                    print '获得tags'
                      
                    for temp in get_abstract(content):
                        abstract += temp                    #简介
                    print '获得abstract'
                     
                    save_csv_solo(file_name, title, content, tags, abstract)
        except:
            print sys.exc_info()[0], sys.exc_info()[1]  #打印异常，后面想写到txt里
    
    
if __name__ == '__main__':
#     main()
    csv_merge()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    