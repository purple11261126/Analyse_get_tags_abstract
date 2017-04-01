# encoding: utf-8
'''
Created on 2017年3月23日

@author: wangcong
'''
import jieba  
import jieba.analyse
import networkx as nx  
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer  
  
  
def cut_sentence(sentence):  
    """ 
    分句 
    :param sentence: 
    :return: 
    """  
    if not isinstance(sentence, unicode):  
        sentence = sentence.decode('utf-8')  
    delimiters = frozenset(u'。！？')  
    buf = []  
    for ch in sentence:  
        buf.append(ch)  
        if delimiters.__contains__(ch):  
            yield ''.join(buf)  
            buf = []  
    if buf:  
        yield ''.join(buf)  
  
  
def load_stopwords(path='./stop.txt'):  
    """ 
    加载停用词 
    :param path: 
    :return: 
    """  
    with open(path) as f:  
        stopwords = filter(lambda x: x, map(lambda x: x.strip().decode('utf-8'), f.readlines()))  
    stopwords.extend([' ', '\t', '\n'])  
    return frozenset(stopwords)  
  
  
def cut_words(sentence):  
    """ 
    分词 
    :param sentence: 
    :return: 
    """  
    stopwords = load_stopwords()  
    return filter(lambda x: not stopwords.__contains__(x), jieba.cut(sentence))  
  
  
def get_abstract(content, size=3):  
    """ 
    利用textrank提取摘要 
    :param content: 
    :param size: 
    :return: 
    """  
    docs = list(cut_sentence(content))  
    tfidf_model = TfidfVectorizer(tokenizer=jieba.cut, stop_words=load_stopwords())  
    tfidf_matrix = tfidf_model.fit_transform(docs)  
    normalized_matrix = TfidfTransformer().fit_transform(tfidf_matrix)  
    similarity = nx.from_scipy_sparse_matrix(normalized_matrix * normalized_matrix.T)
    scores = nx.pagerank(similarity)  
    tops = sorted(scores.iteritems(), key=lambda x: x[1], reverse=True)  
    size = min(size, len(docs))  
    indices = map(lambda x: x[0], tops)[:size]  
    return map(lambda idx: docs[idx], indices)


def get_tags(content):
    '''
    使用 jieba 提取文章 tags
    不知道为什么，感觉 TF-IDF 比 textrank 效果要好一些，虽然textrank比较高大上。
    '''
    tags_tfidf = jieba.analyse.extract_tags(content, topK=2, withWeight=True)
    #tags_textrank = jieba.analyse.textrank(content, topK=10, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
    #print 'TF-IDF : ', tags_tfidf[0][0], tags_tfidf[0][1]
    #print 'TextRank : ', tags_textrank[0][0], tags_textrank[0][1]
    return tags_tfidf  
  


if __name__ == '__main__':
    content = u'大学校园相对于社会，还是比较单纯天真、浪漫的。学生除了学习之外，就是交友了。社团活动或是一些联谊都会增加交友的机会。大学是一个过渡阶段，交友不仅是一种生活的情趣还是以后出社会的刚需。今天的主角11点11分，就是为校园社交服务的一款手机app开发。为广大学子的交友、沟通提供一个自由的空间和平台。 11点11分这个手机软件开发的设置比较简单，只有在11点11分这个点才开始进行条件匹配。由于有校园地理位置的认证，大学生们只需提供性别就好。11分11秒的交流时间里，要判断是否对方符合自己的口味，如果是就需要在规定时间内点击“Like”，那么对方的资料会保存，而且可以知道ta第二天的具体定位。或是不合适点击“Kick”，系统则会重新匹配为用户查找。若是超过时间没有点击选择，则对方信息将自动删除。当然，11点11分这个社交app还有其他的功能。如新发现，每天发布新论坛内的精选内容，聊天秘籍等。还有羞羞哒社区，这时用户需要取昵称并设置头像，也可以开启匿名身份模式。在羞羞哒社区里发帖或是关注其他用户。由于是非实名制的方式，所以各种帖子，如曝照、八卦、各种羞羞的话题，都有所呈现。此外，还有YO一下功能，其实就是一种添加好友请求。而在我的消息与我的帖子里，用户能查看得到自己的之前的消息和发过的帖子或是别人与你互动的消息。11点11分是个蛮好玩的手机软件开发应用。因为主打的是高校，大家的话题差不多类似，还是很容易就聊得来、聊得开，还会比较安全靠谱。夜晚十一点，睡意不浓之时聊下天会是不错的选择。若是能不期而遇到一个有着相同兴趣爱好的朋友那就更好了。本文由天津APP开发公司华为讯飞发布，转载需注明出处http://www.mdkg.net/'
    print get_tags(content)[0][0], get_tags(content)[1][0]    #tags
    for i in get_abstract(content):    #简介
        print i 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        