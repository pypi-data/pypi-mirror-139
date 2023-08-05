from string import punctuation
import re

def preprocessSentence(mySentence,methods="lnp"):
    '''
    预处理句子，并分词
    methods:
    l-lower:小写字母
    n-num:替换数字为num
    p-punctuation:删除标点符号
    '''
    puncStr=punctuation+"「」（）？！?!<>《》、“”。，：♫︰【】—；"
    if "l" in methods:
        mySentence=mySentence.lower()
    mySentence=re.sub("([a-zA-Z]+)",r" \1 ",mySentence)
    
    if "n" in methods:
        mySentence=re.sub("([0-9]+)"," num ",mySentence)
        
    if "p" in methods:
        mySentence=re.sub("["+puncStr+"]+","",mySentence)
    
    mySentence=" ".join([charItem for charItem in mySentence.split(" ") if len(charItem)>0])
    mySentenceList=[]
    for wordItem in mySentence.split(" "):
        if len(re.findall("[\u4e00-\u9fa5]",wordItem))==len(wordItem):
            for charItem in wordItem:
                mySentenceList.append(charItem)
        else:
            mySentenceList.append(wordItem)
    tmpSentence=" ".join(mySentenceList)
    return tmpSentence               

def getSEOfEntity_forCH(entityItem,mySentenceList):
    '''
    获取中文实体entityItem列表头尾id
    '''
    seList=[]
    for tokenI,tokenItem in enumerate(mySentenceList):
        if tokenItem==entityItem[0]:
            plusTokenI=0
            startI=tokenI+plusTokenI
            while plusTokenI<len(entityItem) and tokenI+plusTokenI<len(mySentenceList) and mySentenceList[tokenI+plusTokenI]==entityItem[plusTokenI]:
                plusTokenI+=1
            if plusTokenI==len(entityItem):
                endI=tokenI+plusTokenI
                seList.append([startI,endI])
    return seList

def getSEOfEntity_forEN(entityItem,mySentenceList):
    '''
    获取英文实体entityItem列表头尾id
    '''
    entityItemList=entityItem.split(" ")
    mySentenceList=mySentenceList
    seList=[]
    for tokenI,tokenItem in enumerate(mySentenceList):
        if tokenItem==entityItem[0]:
            plusTokenI=0
            startI=tokenI+plusTokenI
            while plusTokenI<len(entityItemList) and tokenI+plusTokenI<len(mySentenceList) and mySentenceList[tokenI+plusTokenI]==entityItemList[plusTokenI]:
                plusTokenI+=1
            if plusTokenI==len(entityItemList):
                endI=tokenI+plusTokenI
                seList.append([startI,endI])
    return seList

def tagSentence(mySentence,entityList):
    '''
    为句子mySentence标注entityList中的实体
    '''
    mySentenceList=preprocessSentence(mySentence).split(" ")
    
    BIOList=["O" for tagItem in mySentenceList]
    
    mySentence_forCH="".join(mySentenceList)
    mySentence_forEN=" ".join(mySentenceList)
    seList=[]
    for entityI,entityItem in enumerate(entityList):
        entityItem=entityItem.lower()
        if len(re.findall("[\u4e00-\u9fa5]",entityItem))>0:
            if entityItem in mySentence_forCH:
                seItem=getSEOfEntity_forCH(entityItem,mySentenceList)
        elif entityItem in mySentenceList:
            if entityItem in mySentence_forEN:
                seItem=getSEOfEntity_forEN(entityItem,mySentenceList)
        seList+=seItem
    
    for seItem in seList:
        startI,endI=seItem
        BIOList[startI]="B"
        for charI in range(startI+1,endI):
            BIOList[charI]="I"
    
    return " ".join(BIOList)

if __name__=="__main__":
    mySent="《MarketingApi接入规范和实操指南PDF》【Knowhow AMS】MarketingApi作为腾讯广告统一的对外Api，主要负责各类子系统对外API能力的封装，提供统一的广告投放API能力。本课程主要分享接入MarketingApi模块时，需要了解、注意的各项规范、对接流程，从开发到测试到发布，提供实际接入例子，方便后续各类子系统对接。"
    newSent=tagSentence(mySent,["广告","api","投放"])
    print(newSent)