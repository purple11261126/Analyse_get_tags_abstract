#!/usr/bin/env pytho
# encoding: utf-8
'''
Created on 2017年4月10日

@author: wangcong

提取文章标签和简介

要添加的功能：
    1、tags：要把所有tags保存到list当中，方便统计。但现在保存到list时每个汉字都是分开的，不知道怎么解决。unicode 或 string 存入数组时每个文字都是分开的，怎么解决。
    2、学会用numpy或者pandas处理csv。
    3、将数据保存到数据库。
        
问题：

'''
import os
from tags_abstract import get_tags, get_abstract
import csv
import numpy as np
import pandas as pd



def format_content(content):
    '''
    规整字符串
    '''
    content = content.replace(',', '，') #csv使用 英文逗号 作为分隔符，要把文档中的 英文逗号 替换成 中文逗号（参考：http://blog.sina.com.cn/s/blog_468530a60100kjpy.html）
    return content


def no_file_name(content):
    '''
    去掉不能作为文件名的符号
    参考：
    http://stackoverflow.com/questions/22620965/ioerror-errno-22-invalid-mode-wb-or-filename
    http://www.jb51.net/article/100144.htm
    
    IOError: [Errno 22] invalid mode ('wb') or filename（参考：http://www.cnblogs.com/nju2014/p/5364453.html）
    这个错误的根本原因，如果不是文件打开模式不对，那就是文件名或者路径存在能看见或者不能看见的错误。比如直接包含违规字符（能看见的），或者转义字符中包含违规字符（看不见的）。
    '''
    no_title_lst = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for no_title in no_title_lst:
         content = content.replace(no_title, '')
    return content
    

def get_info(file_path_str):
    '''
    提取文档title、content、tags、abstract
    '''
    with open(file_path_str, 'r') as f:
        title = format_content(f.readline()[:-1])
        title = no_file_name(title)
        text = format_content(f.readline())
#     tags = get_tags(text)
#     abstract = get_abstract(text)
    return title, text#, tags, abstract, 


def save_path(title):
    '''
    简单的利用title包含某些关键词将文档分类，下一步能做到 文档聚类 么？？
    '''
    #华为讯飞网站栏目分类
    caiji_app = 'E:/content/02_caiji_app'           #APP行业动态
    caiji_news = 'E:/content/02_caiji_news'         #最新资讯
    caiji_weixin = 'E:/content/02_caiji_weixin'     #微信开发
    caiji_web = 'E:/content/02_caiji_web'           #网站建设
    
    if ('APP' in title) or ('app' in title):
        return caiji_app
    elif ('微信' in title):
        return caiji_weixin
    elif ('网站' in title):
        return caiji_web
    else:
        return caiji_news


def save_csv(title, text, tags, abstract):
    '''
    写入到csv文件，注意 csv 需要 gbk 编码的字符
    参考：
    http://blog.csdn.net/lixiang0522/article/details/7755059
    http://blog.csdn.net/rav009/article/details/9038821
    '''
    print '写入文件：', title+'.csv'
    
    title = title.decode('utf-8').encode('gbk', 'ignore') # UnicodeEncodeError: 'gbk' codec can't encode character u'\ufeff' in position 0: illegal multibyte sequence（参考：http://www.crifan.com/unicodeencodeerror_gbk_codec_can_not_encode_character_in_position_illegal_multibyte_sequence/）
    text = text.decode('utf-8').encode('gbk', 'ignore')
    tags = tags.encode('gbk', 'ignore')
    abstract = abstract.encode('gbk', 'ignore')
    
    file_name = title + '.csv'
    file_path = os.path.join(save_path(title), file_name)
    
    with open(file_path, 'wb') as f:    #为啥用 w 标题和内容之间就会出现空行？？
        writer = csv.writer(f)
        writer.writerow(['post_title', 'post_content', 'post_keywords', 'post_excerpt', 'post_source']) 
        writer.writerow([title, text, tags, abstract, '华为讯飞'.decode('utf-8').encode('gbk')])
        
        
def merge_csv_numpy():
    '''
    合并csv文档（numpy）
    '''
    merge_path = 'E:/content/03_merge'
    csv_name_lst = os.listdir(merge_path)
    csv_data_lst = []
    for csv_name in csv_name_lst:
        print '提取信息：', csv_name.decode('gbk').encode('utf-8')
        csv_path = os.path.join(merge_path, csv_name)
        with open(csv_path, 'r') as f:
            csv_title_str = f.readline()[:-1]                                                   #取得csv的标题
        csv_title_lst = csv_title_str.split(',')                                                #将标题转化为list类型
        csv_title_index_lst = [csv_title_lst.index(csv_title) for csv_title in csv_title_lst]   #取得标题的下标
        try:
            data_array = np.loadtxt(fname=csv_path, 
                                    dtype=str, 
                                    delimiter=',', 
                                    skiprows=1, 
                                    usecols=csv_title_index_lst)                                #根据下标取得内容
            if (data_array[0] == '') or (data_array[1] == ''):  #有些csv内容是空的，这里做一下过滤，不过错误日志并没有写入这里的信息，而是正常记录了异常，为什么？？
                with open('./error_merge.txt', 'a') as log_file:
                    log_file.write(csv_name + '：内容为空' + '\n' + '\n')
                continue
            else:
                csv_data_lst.append(data_array)                                                 #所有内容添加到数组中
        except IndexError as error:
            #有些csv文件会莫名其妙的报出索引超出，可是打开看一下，并没发现什么问题。
            with open('./error_merge.txt', 'a') as log_file:
                log_file.write(csv_name + ': ' + str(error) + '\n' +'\n')
                print str(error)
            continue
            
    with open((merge_path + '/00merge.csv'), 'wb') as f:
        print '写入00merge.csv'
        writer = csv.writer(f)
        writer.writerow(csv_title_lst)
        writer.writerows(csv_data_lst)


def save_error(error):
    '''
    保存错误记录
    '''
    with open('./error.txt', 'a') as log_file:
        log_file.write(str(error) + '\n' + '\n')
        print str(error)
        
        
def main():
    '''
    主函数
    '''
    #初始化数据
    caiji_path = 'E:/content/01_caiji'
    file_name_lst = os.listdir(caiji_path)
    
    for file_name in file_name_lst:
        file_path_str = os.path.join(caiji_path, file_name)
        
        #规整文件名
#         file_name_use = no_file_name(file_name)
#         file_path_use_str = os.path.join(caiji_path, file_name_use)
#         os.rename(file_path_str, file_path_use_str)     #因为原文件根本无法读取，所以无法rename

        try:
            #取得标题，正文，标签，简介
            title = get_info(file_path_str)[0]
            text = get_info(file_path_str)[1]
            tags = get_tags(text)[0][0]
            abstract = ''
            for temp in get_abstract(text):
                abstract += temp
                
            #写入文件
            save_csv(title, text, tags, abstract)
            
        except (IOError, IndexError)  as error:
            #有些文件名包含违规符号，产生读取错误，由于原文件Python根本无法读取，所以也无法操作 （但是手动可以操作，眼上去和正常文件一样，但包含的转义字符里有违规字符）目前只能跳过。
            save_error(error)
            continue
    

if __name__ == '__main__':
#     main()
    merge_csv_numpy()































