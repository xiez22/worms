import requests
from bs4 import BeautifulSoup
import os

allUniv = []
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""
def fillUnivList(soup):
    data = soup.find_all('tr')
    for tr in data:
        ltd = tr.find_all('td')
        if len(ltd)==0:
            continue
        singleUniv = []
        for td in ltd:
            singleUniv.append(td.string)
        allUniv.append(singleUniv)
def printUnivList(num):
    print("{:^4}{:^10}{:^5}{:^8}".format("排名","学校名称","省市","总分"))
    for i in range(num):
        u=allUniv[i]
        print("{:^4}{:^10}{:^5}{:^8}".format(u[0],u[1],u[2],u[3]))

def infbrief(name):
    url="https://baike.baidu.com/item/"+name
    headers = {'Accept': '*/*',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Cache-Control': 'max-age=0',
                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                   'Connection': 'keep-alive',
                   'Referer': 'http://www.baidu.com/' }

    r=requests.get(url,headers=headers)
    r.encoding='utf-8'
    soup=BeautifulSoup(r.text,features='html.parser')
    soup=soup.find('div',{'class':'lemma-summary'})
    res=soup.find_all('div',{'class':'para'})
    chs=str(res)
    #print(chs)

    leftA=0
    leftB=-1
    result=""
    last_g=0

    #进行删减
    for ch in chs:
        if ch=='<':
            leftA+=1
        elif ch=='>':
            leftA-=1
        elif ch=='[':
            leftB+=1
        elif ch==']':
            leftB-=1
        elif leftA==0 and leftB==0:
            result=result+ch

        result=result.replace('\n','')
        result=result.replace('。,','。')

    #返回
    return result

#正文内容
#欢迎使用！
print("欢迎使用中国大学排行文章自动生成工具1.0版，接下来，请按照提示来使用本软件吧！\n正在网络上抓取最新大学排名信息，请稍后……")

try:
    url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2018.html'
    html = getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    fillUnivList(soup)

    name1=input("排名信息抓取完成，请输入您要比较的第一个大学的名称：")
    name2=input("接下来，请输入第二个大学的名称：")

    print("很好，请稍等片刻，我们正在抓取这两所大学的相关信息……")

    result1=infbrief(name1)
    result2=infbrief(name2)

    print("好的，大学的信息抓取完成，正在自动生成文章。\n以下是文章内容：\n\n")

    paiming1=0
    paiming2=0
    mark1=0
    mark2=0
    bingo=0

    #获取大学排名
    for univ in allUniv:
        if name1==univ[1]:
            paiming1=eval(univ[0])
            mark1=eval(univ[3])
            bingo+=1
        elif name2==univ[1]:
            paiming2=eval(univ[0])
            mark2=eval(univ[3])
            bingo+=1
    if bingo<2:
        raise CustomError("No such university!")


    #生成文章
    content="                             {}和{}哪家强？99%的中国人都不知道\n\n    近日，关于{}和{}哪个更好在社会上引发了广泛的争议，小伙伴们有的从地理位置优势角度进行分析，有的从二者的强势专业角度进行PK，有的甚至从男女生比例角度进行撕逼。而小编也脑洞大开，决定就基于院校排名的角度和小伙伴们聊聊{}和{}的对比情况，今天小编就带大家来比较一下哪个大学更好。\n\n".format(name1,name2,name1,name2,name1,name2)
    content+="    首先我们来看一看这两所大学的简介：\n    首先是{}：{}\n\n    接下来我们看一看{}：{}\n".format(name1,result1,name2,result2)
    content+="    看完了简介之后，不知道大家对这两所学校的看法有没有改变呢？好的，接下来我们就要正式开始比较了！！！\n\n"
    content+="    在最新版的中国最好大学排行榜中,{}排在全国第{}名，而{}排在全国第{}名！！！\n".format(name1,str(paiming1),name2,str(paiming2))

    if abs(paiming1-paiming2)>20:
        if paiming1<paiming2:
            content+="    由此可见，{}要完爆{}！！！\n\n".format(name1,name2)
        else:
            content+="    由此可见，{}要完爆{}！！！\n\n".format(name2,name1)
    elif abs(paiming1-paiming2)<=2:
        content+="    由此可见，两所学校的实力在伯仲之间，从排名上难以分出差距，{}在排名上取得了微弱的优势。\n\n".format(name1 if paiming1<paiming2 else name2)
    else:
        content+="    由此可见，两所学校的差距并不是很大，{}在排名上取得了一定的优势。\n\n".format(name1 if paiming1<paiming2 else name2)

    #分数分析
    content+="    除此之外，小编还从软科中国最好大学排名网上获得了两所学校的综合评分，{}获得了{}分，而{}获得了{}分，两所学校的评分差了{:.1f}分。".format(name1,mark1,name2,mark2,abs(mark1-mark2))
    if abs(mark1-mark2)<2:
        content+="所以，两所学校在评分上体现出来的差距微乎其微。"
    elif abs(mark1-mark2)<10:
        content+="所以，这两所学校在评分上还是有着比较小的差距。"
    elif abs(mark1-mark2)<20:
        content+="所以，这两所学校在评分上有着较大的差距。"
    else:
        content+="由此可见，这两个学校在评分上的差距是巨大的。"

    content+="\n\n    好的，关于{}和{}这两所大学的排名分析就到这里了。不过小编在此提醒大家，排名只是参考，选择还是要看自己的兴趣，欢迎大家在评论区发表自己的看法！".format(name1,name2)

    #打印
    print(content)
    print("\n\n------------------------------------------------------------------------------------\n文章已经生成，是否保存？默认保存目录为D:\\AutoSave")
    p=input("请输入相应的数字，1代表保存 ，2代表不保存:")
    if p=="1":
        os.makedirs("D:\\AutoSave",exist_ok=True)
        fpo=open("D:\\AutoSave\\"+name1+"和"+name2+"的比较.txt","wt+",encoding='utf-8')
        fpo.write(content)
        fpo.close()
        print("保存成功！")
    else:
        print("好的，文件不会保存。")
    input()
except:
    print("抱歉，程序出现异常！请重新启动程序。")
    input()