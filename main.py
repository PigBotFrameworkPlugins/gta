import sys, time, traceback, datetime, random, requests
from io import BytesIO
sys.path.append('../..')
from bot import bot

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0','referer':'https://gta.julym.com/'}

def is_number(s):
    try:
        return int(s)
    except ValueError:
        pass
    return False

class gta(bot):
    def gta5RockStarID(self):
        try:
            self.send("正在处理...")
            from imageutils.build_image import BuildImage
            from paddleocr import PaddleOCR
            
            captcha = "https://gta.julym.com/captcha.php?r=1134302707"
            send = "https://gta.julym.com/send.php?authcode={}&name={}".format("{}", self.message)
            s = requests.session()
            
            image = BuildImage.open(BytesIO(s.get(url=captcha).content))
            image = image.resize_canvas((image.width, image.height-10), direction="north")
            image = image.resize((image.width+10, image.height+10), bg_color="#fff")
            data = image.save("png").getvalue()
            
            # self.send('[CQ:image,file=https://resourcesqqbot.xzy.center/createimg/{0}]'.format(image.save_png()))
            
            result = PaddleOCR(use_angle_cls = True,use_gpu= False).ocr(data, cls=True)
            str = result[0][-1][-1][0]
            # self.send(str)
            numList = []
            for i in str:
                if i == " " or i == "=":
                    continue
                num = is_number(i)
                if num != False:
                    numList.append(num)
            num = numList[0]
            for i in numList:
                if i == numList[0]:
                    continue
                if '×' in str or 'x' in str:
                    num *= i
                elif '+' in str:
                    num += i
                elif '-' in str:
                    num -= i
                elif '/' in str:
                    num /= i
            # self.send(num)
            
            send = send.format(num)
            data = s.get(url=send).content.decode()
            self.send("[|{}|]".format(data))
        except Exception as e:
            e = traceback.format_exc()
            self.CrashReport(e, "ocr error")
            self.send(e)