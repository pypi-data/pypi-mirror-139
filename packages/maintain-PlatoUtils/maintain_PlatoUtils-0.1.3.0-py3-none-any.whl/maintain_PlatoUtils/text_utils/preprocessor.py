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
    mySent="Art Direction Bootcamp: Building Worlds Through Shape Language 通过形状语言建立大世界   讲师：Patrick Faulwetter   【内容简介】 In order to inform the process of building imaginary worlds for video games and movies, this talk aims to examine the term ""culture"" as ""story"" which expresses itself in the physical world. The story of a culture is written in a myriad of particulars from architecture, customs, symbols, values to transportation systems. Starting from a philosophical perspective, Patrick will show the practical process of using 2D and 3D tools to build shape languages from abstract shapes as a foundation for designing different subject matters for world building including vehicles, costumes, architecture and environments. 为了让大家了解到电子游戏和电影的虚拟世界构建过程，本讲座将深入探讨“文化”一词，文化即是我们现实世界中所经历的故事。从建筑、习俗、符号、价值观到交通系统，文化的故事以无数的细节书写。从哲学的角度出发，Patrick将展示为World Building设计不同的主题，包括车辆、服装、建筑和环境时使用2D和3D工具从抽象形状构建形状语言的实际过程。   本文翻译官：Samanthawei(魏翠敏)"
    
    processedSent=preprocessSentence(mySent)
    print(processedSent.split(" "))
    
    tagList=tagSentence(mySent,["广告","api","投放"])
    print(tagList.split(" "))