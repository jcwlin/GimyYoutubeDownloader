# 🎬 Video Downloader 影片下載器

**English** | [中文](#中文-1)

A powerful cross-platform video downloader supporting Gimy websites and YouTube. Built with PyQt6 for a beautiful, modern UI.

## Features 功能特色

- 📥 **Multi-source Download** 多來源下載: Supports Gimy websites and YouTube links
- 🌐 **Multi-language** 多語言支援: 4 languages (繁體中文、简体中文、English、Español)
- 🎬 **Batch Download** 批次下載: Download up to 5 videos simultaneously
- 📊 **Real-time Progress** 即時進度: Visual progress bars with live updates
- 🎯 **Smart Organization** 智慧分類: Automatically creates folders for each video
- ⏸️ **Task Management** 任務管理: Cancel, pause, or remove downloads
- 🖱️ **Context Menu** 右鍵選單: Right-click to open folder or remove tasks
- 🎨 **Modern UI** 現代化介面: Beautiful card-based layout with intuitive controls

## Cross-Platform Support 跨平台支援

This application works on:
- **macOS** (tested on macOS 15.1.1)
- **Windows** (Windows 10/11)
- **Linux** (Ubuntu, Fedora, etc.)

## Installation 安裝方式

### Requirements 系統需求
- Python 3.8 or higher
- PyQt6
- yt-dlp
- requests

### Step-by-Step Installation 逐步安裝

#### macOS
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install yt-dlp via Homebrew (recommended)
brew install yt-dlp

# Or via pip
pip install yt-dlp
```

#### Windows
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install yt-dlp
pip install yt-dlp
```

#### Linux (Ubuntu/Debian)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install yt-dlp
sudo apt install yt-dlp

# For opening folders in file manager
sudo apt install xdg-utils
```

## Usage Guide 使用指南

### 1. Launch the Application 啟動應用程式
```bash
python video_downloader.py
```

### 2. Interface Overview 介面概覽

```
┌─────────────────────────────────────────────────┐
│ 🌐 Language: [繁體中文▼]                          │
├─────────────────────────────────────────────────┤
│ 📁 1. 選擇儲存位置                                │
│ [Downloads__________________] [🔍 瀏覽...]       │
├─────────────────────────────────────────────────┤
│ 🔗 2. 新增下載連結                                │
│ [支援多個連結，一行一個...]                        │
│ [🔗 URL input area]                             │
│ [➕ 新增至下載列表]                                │
├─────────────────────────────────────────────────┤
│ 📥 3. 下載列表                                    │
│ [# | 影片標題 | 狀態 | 進度 | 操作]                │
│ [   Download list table                         │
├─────────────────────────────────────────────────┤
│                                  [❌ Exit]      │
└─────────────────────────────────────────────────┘
```

### 3. Basic Workflow 基本流程

1. **Select Save Location** 選擇儲存位置
   - Click the "🔍 瀏覽" button to choose where to save videos
   - Default location: `~/Downloads` (home Downloads folder)

2. **Add Download Links** 新增下載連結
   - Paste video URLs in the text area (one URL per line)
   - Supports both Gimy and YouTube links
   - Click "➕ 新增至下載列表"

3. **Monitor Progress** 監控進度
   - Watch the progress bars update in real-time
   - Status indicators:
     - 🔵 Blue: Downloading
     - 🟢 Green: Completed
     - 🔴 Red: Error

4. **Manage Tasks** 管理任務
   - Click ❌ to cancel a download
   - Right-click for context menu options
   - Remove completed tasks from the list

5. **Change Language** 切換語言
   - Select from the dropdown menu in the top-left corner
   - Available languages: 繁體中文, 简体中文, English, Español

6. **Exit Application** 結束程式
   - Click "❌ Exit" button in the bottom-right
   - Confirm when prompted

## Supported URL Formats 支援的網址格式

### Gimy (https://gimy01.com/) 支援
Examples:l`
- All Gimy episode pages

### YouTube 支援
Examples:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/shorts/VIDEO_ID`
- YouTube Shorts, full videos, playlists

## Features in Detail 詳細功能說明

### Automatic Folder Creation 自動建立資料夾
- Each video is saved in a dedicated folder
- Folder name is based on video title
- Example structure:
  ```
  Downloads/
  ├── ABC/
  │   └── ABC.mp4
  ├── DEF：GHI/
  │   └── DEF：GHI.mp4
  └── Video Title/
      └── Video Title.mp4
  ```

### Progress Tracking 進度追蹤
- **藍色 Blue**: Downloading in progress
- **綠色 Green**: Download completed successfully
- **紅色 Red**: Download failed or error occurred

### Multi-language Support 多語言支援
Switch between 4 languages:
- **繁體中文**: Traditional Chinese (Default)
- **简体中文**: Simplified Chinese
- **English**: English
- **Español**: Spanish

All UI elements update instantly when language is changed.

### Context Menu Features 右鍵選單功能
- **📂 打開檔案所在資料夾**: Open the folder containing the downloaded video
- **🗑️ 從列表中移除**: Remove the task from the download list

## Troubleshooting 問題排除

### YouTube Downloads Fail YouTube 下載失敗
**Possible causes** 可能原因:
- YouTube bot detection triggered

**Solutions** 解決方法:
```bash
# Update yt-dlp to latest version
yt-dlp -U

# The app will automatically try with browser cookies
# Keep your Chrome/Safari/Firefox open and logged in
```

### Gimy Downloads Fail Gimy 下載失敗
**Possible causes** 可能原因:
- Website structure changed
- Network connection issues
- SSL certificate issues

**Solutions** 解決方法:
- Check your internet connection
- Ensure the URL is correct
- Try updating yt-dlp: `yt-dlp -U`

### Folder Opening Issues 無法開啟資料夾
**On Linux**:
```bash
sudo apt install xdg-utils
```

**On macOS/Windows**:
- Usually works out of the box
- If not, make sure you have file system permissions

### SSL Certificate Errors SSL 憑證錯誤
The application automatically handles SSL issues with the `--no-check-certificate` flag for Gimy downloads.

## Keyboard Shortcuts 快捷鍵

- **Enter** (in URL input): Add to download list
- **Ctrl+Q** or **⌘+Q**: Exit application (macOS)
- **Alt+F4**: Exit application (Windows)

## Technical Details 技術細節

### Built With 技術堆疊
- **PyQt6**: Modern GUI framework
- **yt-dlp**: Powerful video downloader
- **requests**: HTTP library for web scraping
- **Python 3.8+**: Programming language

### Architecture 架構
- **Multi-threading**: Uses QThreadPool for concurrent downloads (max 5)
- **Signal-based Communication**: PyQt signals for real-time updates
- **Modular Design**: Separate worker classes for Gimy and YouTube

### File Structure 檔案結構
```
DownloadVideo/
├── video_downloader.py   # Main application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Contributing 貢獻

This is a personal project for educational purposes. Feel free to:
- Report bugs
- Suggest features
- Fork and modify
- Share improvements

## License 授權

This project is for educational and personal use.

## Acknowledgments 致謝

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - For the amazing download functionality
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - For the beautiful GUI framework
- Gimy website - For providing the video content

---

# 中文

🎬 **影片下載器** - 支援 Gimy 與 YouTube 的跨平台影片下載工具

功能強大的跨平台影片下載器，支援 Gimy 網站和 YouTube 連結。使用 PyQt6 建立現代化的圖形介面。

## 功能特色

- 📥 **多來源下載**: 支援 Gimy 網站和 YouTube 連結
- 🌐 **多語言支援**: 4 種語言（繁體中文、简体中文、English、Español）
- 🎬 **批次下載**: 最多同時下載 5 個影片
- 📊 **即時進度**: 視覺化的進度條即時更新
- 🎯 **智慧分類**: 自動為每個影片建立專屬資料夾
- ⏸️ **任務管理**: 取消、暫停或移除下載
- 🖱️ **右鍵選單**: 右鍵點擊開啟資料夾或移除任務
- 🎨 **現代化介面**: 精美的卡片式佈局，直觀的操作

## 跨平台支援

本應用程式支援：
- **macOS** (測試於 macOS 15.1.1)
- **Windows** (Windows 10/11)
- **Linux** (Ubuntu、Fedora 等)

## 安裝方式

### 系統需求
- Python 3.8 或更高版本
- PyQt6
- yt-dlp
- requests

### 逐步安裝

#### macOS
```bash
# 安裝 Python 相依套件
pip install -r requirements.txt

# 透過 Homebrew 安裝 yt-dlp（推薦）
brew install yt-dlp

# 或透過 pip 安裝
pip install yt-dlp
```

#### Windows
```bash
# 安裝 Python 相依套件
pip install -r requirements.txt

# 安裝 yt-dlp
pip install yt-dlp
```

#### Linux (Ubuntu/Debian)
```bash
# 安裝 Python 相依套件
pip install -r requirements.txt

# 安裝 yt-dlp
sudo apt install yt-dlp

# 用於開啟檔案管理器
sudo apt install xdg-utils
```

## 使用指南

### 1. 啟動應用程式
```bash
python video_downloader.py
```

### 2. 介面說明

應用程式分為三個主要區域：

**📁 選擇儲存位置**：選擇下載影片的儲存資料夾

**🔗 新增下載連結**：
- 在此區域貼上影片網址
- 支援多行輸入，每行一個網址
- 支援 Gimy 和 YouTube 連結混合使用

**📥 下載列表**：
- 顯示所有下載任務
- 實時更新下載進度
- 可取消或管理下載任務

**❌ 結束按鈕**：位於右下角，用於關閉應用程式

### 3. 基本操作流程

1. **選擇儲存位置**
   - 點擊「🔍 瀏覽」按鈕選擇儲存位置
   - 預設位置：`~/Downloads`

2. **新增下載任務**
   - 在下載連結區域貼上網址（每行一個）
   - 支援同時貼上多個連結
   - 點擊「➕ 新增至下載列表」

3. **監控下載進度**
   - 進度條會即時更新
   - 顏色指示：
     - 🔵 藍色：正在下載
     - 🟢 綠色：下載完成
     - 🔴 紅色：下載失敗

4. **管理下載任務**
   - 點擊 ❌ 按鈕取消下載
   - 右鍵點擊開啟選單
   - 開啟資料夾或移除任務

5. **切換語言**
   - 使用左上角的下拉選單
   - 可選：繁體中文、简体中文、English、Español

### 4. 右鍵選單功能

- **📂 打開檔案所在資料夾**：立即開啟影片儲存位置
- **🗑️ 從列表中移除**：從列表中移除該任務

## 支援的網址格式

### Gimy 支援
範例：
- 所有 Gimy 影片頁面

### YouTube 支援
範例：
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/shorts/VIDEO_ID`
- 支援 Shorts、完整影片、播放清單

## 詳細功能說明

### 自動資料夾建立
- 每個影片會建立專屬資料夾
- 資料夾名稱以影片標題命名
- 範例結構：
  ```
  Downloads/
  ├── ABC/
  │   └── ABC.mp4
  ├── DEF：GHI/
  │   └── DEF：GHI.mp4
  └── Video Title/
      └── Video Title.mp4
  ```

### 進度條顏色說明
- **藍色**：正在下載中
- **綠色**：下載成功完成
- **紅色**：下載失敗或發生錯誤

### 多語言切換
- **繁體中文**：預設語言
- **简体中文**：簡體中文介面
- **English**：英文介面
- **Español**：西班牙文介面

切換語言後，所有介面文字會立即更新。

## 問題排除

### YouTube 下載失敗
**可能原因**：
- YouTube 偵測到機器人行為

**解決方法**：
```bash
# 更新 yt-dlp 到最新版本
yt-dlp -U

# 應用程式會自動嘗試使用瀏覽器 Cookies
# 請確保 Chrome/Safari/Firefox 保持開啟並已登入
```

### Gimy 下載失敗
**可能原因**：
- 網站結構變更
- 網路連線問題
- SSL 憑證問題

**解決方法**：
- 檢查網路連線
- 確認網址是否正確
- 嘗試更新 yt-dlp：`yt-dlp -U`

### 無法開啟資料夾
**Linux 系統**：
```bash
sudo apt install xdg-utils
```

**macOS/Windows 系統**：
- 通常可直接使用
- 如無法開啟，請檢查檔案系統權限

### SSL 憑證錯誤
應用程式會自動處理 Gimy 下載的 SSL 問題。

## 快捷鍵

- **Enter**（在網址輸入框）：新增到下載列表
- **Ctrl+Q** 或 **⌘+Q**：結束應用程式（macOS）
- **Alt+F4**：結束應用程式（Windows）

## 技術細節

### 使用的技術
- **PyQt6**：現代化 GUI 框架
- **yt-dlp**：強大的影片下載工具
- **requests**：HTTP 函式庫
- **Python 3.8+**：程式語言

### 架構設計
- **多執行緒**：使用 QThreadPool 實現並行下載（最多 5 個）
- **信號通訊**：使用 PyQt signals 實現即時更新
- **模組化設計**：為 Gimy 和 YouTube 建立獨立的工作類別

### 檔案結構
```
DownloadVideo/
├── video_downloader.py   # 主程式
├── requirements.txt       # Python 相依套件
└── README.md             # 本檔案
```

## 致謝

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 強大的下載功能
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - 精美的 GUI 框架
- Gimy 網站 - 提供的影片內容

---

**License** 授權：本專案僅供教育與個人用途使用。
