#version 0.3 to 0.4



from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.core.window import Window

from kivy.uix.button import Button

import random

from PIL import Image as pimage


global setka


global raskus
raskus=0

def crop(crops, wind, k):
    im = pimage.open('windy.jpg')
    im=im.transform((3000,3000), pimage.EXTENT, data=(0,0,im.size[0], im.size[1]), resample=0, fill=1)
    p=pimage.open('00.jpg')
    p = p.transform((int(.9*wind/crops), int(.9*wind/crops)), pimage.EXTENT, data=(0, 0, p.size[0], p.size[1]), resample=0, fill=1).save('00.jpg')

    imgwidth, imgheight = im.size
    height = int(im.size[1]/crops)
    width = int(im.size[0]/crops)

    for i in range(0,imgheight,height):
        for j in range(0,imgwidth,width):
            box = (j, i, j+width, i+height)
            a = im.crop(box)
            a=a.transform((int(.9*wind/crops), int(.9*wind/crops)), pimage.EXTENT, data=(0, 0, width,height), resample=0, fill=1)

            a.save(str(k)+".jpg")
            a.close()

            k += 1
    im.close()
    return k-1

def valima(self):
    sl = BoxLayout(orientation='vertical')
    sl.add_widget(Button(text="для салаг", on_release=self.valibut))
    sl.add_widget(Button(text="золотой стандарт", on_release=self.valibut))
    sl.add_widget(Button(text="я уже смешарик", on_release=self.valibut))
    sl.add_widget(Button(text="только для В.В.", on_release=self.valibut))
    return sl



class PazlApp(App):
    def build(self):
        global ans, setka, k
        setka=[]
        bl=BoxLayout(orientation='vertical')
        if raskus==0: bl.add_widget(valima(self))
        else :
            k=crop(raskus,Window.width, 1)

            for i in range(k):
                setka.append(str(i+1))
            setka.append('00')
            global gl, al
            al=AnchorLayout(size_hint=[1,1])
            gl=GridLayout(cols=raskus, rows=raskus,spacing=1, size=[.9*Window.width,.9*Window.width], size_hint_max_y=Window.width*.9)

            ans=setka[:k]
            while setka[-1]=='00':
                random.shuffle(setka)
            print(setka, ans)
            for i in range(k):
                if setka[i]=='00': gl.add_widget(ImageB(text=str(i), source=setka[i]+'.jpg'))
                else: gl.add_widget(ImageB(text=str(i), source=setka[i]+'.jpg', on_release=self.ppress))

            al.add_widget(gl)
            bl.add_widget(al)


            bl.add_widget(Button(text="restart", size_hint=[.5,.1], on_release=self.restartpress))

        return bl



    def valibut(self, instance):
        global raskus
        if instance.text=="только для В.В.": raskus=12
        elif instance.text=="я уже смешарик": raskus=8
        elif instance.text=="золотой стандарт": raskus=4
        elif instance.text=="для салаг": raskus=2
        self.stop()
        self.run()


    def restartpress(self,instance):
        global raskus
        self.stop()
        raskus=0
        self.run()

    def ppress(self,instance):
        global k, raskus
        pos=setka.index('00')
        sov=0
        t=int(instance.text)
        if pos == t+1 or pos == t-1 or pos == t+raskus or pos == t-raskus:
            setka[pos]=setka[t]
            setka[t]='00'
            gl.clear_widgets()
            for i in range(k):
                if setka[i] == '00':
                    gl.add_widget(ImageB(text=str(i), source=setka[i]+'.jpg'))
                else:
                    gl.add_widget(ImageB(text=str(i), source=setka[i]+'.jpg', on_release=self.ppress))
                if setka[i]==ans[i]: sov+=1

        if sov>k-2:
            print("win!!!!")
            al.add_widget(Button(text="WIN!!!", size_hint=[.5, .5], font_size=50, background_color=[.5,.2,.1,.5], on_release=self.restartpress))



class ImageB(ButtonBehavior, Image):
    def __init__(self, text, source, **kwargs):
        super(ImageB, self).__init__(**kwargs)
        self.text=text
        self.source=source

    def on_press(self):
        if self.source=='00.jpg': print("nothing")

if __name__ == "__main__": PazlApp().run()



#buildozer android debug
#cd /home/sanya/progs/gamescompilation