import tkinter as tk
from tkinter.filedialog import askdirectory
from pytube import YouTube

class YTDownloader:
    def __init__(self):
        self.init_win()
        self.init_parameters()
        self.win.mainloop()
        
    def init_win(self):     # 建立視窗
        self.win = tk.Tk()
        self.win.geometry("500x300")
        self.win.resizable(False,False)
        self.win.title("YT下載器")
        self.win.iconbitmap('icon.ico')
        
    def init_parameters(self):      # 建立按鈕跟變數
        self.choice = tk.StringVar()
        self.url = tk.StringVar()
        self.path = tk.StringVar()
        self.name = tk.StringVar()
        self.btnList = []
        
        self.warning = tk.Label(self.win, text="", fg="red")
        self.warning.pack(side=tk.BOTTOM, pady=10)
        
        self.frame1 = tk.Frame(self.win)    # 放置輸入框的框架
        self.frame1.pack(fill=tk.BOTH, expand=tk.YES)
        self.frame2 = tk.Frame(self.win)    # 放置按鈕的框架
        # 用兩個框架切換，達到切換上下頁的效果
        
        self.btnCheck = tk.Button(self.win, text="下一步", width=10, command=self.check_input)
        self.btnCheck.place(x=210, y=150)
        self.btnChoose = tk.Button(self.frame1, text="選擇", width=5, command=self.change_path)
        self.btnChoose.place(x=385, y=67)
        self.btnReady = tk.Button(self.frame2, text="確認", width=10, command=self.click_ready)
        self.btnReady.place(x=210, y=90)
        self.btnRe = tk.Button(self.frame2, text="上一步", width=10, command=self.click_previous)
        self.btnRe.place(x=210, y=60)
        self.btnCV = tk.Button(self.win, text="下載影片", width=10, command=self.choose_video)
        self.btnCM = tk.Button(self.win, text="下載聲音檔", width=10, command=self.choose_music)
        self.btnDV = tk.Button(self.win, text="開始下載", width=10, command=self.download_video)
        self.btnDM = tk.Button(self.win, text="開始下載", width=10, command=self.download_music)
        self.btnAgain = tk.Button(self.win, text="下載其他影片", width=10, command=self.restart)
        
        self.label1 = tk.Label(self.frame1, text="影片網址: ")
        self.label1.place(x=50, y=30)
        self.label2 = tk.Label(self.frame1, text="存檔位置: ")
        self.label2.place(x=50, y=70)
        self.title = tk.Label(self.frame2, text="")
        self.title.place(x=100, y=10)
        
        self.entryUrl = tk.Entry(self.frame1, textvariable=self.url)    # 輸入框
        self.entryUrl.config(width=45)
        self.entryUrl.place(x=120, y=30)
        self.entryPath = tk.Entry(self.frame1, textvariable=self.path)
        self.entryPath.config(width=35)
        self.entryPath.place(x=120, y=70)
       
    def change_path(self):
        tmp = askdirectory()    # 讓使用者選擇存檔位置
        self.path.set(tmp)
    
    def check_input(self):
        self.warning.config(text="")
        
        if(self.url.get()==""):
            self.warning.config(text="請輸入網址")
            return
        else:
            try:
                self.yt = YouTube(self.url.get())
            except:
                self.warning.config(text="網址錯誤，請重新輸入網址")
                return
        
        if(self.path.get()==""):
            self.warning.config(text="請選擇或輸入存檔位置")
            return
        else:
            self.pathdir = self.path.get()
            self.pathdir = self.pathdir.replace("\\", "\\\\")
        
        self.name = self.yt.title
        self.title.config(text="準備下載: "+self.name[0:20]+"...")
        self.btnCheck.place_forget()
        self.entryUrl.config(state='disabled')      # 鎖住輸入框
        self.entryPath.config(state='disabled')
        self.frame2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)
    
    def click_previous(self):
        self.warning.config(text="")    # 從frame1切換回frame2
        self.frame2.pack_forget()
        self.btnCheck.place(x=210, y=150)
        self.entryPath.config(state='normal')
        self.entryUrl.config(state='normal')
        
    def click_ready(self):
        self.warning.config(text="")    # 選擇要下載影片還是聲音檔
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        
        self.btnCV.pack(side=tk.TOP, pady=20)
        self.btnCM.pack(side=tk.TOP)
        
    def change_choice(self):
        self.quality = self.choice.get()    # 儲存使用者選擇的數值
        
    def choose_video(self):
        self.btnCV.pack_forget()
        self.btnCM.pack_forget()
        List = []
        for item in self.yt.streams.filter(subtype="mp4", progressive=True).order_by('resolution'):
            res = item.resolution
            if res not in List:
                List.append(res)
                radioBtn = tk.Radiobutton(self.win, text=res+"/ mp4", variable=self.choice, 
                                                value=res, command=self.change_choice)
                # 建立解析度的選項
                radioBtn.pack(pady=5)
                self.btnList.append(radioBtn)
        self.btnList[0].select()
        self.btnDV.place(x=210, y=200)
        self.btnAgain.place(x=210, y=230)
    
    def download_video(self):
        self.warning.config(text="")
        try:
            self.yt.streams.filter(res=self.quality, subtype="mp4", progressive=True).first().download(self.pathdir)
            self.warning.config(text="下載完成！", fg="green")
        except:
            self.warning.config(text="下載失敗！", fg="red")
    
    def choose_music(self):
        self.btnCV.pack_forget()
        self.btnCM.pack_forget()
        List = []
        for item in self.yt.streams.filter(type="audio").order_by('abr'):
            abr = item.abr
            if abr not in List:
                List.append(abr)
                radioBtn = tk.Radiobutton(self.win, text=abr+"/ mp3", variable=self.choice, 
                                                value=abr, command=self.change_choice)
                # 建立品質的選項
                radioBtn.pack(pady=5)
                self.btnList.append(radioBtn)
        self.btnList[0].select()
        self.btnDM.place(x=210, y=200)
        self.btnAgain.place(x=210, y=230)
        
    def download_music(self):
        self.warning.config(text="")
        try:
            self.yt.streams.filter(abr=self.quality, type="audio").first().download(self.pathdir)
            self.warning.config(text="下載完成！", fg="green")
        except:
            self.warning.config(text="下載失敗！", fg="red")
    
    def restart(self):
        self.warning.config(text="", fg="red")      # 重設視窗
        self.btnAgain.place_forget()
        self.btnDM.place_forget()
        self.btnDV.place_forget()
        for radioBtn in self.btnList:
            radioBtn.pack_forget()
        self.btnList = []
        self.frame1.pack(fill=tk.BOTH, expand=tk.YES)
        self.entryPath.config(state='normal')
        self.entryUrl.config(state='normal')
        self.btnCheck.place(x=210, y=150)
        self.url.set("")
    
def main():
    YTDownloader()

if __name__ == '__main__':
    main()