import tkinter as tk
from tkinter import filedialog, StringVar, Checkbutton
import requests
import threading


class DirScannerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("目录扫描工具")

        # URL输入标签和输入框
        self.url_label = tk.Label(self.master, text="请输入目标URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(self.master, width=50)
        self.url_entry.pack()

        # 协议选择框架
        self.protocol_frame = tk.Frame(self.master)
        self.protocol_frame.pack()
        self.protocol_var_http = StringVar()
        self.protocol_var_https = StringVar()
        self.protocol_check_http = Checkbutton(self.protocol_frame, text="http", variable=self.protocol_var_http, onvalue="http", offvalue="")
        self.protocol_check_http.pack(side=tk.LEFT)
        self.protocol_check_https = Checkbutton(self.protocol_frame, text="https", variable=self.protocol_var_https, onvalue="https", offvalue="")
        self.protocol_check_https.pack(side=tk.LEFT)

        # 线程数量选择标签和输入框
        self.thread_label = tk.Label(self.master, text="请输入线程数量(1-100):")
        self.thread_label.pack()
        self.thread_entry = tk.Entry(self.master, width=10)
        self.thread_entry.pack()

        # 字典文件路径选择标签和按钮
        self.file_label = tk.Label(self.master, text="选择目录字典文件:")
        self.file_label.pack()
        self.file_button = tk.Button(self.master, text="选择文件", command=self.select_file)
        self.file_button.pack()

        # 用于显示选择的字典文件路径的标签
        self.file_path_label = tk.Label(self.master, text="")
        self.file_path_label.pack()

        # 开始扫描按钮
        self.scan_button = tk.Button(self.master, text="开始扫描", command=self.start_scan)
        self.scan_button.pack()

        # 用于显示扫描结果的文本框
        self.result_text = tk.Text(self.master, width=80, height=30)
        self.result_text.pack()

        self.file_path = ""

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        self.file_path_label.config(text=f"已选择字典文件: {self.file_path}")

    def start_scan(self):
        url = self.url_entry.get()
        if not url:
            self.result_text.insert(tk.END, "请输入有效的URL\n")
            return
        if not self.file_path:
            self.result_text.insert(tk.END, "请选择目录字典文件\n")
            return

        thread_count_str = self.thread_entry.get()
        try:
            thread_count = int(thread_count_str)
            if thread_count < 1 or thread_count > 100:
                raise ValueError
        except ValueError:
            self.result_text.insert(tk.END, "请输入1-100之间的有效线程数量\n")
            return

        protocols = []
        if self.protocol_var_http.get():
            protocols.append(self.protocol_var_http.get())
        if self.protocol_var_https.get():
            protocols.append(self.protocol_var_https.get())
        if not protocols:
            self.result_text.insert(tk.END, "请至少选择一种协议\n")
            return

        with open(self.file_path, 'r') as file:
            dir_paths = [line.strip() for line in file]
            total_count = len(dir_paths)
            step = total_count // thread_count
            threads = []
            for i in range(thread_count):
                start_index = i * step
                end_index = (i + 1) * step if i < thread_count - 1 else total_count
                thread = threading.Thread(target=self.scan_directories, args=(url, protocols, dir_paths[start_index:end_index]))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

    def scan_directories(self, url, protocols, dir_paths):
        for dir_path in dir_paths:
            for protocol in protocols:
                full_url = protocol + "://" + url.rstrip('/') + '/' + dir_path.lstrip('/')
                try:
                    response = requests.get(full_url, allow_redirects=False)  # 禁止自动重定向
                    if response.status_code in [301, 302, 303, 307, 308]:  # 判断是否为重定向状态码
                        # 获取原始响应的状态码（重定向之前的状态码）
                        original_status_code = response.status_code
                        # 尝试获取最终的实际状态码（跟随重定向去获取最终页面状态码）
                        final_response = requests.get(full_url)
                        final_status_code = final_response.status_code
                        result_message = f"{full_url} 原始状态码: {original_status_code}，最终状态码: {final_status_code}\n"
                    else:
                        status_code = response.status_code
                        result_message = f"{full_url} 状态码: {status_code}\n"
                    # 在扫描过程中实时插入结果到文本框并更新界面显示
                    self.result_text.insert(tk.END, result_message)
                    self.master.update_idletasks()
                except requests.RequestException as e:
                    error_message = f"{full_url} 出现异常: {str(e)}\n"
                    self.result_text.insert(tk.END, error_message)
                    self.master.update_idletasks()


root = tk.Tk()
app = DirScannerApp(root)
root.mainloop()