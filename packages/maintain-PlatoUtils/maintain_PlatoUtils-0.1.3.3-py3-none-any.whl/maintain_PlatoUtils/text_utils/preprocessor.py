from string import punctuation
import re
from stopwords import stopwordList

totalStopWordList=stopwordList
def preprocessSentence(mySentence,methods="lnp",stopwords=[],withStopWord=True):
    '''
    预处理句子，并分词
    methods:
    l-lower:小写字母
    n-num:替换数字为num
    p-punctuation:删除标点符号
    '''
    totalStopWordList+=stopwords
    mySentence=mySentence.strip()
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
    if withStopWord==True:
        mySentenceList=[tokenItem for tokenItem in mySentenceList if tokenItem not in totalStopWordList]
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
                seList+=seItem
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
    mySent="实验设计【启航计划】\n"
    
    processedSent=preprocessSentence(mySent)
    print(processedSent.split(" "))
    
    tagList=tagSentence(mySent,["广告","api","投放"])
    print(tagList.split(" "))