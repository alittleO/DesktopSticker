import tkinter as tk
from tkinter import filedialog, messagebox, Menu, simpledialog
from PIL import Image, ImageTk
import os
import sys
import json
import winreg
import ctypes
import uuid

# 尝试开启高 DPI 感知，解决在高分辨率屏幕下模糊的问题
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

# 获取当前脚本所在目录，确保配置文件和图片路径正确
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

class StickerWindow:
    def __init__(self, master, manager, sticker_id, config_data):
        self.root = master
        self.manager = manager
        self.sticker_id = sticker_id
        self.config_data = config_data
        
        # --- 窗口设置 ---
        self.root.title("桌面贴图")
        self.root.overrideredirect(True) # 无边框
        self.root.attributes("-topmost", False) # 不置顶
        try:
            self.root.attributes("-toolwindow", True)
        except:
            pass

        # --- 变量初始化 ---
        self.image_path = self.config_data.get("image_path", "")
        self.tk_image = None
        self.original_image = None
        self.drag_data = {"x": 0, "y": 0}
        
        # --- UI 组件 ---
        self.label = tk.Label(self.root, bg='white', bd=0)
        self.label.pack(fill="both", expand=True)
        
        # --- 初始化逻辑 ---
        self.load_image()
        
        # 恢复位置
        x = self.config_data.get("x", 200)
        y = self.config_data.get("y", 200)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        if x > screen_width - 50: x = 0
        if y > screen_height - 50: y = 0
        self.root.geometry(f"+{x}+{y}")

        # --- 事件绑定 ---
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.label.bind("<ButtonRelease-1>", self.stop_move)
        self.label.bind("<MouseWheel>", self.on_mouse_wheel)
        self.label.bind("<Button-3>", self.show_menu)

        # --- 右键菜单 ---
        self.menu = Menu(self.root, tearoff=0)
        self.menu.add_command(label="新建贴图", command=self.manager.create_new_sticker)
        self.menu.add_command(label="更换图片...", command=self.choose_image)
        self.menu.add_command(label="调整大小...", command=self.ask_resize)
        
        self.auto_start_var = tk.BooleanVar()
        self.check_autostart_status()
        self.menu.add_checkbutton(label="开机自启", variable=self.auto_start_var, command=self.toggle_autostart)
        
        self.menu.add_separator()
        self.menu.add_command(label="关闭此贴图", command=self.close_sticker)
        self.menu.add_command(label="退出程序", command=self.manager.quit_app)

    def load_image(self):
        if not self.image_path or not os.path.exists(self.image_path):
            self.label.config(text="[ 右键菜单 -> 更换图片 ]\n\n可拖动 · 可缩放\n右键新建更多", 
                              font=("Microsoft YaHei", 12), 
                              width=25, height=8, 
                              bg="#f0f0f0", fg="#333")
            self.label.config(image="")
            self.original_image = None
            return

        try:
            self.original_image = Image.open(self.image_path)
            w = self.config_data.get("width", self.original_image.width)
            self.update_display_image(w, 0)
        except Exception as e:
            self.label.config(text=f"图片加载失败:\n{e}", bg="red", fg="white")
            self.original_image = None

    def update_display_image(self, width, height):
        if not self.original_image: return
        aspect_ratio = self.original_image.width / self.original_image.height
        final_w = int(width)
        final_h = int(final_w / aspect_ratio)
        try:
            img_resized = self.original_image.resize((final_w, final_h), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(img_resized)
            self.label.config(image=self.tk_image, text="", width=0, height=0, bg='white')
            self.root.geometry(f"{final_w}x{final_h}")
            
            # 更新配置数据
            self.config_data["width"] = final_w
            self.config_data["height"] = final_h
        except Exception as e:
            print(f"缩放失败: {e}")

    def start_move(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def do_move(self, event):
        deltax = event.x - self.drag_data["x"]
        deltay = event.y - self.drag_data["y"]
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def stop_move(self, event):
        self.config_data["x"] = self.root.winfo_x()
        self.config_data["y"] = self.root.winfo_y()
        self.manager.save_config()

    def on_mouse_wheel(self, event):
        if not self.original_image: return
        scale = 1.1 if event.delta > 0 else 0.9
        current_w = self.root.winfo_width()
        new_w = int(current_w * scale)
        if new_w < 50: new_w = 50
        self.update_display_image(new_w, 0)
        self.manager.save_config()

    def ask_resize(self):
        if not self.original_image: return
        current_w = self.root.winfo_width()
        new_w = simpledialog.askinteger("调整大小", "请输入新的宽度 (像素):", initialvalue=current_w, minvalue=50, maxvalue=5000)
        if new_w:
            self.update_display_image(new_w, 0)
            self.manager.save_config()

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def choose_image(self):
        path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("图片文件", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp")]
        )
        if path:
            self.image_path = path
            self.config_data["image_path"] = path
            # 重置大小为原图大小，或者保持当前大小？通常换图后重置大小比较合理
            self.config_data.pop("width", None)
            self.config_data.pop("height", None)
            self.load_image()
            self.manager.save_config()

    def close_sticker(self):
        self.manager.remove_sticker(self.sticker_id)

    def check_autostart_status(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
            try:
                winreg.QueryValueEx(key, "DesktopStickerApp")
                self.auto_start_var.set(True)
            except FileNotFoundError:
                self.auto_start_var.set(False)
            winreg.CloseKey(key)
        except:
            self.auto_start_var.set(False)

    def toggle_autostart(self):
        python_exe = sys.executable.replace("python.exe", "pythonw.exe")
        if not os.path.exists(python_exe):
            python_exe = sys.executable
        script_path = os.path.abspath(__file__)
        cmd = f'"{python_exe}" "{script_path}"'
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
            if self.auto_start_var.get():
                winreg.SetValueEx(key, "DesktopStickerApp", 0, winreg.REG_SZ, cmd)
            else:
                try:
                    winreg.DeleteValue(key, "DesktopStickerApp")
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
        except Exception as e:
            messagebox.showerror("错误", f"无法设置开机自启权限:\n{e}")
            self.auto_start_var.set(not self.auto_start_var.get())

class StickerManager:
    def __init__(self, root):
        self.root = root
        self.root.withdraw() # 隐藏主窗口
        self.stickers = {} # id -> window_instance
        self.config = self.load_config()
        
        if not self.config.get("stickers"):
            self.create_new_sticker()
        else:
            for s_conf in self.config["stickers"]:
                self.create_window(s_conf)
    
    def load_config(self):
        config = {}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding='utf-8') as f:
                    data = json.load(f)
                    # 兼容旧版本配置
                    if "stickers" not in data:
                        # 如果是旧的扁平结构，转换为新的列表结构
                        if "image_path" in data or "x" in data:
                            new_sticker = data.copy()
                            new_sticker["id"] = str(uuid.uuid4())
                            config = {"stickers": [new_sticker]}
                        else:
                            config = {"stickers": []}
                    else:
                        config = data
            except:
                config = {"stickers": []}
        else:
            config = {"stickers": []}
        return config

    def save_config(self):
        # config["stickers"] 已经在各个 StickerWindow 中被实时修改了引用
        # 这里只需要 dump 即可
        try:
            with open(CONFIG_FILE, "w", encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")

    def create_new_sticker(self):
        new_id = str(uuid.uuid4())
        # 默认位置稍微错开一点
        offset = len(self.stickers) * 20
        default_conf = {
            "id": new_id, 
            "x": 200 + offset, 
            "y": 200 + offset,
            "image_path": ""
        }
        self.config["stickers"].append(default_conf)
        self.create_window(default_conf)
        self.save_config()

    def create_window(self, conf):
        # 使用 Toplevel 创建独立窗口
        window = tk.Toplevel(self.root)
        app = StickerWindow(window, self, conf["id"], conf)
        self.stickers[conf["id"]] = app

    def remove_sticker(self, sticker_id):
        if sticker_id in self.stickers:
            # 销毁窗口
            self.stickers[sticker_id].root.destroy()
            del self.stickers[sticker_id]
            
            # 从配置中移除
            self.config["stickers"] = [s for s in self.config["stickers"] if s["id"] != sticker_id]
            self.save_config()
            
            # 如果所有贴图都关闭了，退出程序
            if not self.stickers:
                self.quit_app()

    def quit_app(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = StickerManager(root)
    root.mainloop()
