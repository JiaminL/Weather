#!/usr/bin/python
# -*- coding:utf-8 -*-
from MyClass import *

def getChoice(DISPLAYSURF,windowSize,buttonSize,hintSize,cityList):
    boxRect = pygame.Rect(int(windowSize[0]*0.2),int(windowSize[1]*0.4),int(windowSize[0]*0.6),40)
    btAreaRect = pygame.Rect(int(windowSize[0]*0.1),int(windowSize[1]*0.25),int(windowSize[0]*0.8),int(windowSize[1]*0.7))
    backRect = pygame.Rect(10,10,*buttonSize)
    inputBox = Inputbox(DISPLAYSURF, boxRect, WHITE, BLACK, 20, "请输入城市名（拼音）：", int(boxRect.height * 0.5), BLACK)
    while True:
        while True:#通过输入减少查询范围
            inputPinyin = inputBox.getInput()
            rightCityL = cityList.findCityByPinyin(inputPinyin)
            if rightCityL:
                break
            inputBox.showError("没有找到对应城市，请按任意键重新输入")
        clickWindow = ButtonWindow(DISPLAYSURF,hintSize,"请点击选择城市:",buttonSize,btAreaRect,rightCityL,backRect)
        myChioce = clickWindow.getClick()
        if myChioce:
            return myChioce


def getCityList(DISPLAYSURF,cityUrl,appkey,buttonRect,errorRect):
    while True:#拉取城市列表
        cityList = Citys(cityUrl,appkey)
        if cityList.list == None:
            error = "获取城市信息出错，请检查您的网络、APPKEY以及接口地址"
            tryButton = Button(DISPLAYSURF, buttonRect, LTGRAY, BLACK, "重试")
            mousex, mousey = 0, 0
            while True:
                mouseClicked = False
                DISPLAYSURF.fill(WHITE)
                drawText(DISPLAYSURF, errorRect, False, error, errorRect.height, RED, True)
                tryButton.drawButton()
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    elif event.type == MOUSEMOTION:
                        mousex, mousey = event.pos
                    elif event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        mouseClicked = True
                if tryButton.onButton(mousex, mousey):
                    tryButton.highLight(DPGRAY)
                    if mouseClicked:
                        break
                pygame.display.update()
        else: break
    return cityList


def main():
    pygame.init()
    #set some information of window
    windowSize = (1100, 650)
    buttonSize = (150, 40)
    hintSize = 40
    bcRect = pygame.Rect(10, 10, *buttonSize)
    pictureSize = (int(windowSize[1] * 0.15), int(windowSize[1] * 0.15))
    pictureRect = pygame.Rect(int(windowSize[0] / 12), buttonSize[1] * 2, *pictureSize)
    errorRect = pygame.Rect(int(windowSize[0]*0.15), int(windowSize[1]*0.35), int(windowSize[0]*0.7),int(hintSize*0.7))
    tryAgainRect = pygame.Rect(int(windowSize[0]*0.4), int(windowSize[1]*0.55), int(windowSize[0]*0.2),hintSize)
    #API接口及appkey
    cityUrl = "http://apis.juhe.cn/simpleWeather/cityList"
    weatherUrl = "http://op.juhe.cn/onebox/weather/query"
    appkey = "affa834845c6fd3421bbce371dbf2d95"
    #设置窗口、图标、标题
    DISPLAYSURF = pygame.display.set_mode(windowSize, 0, 32)
    pygame.display.set_icon(pygame.image.load('picture/weather.png'))
    pygame.display.set_caption('全国天气预报')
    #获取所有城市名称的一个列表
    cityList = getCityList(DISPLAYSURF,cityUrl,appkey,tryAgainRect,errorRect)
    while True:
        #先输入一个字符串，然后找到拼音段里有这一子串的城市列表，显示在窗口以后通过点击选择要查询的城市
        cityName = getChoice(DISPLAYSURF, windowSize, buttonSize, hintSize, cityList)
        wthWindow = WeatherWindow(DISPLAYSURF, bcRect)
        wthWindow.setInfor(weatherUrl, appkey, cityName, windowSize, pictureRect)
        if wthWindow.information.error:
            wthWindow.showError("获取天气信息失败，您或许需要检查一下网络")
        else:
            wthWindow.drawWindow()

if __name__ == '__main__':
    main()