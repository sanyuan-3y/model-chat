import configparser
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from openai import OpenAI

# 配置文件路径
CONFIG_FILE = "config.ini"

# 模拟获取模型平台下的模型列表
def get_models(platform):
    if platform == "DeepSeek":
        return ["deepseek-model-1", "deepseek-model-2"]
    elif platform == "ZhiPuAI":
        return ["zhipuai-model-1", "zhipuai-model-2"]
    elif platform == "OpenAI":
        return ["gpt-3.5-turbo", "gpt-4"]
    else:
        return []

# 获取当前选择模型平台下开放的模型
def get_model_list(platform):
    client.models.list()

# 更新模型下拉框的内容
def update_models(event=None):
    selected_platform = platform_combobox.get()
    models = get_models(selected_platform)
    model_combobox['values'] = models
    if models:
        model_combobox.current(0)
    else:
        model_combobox.set('')

# 确定按钮点击事件
def on_confirm():
    platform = platform_combobox.get()
    api_key = api_key_entry.get()
    model = model_combobox.get()

    config = configparser.ConfigParser()
    config["ModelConfig"] = {
        "platform": platform,
        "api_key": api_key,
        "model": model
    }
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

    messagebox.showinfo("成功", "配置已保存！")

# 取消按钮点击事件
def on_start():
    platform = platform_combobox.get()
    api_key = api_key_entry.get()
    model = model_combobox.get()

    # 校验字段是否为空
    if not platform:
        messagebox.showwarning("警告", "请选择模型平台！")
        return
    if not api_key:
        messagebox.showwarning("警告", "请输入 API Key！")
        return
    if not model:
        messagebox.showwarning("警告", "请选择模型！")
        return

    # 如果所有字段都有值，跳转到对话界面
    show_chat()

# 载入配置文件
def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        if "ModelConfig" in config:
            return config["ModelConfig"]
    return None

# 填充配置到界面
def fill_config_to_ui():
    config = load_config()
    if config:
        platform_combobox.set(config.get("platform", ""))
        api_key_entry.insert(0, config.get("api_key", ""))
        model_combobox.set(config.get("model", ""))
        update_models()

# 复制api_key
def copy_api_key():
    copy_api_key = api_key_entry.get()
    if copy_api_key:
        root.clipboard_clear()  # 清空剪贴板
        root.clipboard_append(copy_api_key)  # 将 API Key 添加到剪贴板
        messagebox.showinfo("成功", "API Key 已复制到剪贴板！")
    else:
        messagebox.showwarning("警告", "API Key 为空，无法复制！")

# 创建一个自定义按钮样式的函数
def create_styled_button(parent, text, command=None):
    # 创建 Canvas 绘制圆角矩形按钮
    button = tk.Button(parent, text=text, command=command, relief="flat",
                       fg="white", bg="#409EFF", activebackground="#66b1ff",
                       activeforeground="white", font=("微软雅黑", 10, "bold"),
                       bd=0, padx=10, pady=3, highlightthickness=0)

    # 按钮的圆角效果可以通过 canvas 绘制
    button.configure(highlightthickness=0)  # 去掉按钮外的高亮
    return button

# 创建主窗口
root = tk.Tk()
root.title("AI 助手")
root.geometry("900x600")  # 初始分辨率

# 设置窗口背景颜色
root.configure(bg="white")

# 创建左侧导航栏
navigation_frame = tk.Frame(root, width=100, bg="#f0f0f0")
navigation_frame.pack(side=tk.LEFT, fill=tk.Y)

def on_chat_click(event):
    show_chat()

def on_config_click(event):
    show_config()
    fill_config_to_ui()

# 设置固定宽度
label_width = 13

# 导航栏文本
chat_label = tk.Label(navigation_frame, text="对话", bg="#f0f0f0", fg="black", font=("微软雅黑", 13), width=label_width)
chat_label.pack(pady=10)
chat_label.bind("<Button-1>", on_chat_click)  # 绑定左键点击事件

config_label = tk.Label(navigation_frame, text="配置", bg="#f0f0f0", fg="black", font=("微软雅黑", 13), width=label_width)
config_label.pack(pady=10)
config_label.bind("<Button-1>", on_config_click)  # 绑定左键点击事件

# 创建右侧内容区域
content_frame = tk.Frame(root, bg="white")
content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# 对话界面
chat_frame = tk.Frame(content_frame, bg="white")
chat_frame.pack(fill=tk.BOTH, expand=True)

# 创建底部浅蓝色阴影区域
bottom_shadow_frame = tk.Frame(chat_frame, bg="#E0E0E0", height=80)  # 浅蓝色阴影
bottom_shadow_frame.pack(fill=tk.X, side=tk.BOTTOM)

# 在阴影区域中添加文本框和发送按钮
input_frame = tk.Frame(bottom_shadow_frame, bg="#E0E0E0")
input_frame.pack(fill=tk.BOTH, padx=2, pady=2)  # 缩小间距为 2 像素

# 使用 grid 布局管理器
input_frame.grid_columnconfigure(0, weight=1)  # 文本框占满剩余空间
input_frame.grid_columnconfigure(1, weight=0)  # 发送按钮固定宽度

# 创建文本框
input_text = tk.Text(input_frame, font=("微软雅黑", 12), height=3, wrap=tk.WORD)
input_text.grid(row=0, column=0, sticky="ew", padx=(0, 5))  # 文本框占满剩余空间，右侧留 5 像素间距

# 创建发送按钮
send_button = tk.Button(input_frame, text="发送", font=("微软雅黑", 12), bg="#409EFF", fg="white", relief="flat", width=10, height=3)
send_button.grid(row=0, column=1, sticky="e")  # 发送按钮固定在右侧

# 配置界面
config_frame = tk.Frame(content_frame, bg="white")

# 模型平台
platform_label = tk.Label(config_frame, text="模型平台:", bg="white", fg="black", font=("微软雅黑", 13))
platform_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
platform_combobox = ttk.Combobox(config_frame, values=["DeepSeek", "ZhiPuAI", "OpenAI"])
platform_combobox.grid(row=0, column=1, padx=10, pady=10, sticky=tk.EW)
platform_combobox.bind("<<ComboboxSelected>>", update_models)

# API Key
api_key_label = tk.Label(config_frame, text="API Key:", bg="white", fg="black", font=("微软雅黑", 13))
api_key_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
api_key_entry = tk.Entry(config_frame, show="*")
api_key_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)

copy_button = tk.Button(config_frame, text="copy", command=copy_api_key)
copy_button.grid(row=1, column=2, padx=10, pady=10)


# 模型
model_label = tk.Label(config_frame, text="模型:", bg="white", fg="black", font=("微软雅黑", 13))
model_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
model_combobox = ttk.Combobox(config_frame)
model_combobox.grid(row=2, column=1, padx=10, pady=10, sticky=tk.EW)
update_models()  # 初始化模型下拉框

# 确定/取消按钮
button_frame = tk.Frame(config_frame, bg="white")
button_frame.grid(row=3, column=0, columnspan=3, pady=20)

confirm_button = create_styled_button(button_frame, "确定", on_confirm)
confirm_button.pack(side=tk.LEFT, padx=10)

start_button = create_styled_button(button_frame, "start chat", on_start)
start_button.pack(side=tk.LEFT, padx=10)

# 默认显示对话界面
config_frame.pack_forget()

# 切换界面函数
def show_chat():
    config_frame.pack_forget()
    chat_frame.pack(fill=tk.BOTH, expand=True)

def show_config():
    chat_frame.pack_forget()
    config_frame.pack(fill=tk.BOTH, expand=True)

# 创建客户端
client = OpenAI(api_key="sk-b6c5776beadd49108d030f56bb9c8e50", base_url="https://api.deepseek.com")

# 运行主循环
root.mainloop()