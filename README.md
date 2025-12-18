# DesktopSticker / 桌面贴图

[中文](#chinese) | [English](#english)

---

<a name="chinese"></a>
## 中文

**DesktopSticker (桌面贴图)** 是一款基于 Python 编写的轻量级 Windows 桌面工具。它可以将图片“贴”在你的桌面上，就像便利贴一样。非常适合用来放置备忘录、参考图表或任何你需要经常看到的重要内容。

### 功能特点

*   **桌面层级显示**：图片贴在桌面层，不会置顶遮挡浏览器或其他正在使用的软件窗口（按 Win+D 显示桌面时可见）。
*   **自由拖拽**：按住图片任意位置即可拖动，调整位置。
*   **自由缩放**：
    *   **鼠标滚轮**：鼠标悬停在图片上滚动滚轮即可快速放大缩小。
    *   **右键菜单**：选择“调整大小...”可输入精确宽度。
*   **便捷换图**：右键菜单一键更换显示的图片。
*   **开机自启**：右键菜单中提供“开机自启”选项，勾选后软件随系统启动。
*   **极低占用**：使用 Python 原生 Tkinter 库，内存和 CPU 占用极低。

### 使用说明

#### 环境要求
*   Windows 操作系统
*   已安装 Python 3.x
*   `Pillow` 库

#### 安装与运行

1.  下载本项目代码。
2.  安装依赖库：
    ```bash
    pip install -r requirements.txt
    ```
3.  **运行软件**：
    *   直接双击 `run.bat` 文件（推荐）。
    *   或者在命令行运行：`python main.py`

#### 操作指南
*   **首次运行**：屏幕上会出现一个灰色方块。**右键点击**它，选择 **“更换图片...”** 来选择你想贴的图片。
*   **移动图片**：按住图片拖动即可。
*   **缩放图片**：滚动鼠标滚轮，或右键选择“调整大小”。
*   **关闭软件**：右键点击图片，选择“关闭贴图”。

---

<a name="english"></a>
## English

**DesktopSticker** is a lightweight Windows application written in Python that allows you to pin images to your desktop. It acts like a digital sticky note for images, perfect for keeping important information, reminders, or reference charts visible on your desktop wallpaper.

### Features

*   **Desktop Integration**: Images are pinned to the desktop layer (not "always on top"), so they don't block your active windows.
*   **Draggable**: Easily move the image anywhere on your screen by dragging it.
*   **Resizable**:
    *   **Mouse Wheel**: Hover over the image and scroll to zoom in/out.
    *   **Right-click Menu**: Select "Resize..." for precise pixel-width adjustment.
*   **Easy Image Swapping**: Right-click to change the displayed image instantly.
*   **Auto-Start**: Optional "Start with Windows" feature in the right-click menu.
*   **Lightweight**: Built with Tkinter, consuming minimal system resources.

### Getting Started

#### Prerequisites
*   Windows OS
*   Python 3.x installed
*   `Pillow` library

#### Installation & Run

1.  Clone this repository or download the source code.
2.  Install the required dependency:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application**:
    *   Double-click `run.bat` (Recommended for Windows users).
    *   Or run via command line: `python main.py`

#### Usage
*   **First Run**: A gray box will appear. Right-click it and select **"Change Image..."** to pick your image.
*   **Move**: Click and drag the image.
*   **Resize**: Scroll mouse wheel or use the right-click menu.
*   **Close**: Right-click and select "Close".

---

## 许可证 / License

本项目采用 **[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh)** 国际许可协议进行许可。

[![CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh)

这意味着您可以：
*   **共享** — 在任何媒介以任何形式复制、发行本作品。
*   **演绎** — 修改、转换或以本作品为基础进行创作。

但必须遵守以下条件：
1.  **署名 (Attribution)** — 您必须给出适当的署名，提供指向本许可协议的链接，同时标明是否（对原始作品）作了修改。
2.  **非商业性使用 (NonCommercial)** — 您**不得**将本作品用于商业目的。
3.  **相同方式共享 (ShareAlike)** — 如果您再混合、转换或者基于本作品进行创作，您必须基于**与原先许可协议相同的许可协议**分发您贡献的作品（即必须开源且同样禁止商用）。

---
Copyright (c) 2025 [Your Name]
