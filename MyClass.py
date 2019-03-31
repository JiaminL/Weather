#!/usr/bin/python
# -*- coding:utf-8 -*-
import pygame, sys
import json, urllib
import urllib.request
from urllib.parse import urlencode
from pygame.locals import *
from pypinyin import pinyin, lazy_pinyin, Style

# color        R   G   B
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
DPGRAY = (155, 155, 155)
LTGRAY = (240, 240, 240)


class Button:  # 按钮
    def __init__(self, DISPLAYSURF, buttonRect, colorBox, colorText, text):
        self.DISPLAYSURF, self.buttonRect, self.colorBox, self.colorText, self.text = \
            DISPLAYSURF, buttonRect, colorBox, colorText, text

    def drawButton(self):  # 绘制按钮
        sizeText = int(self.buttonRect.height * 0.7)
        drawText(self.DISPLAYSURF, self.buttonRect, self.colorBox, self.text, sizeText, self.colorText, True)

    def onButton(self, x, y):  # 检查某个像素点(x,y)是否在按钮上
        return self.buttonRect.collidepoint(x, y)

    def highLight(self, color):  # 给按钮绘制边框以突出显示
        pygame.draw.rect(self.DISPLAYSURF, color, self.buttonRect, 4)


class Inputbox:  # 输入界面
    def __init__(self, DISPLAYSURF, boxRect, colorBox, colorText, maxLen, hintText, sizeHint, colorHint):
        self.DISPLAYSURF = DISPLAYSURF
        self.boxRect = boxRect
        self.colorBox = colorBox
        self.hintText = hintText
        self.maxLen = maxLen
        self.sizeHint = sizeHint
        self.colorHint = colorHint
        self.colorText = colorText
        self.inputText = ""

    def drawInputbox(self):  # 绘制输入框
        self.DISPLAYSURF.fill(LTGRAY)
        textRect = pygame.Rect(self.boxRect.left, self.boxRect.top - int(self.sizeHint * 1.25), self.boxRect.width,
                               self.sizeHint)
        drawText(self.DISPLAYSURF, textRect, False, self.hintText, self.sizeHint, self.colorText, False)
        pygame.draw.rect(self.DISPLAYSURF, self.colorBox, self.boxRect)

    def showError(self, error):  # 显示报错信息，按任意键（除Esc）重新输入
        errorRect = pygame.Rect(self.boxRect.left, self.boxRect.top + int(self.sizeHint * 3), self.boxRect.width,
                                self.sizeHint)
        drawText(self.DISPLAYSURF, errorRect, False, error, self.sizeHint, RED, True)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP:
                    return
            pygame.display.update()

    def drawInput(self):
        sizeText = int(self.boxRect.height * 0.75)
        drawText(self.DISPLAYSURF, self.boxRect, False, self.inputText, sizeText, self.colorText, False)

    def getInput(self):
        message = []
        self.inputText = ''
        eventKey = [K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t,
                    K_u, K_v, K_w, K_x, K_y, K_z]
        inchar = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z']
        while True:
            # 绘制窗口
            self.drawInputbox()
            self.drawInput()
            # 事件处理
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # 回车键确定输入
                elif event.type == KEYUP and event.key == K_RETURN and len(message):
                    return self.inputText
                # 获得键盘输入，仅字母及Backspace有效
                elif event.type == KEYUP:
                    keyLen = len(eventKey)
                    charGet = False
                    if len(message) < self.maxLen:
                        for i in range(keyLen):
                            if event.key == eventKey[i]:
                                message.append(inchar[i])
                                charGet = True
                    if (not charGet):
                        if event.key == K_BACKSPACE and len(message):
                            message.pop()
                self.inputText = ''.join(message)
            pygame.display.update()


class ButtonWindow:  # 按钮界面
    def __init__(self, DISPLAYSURF, hintSize, hintText, btRectSize, btAreaRect, textList, backRect):
        self.DISPLAYSURF, self.hintSize, self.hintText = DISPLAYSURF, hintSize, hintText
        self.btRectSize, self.btAreaRect, self.textList = btRectSize, btAreaRect, textList
        self.hintRect = pygame.Rect(btAreaRect.left, btAreaRect.top - 2 * hintSize, btAreaRect.width, hintSize)
        self.btNum = len(textList)
        self.rectList = self.initRectList()
        self.btList = self.initBtList()
        self.returnBt = Button(DISPLAYSURF, backRect, LTGRAY, BLACK, "返回")

    def initRectList(self):  # 初始化按钮排版
        list = []
        width = self.btRectSize[0] + 15
        height = self.btRectSize[1] + 8
        numX = int(self.btAreaRect.width / width)
        numY = int(self.btAreaRect.height / height)
        mul = numX * numY
        if self.btNum > mul:
            self.btNum = mul
        x, y = -1, 0
        for i in range(mul):
            if x == numX - 1:
                x, y = 0, y + 1
            else:
                x += 1
            rect = pygame.Rect(width * x + self.btAreaRect.left, height * y + self.btAreaRect.top, *self.btRectSize)
            list.append(rect)
        return list

    def initBtList(self):  # 返回按钮列表
        btList = []
        for i in range(self.btNum):
            btObj = Button(self.DISPLAYSURF, self.rectList[i], LTGRAY, BLACK, self.textList[i])
            btList.append(btObj)
        return btList

    def drawWindow(self):  # 绘制窗口
        self.DISPLAYSURF.fill(WHITE)
        drawText(self.DISPLAYSURF, self.hintRect, False, self.hintText, self.hintSize, BLACK, False)
        for i in range(self.btNum):
            self.btList[i].drawButton()
        self.returnBt.drawButton()

    def getClick(self):  # 获得点击按钮的信息
        mousex, mousey = 0, 0
        while True:
            mouseClicked = False
            self.drawWindow()
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouseClicked = True
            # 如果点击“返回”按钮，返回False
            if self.returnBt.onButton(mousex, mousey):
                self.returnBt.highLight(DPGRAY)
                if mouseClicked:
                    return False
            # 点击其余按钮，返回按钮上显示的字符串
            else:
                for button in self.btList:
                    if button.onButton(mousex, mousey):
                        button.highLight(DPGRAY)
                        if mouseClicked:
                            return button.text
                        break
            pygame.display.update()


class Citys:  # 城市列表
    def __init__(self, url, appkey):
        self.list = self.getCitys(url, appkey)

    def getCitys(self, url, appkey):  # 获取能查询的城市列表
        cityRaw = self.getRawInf(url, appkey)
        if cityRaw == None: return None
        cityList = []
        for city in cityRaw:
            citypinyin = "".join(lazy_pinyin(city['district']))
            cityEle = {"city": city['district'], "pinyin": citypinyin}
            cityList.append(cityEle)
        return (cityList)

    def getRawInf(self, url, appkey):  # 从API上得到原始信息
        import json, urllib
        import urllib.request
        from urllib.parse import urlencode
        params = {
            "key": appkey,
            "dtype": "json",
        }
        params = urlencode(params)
        try:
            f = urllib.request.urlopen("%s?%s" % (url, params))
            content = f.read()
            res = json.loads(content)
            if res:
                error_code = res["error_code"]
                if error_code == 0:
                    # 成功请求
                    print("Get citys successfully!")
                    return res["result"]
                else:
                    print("Something error!")
                    return None
            else:
                print("Request api error")
                return None
        except Exception as e:
            print("ERROR: ", e)
            return None

    def findCityByPinyin(self, findPinyin):  # 返回一个有findPinyin为拼音子串的城市列表
        findPinyin = findPinyin.replace(' ', '')
        result = []
        for city in self.list:
            if findPinyin in city["pinyin"]:
                result.append(city['city'])
        if (len(result)):
            return result
        else:
            return False


class WeatherInfo:  # 天气信息
    def __init__(self, url, appkey, city):
        self.error = True
        self.result = self.getFromAPI(url, appkey, city)
        if None != self.result:
            self.error = False
            self.cityName = city
            # 因为有些信息某些城市没有，所以需要异常处理
            self.getLife()
            self.getOthers()

    def getOthers(self):
        try:
            self.pm25 = self.result['data']['pm25']['pm25']
        except KeyError:
            self.pm25 = {'pm25': '查询无结果', 'quality': '查询无结果'}
        try:
            self.date = self.result['data']['life']['date']
        except KeyError:
            self.date = ''
        try:
            self.humidity = self.result['data']['realtime']['weather']['humidity'] + ' %'
        except KeyError:
            self.humidity = '查询无结果'
        try:
            self.weather = self.result['data']['realtime']['weather']['info']
        except KeyError:
            self.weather = '查询无结果'
        try:
            self.temperature = self.result['data']['realtime']['weather']['temperature'] + u'°C'
        except KeyError:
            self.temperature = '查询无结果'
        try:
            self.wind = self.result['data']['realtime']['wind']
        except KeyError:
            self.wind = {'direct': '查询无结果', 'power': '查询无结果'}
        try:
            self.img = self.getImg()
        except KeyError:
            self.img = 'picture/none.png'

    def getLife(self):
        try:
            self.life = self.result['data']['life']['info']
            need = ['chuanyi', 'daisan', 'diaoyu', 'ganmao', 'guomin', 'kongtiao', 'shushidu', 'xiche', 'yundong',
                    'ziwaixian']
            for i in need:
                if not (i in self.life.keys()):
                    self.life[i] = '无建议'
        except KeyError:
            self.life = {'chuanyi': '无建议', 'daisan': '无建议', 'diaoyu': '无建议', 'ganmao': '无建议',
                         'guomin': '无建议', 'kongtiao': '无建议', 'shushidu': '无建议', 'xiche': '无建议',
                         'yundong': '无建议', 'ziwaixian': '无建议'}

    def getImg(self):  # 天气图标获取
        ImgTable = {
            '晴': 'qing.png', '多云': 'duoyun.png', '阴': 'yin.png', '阵雨': 'zhenyu.png',
            '雷阵雨': 'leiyu.png', '雷阵雨伴有冰雹': 'leiyubingbao.png', '雨夹雪': 'yuxue.png',
            '小雨': 'xiaoyu.png', '中雨': 'zhongyu.png', '大雨': 'dayu.png', '暴雨': 'baoyu.png',
            '大暴雨': 'baoyu.png', '特大暴雨': 'baoyu.png', '阵雪': 'zhenxue.png', '小雪': 'xiaoxue.png',
            '中雪': 'zhongxue.png', '大雪': 'daxue.png', '暴雪': 'baoxue.png', '雾': 'wu.png',
            '冻雨': 'dongyu.png', '沙尘暴': 'shachenbao.png', '小到中雨': 'xiaoyu.png',
            '中到大雨': 'zhongyu.png', '大到暴雨': 'dayu.png', '暴雨到大暴雨': 'baoyu.png',
            '大暴雨到特大暴雨': 'baoyu.png', '小到中雪': 'xiaoxue.png', '中到大雪': 'zhongxue.png',
            '大到暴雪': 'daxue.png', '浮尘': 'fuchen.png', '扬沙': 'yangsha.png', '强沙尘暴': 'qiangsha.png',
            '霾': 'mai.png'
        }
        return 'picture/' + ImgTable[self.weather]

    def getFromAPI(self, url, appkey, city):  # 从API接口获得天气信息
        params = {
            "cityname": city,  # 要查询的城市，如：温州、上海、北京
            "key": appkey,
            "dtype": "json",
        }
        params = urlencode(params)
        try:
            f = urllib.request.urlopen("%s?%s" % (url, params))
            content = f.read()
            res = json.loads(content)
            if res:
                error_code = res["error_code"]
                if error_code == 0:
                    # 成功请求
                    print("get weather successfully!")
                    return res["result"]
                else:
                    print("%s:%s" % (res["error_code"], res["reason"]))
                    return None
            else:
                print("request api error")
                return None
        except Exception as e:
            print("ERROR: ", e)
            return None


class WeatherWindow:
    def __init__(self, DISPLAYSURF, backRect):
        self.DISPLAYSURF = DISPLAYSURF
        self.backButton = Button(DISPLAYSURF, backRect, LTGRAY, BLACK, "返回")

    def setInfor(self, url, appkey, city, windowSize, pictureRect):  # 信息与窗口排版初始化
        self.pictureRect = pictureRect
        self.information = WeatherInfo(url, appkey, city)  # 从API获得对应城市的天气信息
        self.windowSize = windowSize
        if not self.information.error:
            # 窗口排版信息(各信息显示位置及显示大小)初始化
            img = pygame.image.load(self.information.img)
            self.surf = pygame.transform.scale(img, pictureRect.size)
            cityRectWidth = windowSize[0] - pictureRect.right - pictureRect.left
            cityRectHeight = int(pictureRect.height * 0.7)
            cityRectTop = pictureRect.top + int(pictureRect.height * 0.3)
            self.tableLeft, self.tableTop = pictureRect.left, pictureRect.bottom + 10
            self.tableWidth = windowSize[0] - pictureRect.left * 2
            self.tableHeight = int(windowSize[1] * 0.90) - self.tableTop
            self.perHeight = int(self.tableHeight / 18)
            self.dateRect = pygame.Rect(pictureRect.right + 10, pictureRect.top, int(self.tableWidth / 2),
                                        self.perHeight)
            self.cityWeatherRect = pygame.Rect(pictureRect.right + 10, cityRectTop, cityRectWidth, cityRectHeight)
            self.tempRect = pygame.Rect(self.tableLeft, self.tableTop, int(self.tableWidth / 2),
                                        int(self.perHeight * 2.75))
            self.humiRect = pygame.Rect(int(windowSize[0] / 2), self.tableTop, int(self.tableWidth / 2),
                                        int(self.perHeight * 2.75))
            self.pm25Rect1 = pygame.Rect(self.tableLeft, self.tableTop + self.perHeight * 3, self.tableWidth,
                                         int(self.perHeight * 2.75))
            self.pm25Rect2 = pygame.Rect(int(windowSize[0] / 2), self.tableTop + self.perHeight * 3, self.tableWidth,
                                         int(self.perHeight * 2.75))
            self.windRect = pygame.Rect(self.tableLeft, self.tableTop + self.perHeight * 6, self.tableWidth,
                                        int(self.perHeight * 2.75))
            self.lifeRectList = {}
            beginTop = self.tableTop + self.perHeight * 9
            for i in self.information.life:
                self.lifeRectList[i] = pygame.Rect(self.tableLeft, beginTop, self.tableWidth, self.perHeight)
                beginTop += self.perHeight

    def drawWindow(self):  # 窗口显示
        if not self.information.error:
            mousex, mousey = 0, 0
            # 信息润色
            liftTitle = {'chuanyi': '穿衣', 'daisan': '带伞', 'diaoyu': '钓鱼', 'ganmao': '感冒', 'guomin': '过敏',
                         'kongtiao': '空调', 'shushidu': '舒适度', 'xiche': '洗车', 'yundong': '运动', 'ziwaixian': '紫外线'}
            liftText = {}
            for i in self.information.life:
                liftText[i] = liftTitle[i] + ": " + self.information.life[i][0] + " (" + self.information.life[i][
                    1] + ")"
            cityWthText = self.information.cityName + "  " + self.information.weather
            pm25Text1 = "PM2.5： " + self.information.pm25['pm25']
            pm25Text2 = "空气质量： " + self.information.pm25['quality']
            windText = "风： " + self.information.wind['direct'] + " " + self.information.wind['power']
            # 显示循环
            while True:
                mouseClicked = False
                self.DISPLAYSURF.fill(WHITE)
                self.backButton.drawButton()  # 返回按钮
                self.DISPLAYSURF.blit(self.surf, self.pictureRect)  # 天气图标
                drawText(self.DISPLAYSURF, self.dateRect, False, self.information.date, self.perHeight, DPGRAY,
                         False)  # 日期显示
                drawText(self.DISPLAYSURF, self.cityWeatherRect, False, cityWthText, self.cityWeatherRect.height, BLACK,
                         False, False)  # 城市名称与天气显示
                drawText(self.DISPLAYSURF, self.tempRect, False, "温度： " + self.information.temperature,
                         self.tempRect.height - 20, BLACK, False)  # 温度显示
                drawText(self.DISPLAYSURF, self.humiRect, False, "湿度： " + self.information.humidity,
                         self.humiRect.height - 20, BLACK, False)  # 湿度显示
                drawText(self.DISPLAYSURF, self.pm25Rect1, False, pm25Text1, self.pm25Rect1.height - 20, BLACK,
                         False)  # PM2.5显示
                drawText(self.DISPLAYSURF, self.pm25Rect2, False, pm25Text2, self.pm25Rect2.height - 20, BLACK,
                         False)  # 空气质量显示
                drawText(self.DISPLAYSURF, self.windRect, False, windText, self.windRect.height - 20, BLACK,
                         False)  # 风向与级数显示
                color1, color2 = DPGRAY, WHITE
                for i in self.information.life:  # 生活建议显示
                    drawText(self.DISPLAYSURF, self.lifeRectList[i], color1, liftText[i], self.perHeight - 6, color2,
                             False, True)
                    color1, color2 = color2, color1
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    elif event.type == MOUSEMOTION:
                        mousex, mousey = event.pos
                    elif event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        mouseClicked = True
                if self.backButton.onButton(mousex, mousey):  # “返回”按钮响应
                    self.backButton.highLight(DPGRAY)
                    if mouseClicked:
                        return False
                pygame.display.update()

    def showError(self, error):  # 显示错误，按返回键退出显示
        self.DISPLAYSURF.fill(WHITE)
        self.backButton.drawButton()
        errorRect = pygame.Rect(int(self.windowSize[0] * 0.15), int(self.windowSize[1] / 3),
                                int(self.windowSize[0] * 0.7), int(self.windowSize[1] / 20))
        drawText(self.DISPLAYSURF, errorRect, False, error, int(self.windowSize[1] / 30), RED, True)
        mousex, mousey = 0, 0
        while True:
            mouseClicked = False
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouseClicked = True
            if self.backButton.onButton(mousex, mousey):
                self.backButton.highLight(DPGRAY)
                if mouseClicked:
                    return
            pygame.display.update()


# 文字显示函数，因重复次数很多，且过程繁琐，故单列一个函数
def drawText(DISPLAYSURF, boxRect, colorBox, text, sizeText, colorText, isCenter, isBold=False):
    fontObj = pygame.font.Font('simkai.ttf', sizeText)
    fontObj.set_bold(isBold)
    if colorBox != False:
        pygame.draw.rect(DISPLAYSURF, colorBox, boxRect)
    textSurfaceObj = fontObj.render(text, True, colorText)
    textRectObj = textSurfaceObj.get_rect()
    if isCenter:
        textRectObj.center = boxRect.center
    else:
        textRectObj.midleft = boxRect.midleft
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
