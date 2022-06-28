import tkinter as tk
from tkinter.filedialog import askdirectory
from pytube import YouTube
import os
import subprocess

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
        
    def init_parameters(self):      # 建立按鈕跟變數
        self.choice = tk.StringVar()
        self.url = tk.StringVar()
        self.path = tk.StringVar()
        self.name = tk.StringVar()
        self.btnList = []
        
        self.warning = tk.Label(self.win, text="", fg="red")
        self.warning.pack(side=tk.BOTTOM, pady=10)
        
        self.frame1 = tk.Frame(self.win)    # 放置輸入框
        self.frame1.pack(fill=tk.BOTH, expand=tk.YES)
        self.frame2 = tk.Frame(self.win)    # 放置確認訊息
        self.frame3 = tk.Frame(self.win)    # 放置選擇下載類型
        self.frame4 = tk.Frame(self.win)    # 放置解析度選項
        
        self.btnCheck = tk.Button(self.win, text="下一步", width=10, command=self.check_input)
        self.btnCheck.place(x=210, y=150)
        self.btnChoose = tk.Button(self.frame1, text="選擇", width=5, command=self.change_path)
        self.btnChoose.place(x=385, y=67)
        self.btnReady = tk.Button(self.frame2, text="確認", width=10, command=self.click_ready)
        self.btnReady.place(x=210, y=100)
        self.btnRe = tk.Button(self.frame2, text="上一步", width=10, command=self.click_previous)
        self.btnRe.place(x=210, y=60)
        self.btnCV = tk.Button(self.frame3, text="下載影片", width=10, command=self.choose_video)
        self.btnCV.pack(side=tk.TOP, pady=20)
        self.btnDA = tk.Button(self.frame3, text="下載聲音檔", width=10, command=self.download_audio)
        self.btnDA.pack(side=tk.TOP)
        self.btnDV = tk.Button(self.frame4, text="開始下載", width=10, command=self.download_video)
        self.btnDV.place(x=150, y=220)
        self.btnAgain = tk.Button(self.win, text="下載其他影片", width=10, command=self.restart)
        
        self.label1 = tk.Label(self.frame1, text="影片網址: ")
        self.label1.place(x=50, y=30)
        self.label2 = tk.Label(self.frame1, text="存檔位置: ")
        self.label2.place(x=50, y=70)
        self.title = tk.Label(self.frame2, text="")
        self.title.place(x=50, y=5)
        
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
            self.pathdir = self.pathdir.replace("/", "\\")
        
        self.title.config(text="準備下載: "+self.yt.title[0:20]+"...")
        self.btnCheck.place_forget()
        self.entryUrl.config(state='disabled')      # 鎖住輸入框
        self.entryPath.config(state='disabled')
        self.frame2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)
    
    def click_previous(self):
        self.warning.config(text="")
        self.frame2.pack_forget()
        self.btnCheck.place(x=210, y=150)
        self.entryPath.config(state='normal')
        self.entryUrl.config(state='normal')
        
    def click_ready(self):
        self.warning.config(text="")
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)
        self.btnAgain.place(x=210, y=220)
        
    def change_choice(self):
        self.quality = self.choice.get()    # 儲存使用者選擇的數值
        
    def choose_video(self):
        self.frame3.pack_forget()
        List = []
        for item in self.yt.streams.filter(subtype="mp4", type="video").order_by('resolution'): # 建立解析度的選項
            res = item.resolution
            if res not in List:
                List.append(res)
                radioBtn = tk.Radiobutton(self.frame4, text=res+"/ mp4", variable=self.choice, 
                                                value=res, command=self.change_choice)
                radioBtn.pack(pady=5)
                self.btnList.append(radioBtn)
                
        if not self.btnList:
            self.warning.config(text="沒有可供下載的影片")
        else:
            self.btnList[len(self.btnList)-1].select()
            self.quality = res
            self.frame4.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)
        self.btnAgain.place(x=260, y=220)
    
    def download_video(self):
        self.warning.config(text="")
        try:        # 影片有聲音
            self.yt.streams.filter(res=self.quality, subtype="mp4", progressive=True).first().download(self.pathdir)
            self.warning.config(text="下載完成！", fg="green")
        except:     # 影片無聲音，須個別下載影片及聲音檔再合併
            self.warning.config(text="合併影片及聲音中，請稍後...", fg="red")
            try:
                self.yt.streams.filter(res=self.quality, subtype="mp4", type="video").first().download(self.pathdir)
                v_name = self.yt.streams.filter(res=self.quality, subtype="mp4", type="video").first().default_filename
                tmp_video_path = os.path.join(self.pathdir, "video.mp4")
                os.rename(os.path.join(self.pathdir, v_name), tmp_video_path)
                
                self.yt.streams.filter(type="audio").last().download(self.pathdir)
                a_name = self.yt.streams.filter(type="audio").last().default_filename
                tmp_audio_path = os.path.join(self.pathdir, "audio.mp3")
                os.rename(os.path.join(self.pathdir, a_name), tmp_audio_path)
                
                had_download = True
            except:
                self.warning.config(text="下載失敗！")
                had_download = False
            
            if had_download:
                tmp_output = os.path.join(self.pathdir, "output.mp4")
                cmd = f'ffmpeg -i {tmp_video_path} -i {tmp_audio_path} \ -map 0:v -map 1:a -c copy -y {tmp_output}'
                try:
                    
                    subprocess.call(cmd, shell=True)
                    os.rename(tmp_output, os.path.join(self.pathdir, "output.mp4"), os.path.join(self.pathdir, v_name))
                    #os.remove(tmp_audio_path)
                    #os.remove(tmp_video_path)   
                    
                    self.warning.config(text="下載完成！", fg="green")
                except:
                    self.warning.config(text="影片合併失敗")
            else:
                pass
            
    def download_audio(self):
        self.warning.config(text="")
        try:
            self.yt.streams.filter(type="audio").last().download(self.pathdir)
            a_name = self.yt.streams.filter(type="audio").last().default_filename
            os.rename(os.path.join(self.pathdir, a_name), os.path.join(self.pathdir, a_name+".mp3"))
            self.warning.config(text="下載完成！", fg="green")
        except:
            self.warning.config(text="下載失敗！", fg="red")
    
    def restart(self):      # 重設視窗
        self.warning.config(text="", fg="red")
        self.btnAgain.place_forget()
        if not self.btnList:
            self.frame3.pack_forget()
        else:
            for radioBtn in self.btnList:
                radioBtn.pack_forget()
            self.btnList = []
            self.frame4.pack_forget()
        self.frame1.pack(fill=tk.BOTH, expand=tk.YES)
        self.entryPath.config(state='normal')
        self.entryUrl.config(state='normal')
        self.btnCheck.place(x=210, y=150)
        self.url.set("")
    
def main():
    YTDownloader()

if __name__ == '__main__':
    main()