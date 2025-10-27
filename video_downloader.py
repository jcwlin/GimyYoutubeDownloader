import sys
import re
import requests
import subprocess
import json
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QFileDialog, QHBoxLayout, QHeaderView, QGroupBox,
                             QTextEdit, QProgressBar, QMenu, QMessageBox, QComboBox, QLabel)
from PyQt6.QtCore import QThread, pyqtSignal, QRunnable, QThreadPool, QObject, Qt, pyqtSlot
from PyQt6.QtGui import QAction

# Translation dictionary
TRANSLATIONS = {
    'en': {
        'app_title': '🎬 Video Downloader (Supports Gimy & YouTube)',
        'save_location': '📁 1. Choose Save Location',
        'add_download': '🔗 2. Add Download Link (Supports Gimy & YouTube)',
        'download_list': '📥 3. Download List',
        'placeholder_save': 'Please select save location...',
        'placeholder_url': 'Support multiple links, one per line...\nSupports Gimy websites and YouTube links',
        'button_browse': '🔍 Browse...',
        'button_add': '➕ Add to Download List',
        'button_cancel_task': '❌ Cancel',
        'button_exit': '❌ Exit Application',
        'col_id': '#',
        'col_title': 'Video Title',
        'col_status': 'Status',
        'col_progress': 'Progress',
        'col_action': 'Action',
        'context_open_folder': '📂 Open File Location',
        'context_remove': '🗑️ Remove from List',
        'status_parsing': 'Parsing...',
        'status_waiting': 'Waiting...',
        'status_downloading': 'Downloading...',
        'status_done': 'Download Complete!',
        'status_cancelled': 'Cancelled',
        'status_error': 'Error',
        'message_warning': 'Warning',
        'message_info': 'Information',
        'message_unsupported': 'Unsupported Link',
        'message_cannot_detect': 'Unable to detect link type',
        'dialog_folder_not_exists': 'Folder does not exist or download has not started.',
        'dialog_choose_folder': 'Choose Save Folder'
    },
    'zh-TW': {
        'app_title': '🎬 影片下載器 (支援 Gimy & YouTube)',
        'save_location': '📁 1. 選擇儲存位置',
        'add_download': '🔗 2. 新增下載連結 (支援 Gimy & YouTube)',
        'download_list': '📥 3. 下載列表',
        'placeholder_save': '請選擇影片儲存位置...',
        'placeholder_url': '支援多個連結，一行一個...\n支援 Gimy 網站和 YouTube 連結',
        'button_browse': '🔍 瀏覽...',
        'button_add': '➕ 新增至下載列表',
        'button_cancel_task': '❌ 取消',
        'button_exit': '❌ 結束應用程式',
        'col_id': '#',
        'col_title': '影片標題',
        'col_status': '狀態',
        'col_progress': '進度',
        'col_action': '操作',
        'context_open_folder': '📂 打開檔案所在資料夾',
        'context_remove': '🗑️ 從列表中移除',
        'status_parsing': '解析中...',
        'status_waiting': '等待中...',
        'status_downloading': '下載中...',
        'status_done': '下載完成！',
        'status_cancelled': '已取消',
        'status_error': '錯誤',
        'message_warning': '提醒',
        'message_info': '提示',
        'message_unsupported': '不支援的連結',
        'message_cannot_detect': '無法識別的連結類型',
        'dialog_folder_not_exists': '資料夾尚不存在或下載未開始。',
        'dialog_choose_folder': '選擇儲存資料夾'
    },
    'zh-CN': {
        'app_title': '🎬 视频下载器 (支持 Gimy & YouTube)',
        'save_location': '📁 1. 选择保存位置',
        'add_download': '🔗 2. 添加下载链接 (支持 Gimy & YouTube)',
        'download_list': '📥 3. 下载列表',
        'placeholder_save': '请选择视频保存位置...',
        'placeholder_url': '支持多个链接，每行一个...\n支持 Gimy 网站和 YouTube 链接',
        'button_browse': '🔍 浏览...',
        'button_add': '➕ 添加到下载列表',
        'button_cancel_task': '❌ 取消',
        'button_exit': '❌ 退出应用程序',
        'col_id': '#',
        'col_title': '视频标题',
        'col_status': '状态',
        'col_progress': '进度',
        'col_action': '操作',
        'context_open_folder': '📂 打开文件位置',
        'context_remove': '🗑️ 从列表中移除',
        'status_parsing': '解析中...',
        'status_waiting': '等待中...',
        'status_downloading': '下载中...',
        'status_done': '下载完成！',
        'status_cancelled': '已取消',
        'status_error': '错误',
        'message_warning': '提醒',
        'message_info': '提示',
        'message_unsupported': '不支持的链接',
        'message_cannot_detect': '无法识别的链接类型',
        'dialog_folder_not_exists': '文件夹尚不存在或下载未开始。',
        'dialog_choose_folder': '选择保存文件夹'
    },
    'es': {
        'app_title': '🎬 Descargador de Videos (Soporta Gimy & YouTube)',
        'save_location': '📁 1. Elegir Ubicación de Guardado',
        'add_download': '🔗 2. Agregar Enlace de Descarga (Soporta Gimy & YouTube)',
        'download_list': '📥 3. Lista de Descargas',
        'placeholder_save': 'Por favor seleccione la ubicación de guardado...',
        'placeholder_url': 'Soporta múltiples enlaces, uno por línea...\nSoporta sitios web Gimy y enlaces de YouTube',
        'button_browse': '🔍 Examinar...',
        'button_add': '➕ Agregar a la Lista de Descarga',
        'button_cancel_task': '❌ Cancelar',
        'button_exit': '❌ Salir de la Aplicación',
        'col_id': '#',
        'col_title': 'Título del Video',
        'col_status': 'Estado',
        'col_progress': 'Progreso',
        'col_action': 'Acción',
        'context_open_folder': '📂 Abrir Ubicación del Archivo',
        'context_remove': '🗑️ Eliminar de la Lista',
        'status_parsing': 'Analizando...',
        'status_waiting': 'Esperando...',
        'status_downloading': 'Descargando...',
        'status_done': '¡Descarga Completada!',
        'status_cancelled': 'Cancelado',
        'status_error': 'Error',
        'message_warning': 'Advertencia',
        'message_info': 'Información',
        'message_unsupported': 'Enlace No Soportado',
        'message_cannot_detect': 'No se pudo detectar el tipo de enlace',
        'dialog_folder_not_exists': 'La carpeta aún no existe o la descarga no ha comenzado.',
        'dialog_choose_folder': 'Elegir Carpeta de Guardado'
    }
}


def get_translation(key, lang='en'):
    """Get translation for a given key and language."""
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    Supported signals are:
    progress: int, str -> task_id, progress_string
    finished: int, str -> task_id, message
    error: int, str -> task_id, error_message
    title_found: int, str -> task_id, video_title
    '''
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(int, str)
    error = pyqtSignal(int, str)
    title_found = pyqtSignal(int, str)

class GimyDownloadWorker(QRunnable):
    '''
    Worker thread for downloading videos from Gimy.
    Inherits from QRunnable to run on a thread in a QThreadPool.
    '''
    def __init__(self, task_id, url, save_path):
        super().__init__()
        self.task_id = task_id
        self.url = url
        self.save_path = save_path
        self.signals = WorkerSignals()
        self.is_cancelled = False
        self.process = None
        
    def cancel(self):
        self.is_cancelled = True
        if self.process:
            self.process.terminate()

    def sanitize_filename(self, name):
        """Remove characters that are invalid in folder/file names on most OSes."""
        return re.sub(r'[\\/*?:"<>|]', "", name).strip()

    def run(self):
        try:
            self.signals.progress.emit(self.task_id, "正在獲取網頁內容...")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                'Referer': 'https://gimy01.com/',
            }
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
            html_content = response.text
            self.signals.progress.emit(self.task_id, "正在解析影片網址...")

            player_data_match = re.search(r'var player_data\s*=\s*(.*?)</script>', html_content, re.DOTALL)
            if not player_data_match:
                self.signals.error.emit(self.task_id, "錯誤：在網頁中找不到播放器資料 (player_data)。")
                self.signals.progress.emit(self.task_id, f"--- 偵錯: 獲取到的 HTML (前 1500 字元) ---\n{html_content[:1500]}")
                return

            player_data_str = player_data_match.group(1).strip()
            try:
                player_data = json.loads(player_data_str)
            except json.JSONDecodeError as e:
                self.signals.error.emit(self.task_id, f"錯誤：解析播放器資料失敗: {e}")
                return

            video_url = player_data.get("url")
            vod_name = player_data.get("vod_data", {}).get("vod_name", f"video_{self.task_id}")
            self.signals.title_found.emit(self.task_id, vod_name)

            if not video_url:
                self.signals.error.emit(self.task_id, "錯誤：在播放器資料中未找到 'url' 欄位。")
                return
            
            # Create a dedicated folder for the video
            sanitized_folder_name = self.sanitize_filename(vod_name)
            final_save_path = os.path.join(self.save_path, sanitized_folder_name)
            
            self.signals.progress.emit(self.task_id, f"儲存至: {sanitized_folder_name}")

            # Use -P for path and --no-check-certificate for SSL errors
            self.process = subprocess.Popen(
                ['yt-dlp', '--no-check-certificate', '-P', final_save_path, video_url],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8'
            )

            for line in iter(self.process.stdout.readline, ''):
                if self.is_cancelled:
                    break
                self.signals.progress.emit(self.task_id, line.strip())
            
            self.process.stdout.close()
            return_code = self.process.wait()

            if self.is_cancelled:
                self.signals.error.emit(self.task_id, "已取消")
            elif return_code == 0:
                self.signals.finished.emit(self.task_id, f"下載完成！")
            else:
                self.signals.error.emit(self.task_id, f"下載失敗，返回錯誤碼：{return_code}")

        except requests.RequestException as e:
            self.signals.error.emit(self.task_id, f"網路錯誤：{e}")
        except Exception as e:
            self.signals.error.emit(self.task_id, f"發生未知錯誤：{e}")


class YouTubeDownloadWorker(QRunnable):
    '''
    Worker thread for downloading videos from YouTube.
    Uses yt-dlp directly since it has native YouTube support.
    '''
    def __init__(self, task_id, url, save_path):
        super().__init__()
        self.task_id = task_id
        self.url = url
        self.save_path = save_path
        self.signals = WorkerSignals()
        self.is_cancelled = False
        self.process = None
        
    def cancel(self):
        self.is_cancelled = True
        if self.process:
            self.process.terminate()
            
    def _detect_default_browser(self):
        """Detect the default browser for cookie extraction based on OS."""
        import platform
        system = platform.system()
        
        if system == 'Windows':
            # Try Chrome, Edge, Firefox in order
            return 'chrome'
        elif system == 'Darwin':  # macOS
            return 'chrome'
        else:  # Linux
            # Try Chrome, Firefox
            return 'chrome'

    def run(self):
        try:
            self.signals.progress.emit(self.task_id, "正在下載 YouTube 影片...")

            # Use multiple fallback options to bypass YouTube's bot detection
            commands = []
            
            # First, try with cookies from browser (detect based on OS)
            browser = self._detect_default_browser()
            if browser:
                commands.append([
                    'yt-dlp',
                    '--cookies-from-browser', browser,
                    '--format', 'best',
                    '-o', f'{self.save_path}/%(title)s.%(ext)s',
                    '--newline',
                    '--progress',
                    self.url
                ])
            
            # Fallback: try with extended options without cookies
            commands.append([
                'yt-dlp',
                '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                '--format', 'best',
                '-o', f'{self.save_path}/%(title)s.%(ext)s',
                '--newline',
                '--progress',
                self.url
            ])
            
        # Try each command until one succeeds
            for cmd in commands:
                if self.is_cancelled:
                    break
                    
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    encoding='utf-8'
                )
                
                output_lines = []
                for line in iter(self.process.stdout.readline, ''):
                    if self.is_cancelled:
                        break
                    
                    output_lines.append(line.strip())
                    self.signals.progress.emit(self.task_id, line.strip())
                
                self.process.stdout.close()
                return_code = self.process.wait()
                
                # If this command succeeded, we're done
                if return_code == 0:
                    self.signals.finished.emit(self.task_id, "下載完成！")
                    return
                
                # If we got a bot detection error, try next command
                if any('Sign in to confirm' in line or 'not a bot' in line for line in output_lines):
                    self.signals.progress.emit(self.task_id, f"YouTube 偵測到機器人，嘗試另一種方法...")
                    continue
                else:
                    # Some other error, break out and report it
                    error_msg = f"下載失敗，返回錯誤碼：{return_code}"
                    error_lines = [line for line in output_lines if 'error' in line.lower() or 'ERROR' in line]
                    if error_lines:
                        error_msg += f"\n{error_lines[-1]}"
                    if self.is_cancelled:
                        self.signals.error.emit(self.task_id, "已取消")
                    else:
                        self.signals.error.emit(self.task_id, error_msg)
                    return

        except Exception as e:
            self.signals.error.emit(self.task_id, f"發生未知錯誤：{e}")


def detect_url_type(url):
    """Detect if the URL is from YouTube or Gimy."""
    youtube_patterns = [
        r'(youtube\.com|youtu\.be)',
        r'youtube\.com/watch',
        r'youtu\.be/',
    ]
    
    for pattern in youtube_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return 'youtube'
    
    if 'gimy01.com' in url:
        return 'gimy'
    
    return 'unknown'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang = 'zh-TW'  # Default language
        self.setGeometry(100, 100, 900, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(15)
        
        # Create toolbar for language selection and exit button
        self._create_toolbar()

        self._create_save_path_widgets()
        self._create_url_input_widgets()
        self._create_download_table()
        
        # Add exit button at the bottom right
        self._add_exit_button()

        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(5)
        
        self.task_id_counter = 0
        self.task_row_map = {}
        self.workers = {}
        
        # Update UI with current language
        self.update_language()
        
    def _create_toolbar(self):
        """Create language selector in top-left and exit button in layout."""
        # Language selector in top-left
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(['繁體中文', '简体中文', 'English', 'Español'])
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        
        # Add language selector to main layout at the top
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel('🌐 Language:'))
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()  # Push to left
        
        # Create a temporary widget to hold the language selector
        lang_widget = QWidget()
        lang_widget.setLayout(lang_layout)
        self.main_layout.addWidget(lang_widget)
        
        # Exit button will be added to the bottom layout
        self.exit_button = QPushButton('❌ Exit')
        self.exit_button.clicked.connect(self.close_application)
        
    def _add_exit_button(self):
        """Add exit button at the bottom right of the window."""
        exit_layout = QHBoxLayout()
        exit_layout.addStretch()  # Push button to the right
        exit_layout.addWidget(self.exit_button)
        self.main_layout.addLayout(exit_layout)
            
    def close_application(self):
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            QApplication.quit()
            
    def on_language_changed(self, index):
        """Handle language combo box change."""
        lang_map = {0: 'zh-TW', 1: 'zh-CN', 2: 'en', 3: 'es'}
        lang_code = lang_map.get(index, 'en')
        self.set_language(lang_code)
            
    def set_language(self, lang_code):
        self.lang = lang_code
        self.update_language()
        
        # Update combo box index to match current language (suppress signal during update)
        if hasattr(self, 'lang_combo'):
            self.lang_combo.blockSignals(True)
            lang_map = {'zh-TW': 0, 'zh-CN': 1, 'en': 2, 'es': 3}
            index = lang_map.get(lang_code, 0)
            self.lang_combo.setCurrentIndex(index)
            self.lang_combo.blockSignals(False)
        
    def update_language(self):
        t = lambda k: get_translation(k, self.lang)
        
        # Update window title
        self.setWindowTitle(t('app_title'))
        
        # Update group boxes
        self.save_location_group.setTitle(t('save_location'))
        self.url_input_group.setTitle(t('add_download'))
        self.download_table_group.setTitle(t('download_list'))
        
        # Update placeholders and buttons
        self.save_path_input.setPlaceholderText(t('placeholder_save'))
        self.url_input.setPlaceholderText(t('placeholder_url'))
        self.browse_button.setText(t('button_browse'))
        self.add_download_button.setText(t('button_add'))
        
        # Update table headers
        headers = [t('col_id'), t('col_title'), t('col_status'), t('col_progress'), t('col_action')]
        self.download_table.setHorizontalHeaderLabels(headers)

    def _create_save_path_widgets(self):
        self.save_location_group = QGroupBox()
        path_layout = QHBoxLayout()
        self.save_path_input = QLineEdit()
        self.save_path_input.setText(os.path.join(os.path.expanduser("~"), "Downloads"))
        path_layout.addWidget(self.save_path_input)

        self.browse_button = QPushButton()
        self.browse_button.clicked.connect(self.browse_save_location)
        path_layout.addWidget(self.browse_button)
        self.save_location_group.setLayout(path_layout)
        self.main_layout.addWidget(self.save_location_group)

    def _create_url_input_widgets(self):
        self.url_input_group = QGroupBox()
        main_layout = QVBoxLayout()
        
        self.url_input = QTextEdit()
        self.url_input.setFixedHeight(100)
        main_layout.addWidget(self.url_input)

        self.add_download_button = QPushButton()
        self.add_download_button.clicked.connect(self.add_downloads)
        main_layout.addWidget(self.add_download_button)
        
        self.url_input_group.setLayout(main_layout)
        self.main_layout.addWidget(self.url_input_group)

    def _create_download_table(self):
        self.download_table_group = QGroupBox()
        table_layout = QVBoxLayout()
        
        self.download_table = QTableWidget()
        self.download_table.setColumnCount(5)
        header = self.download_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        self.download_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.download_table.customContextMenuRequested.connect(self.show_context_menu)
        
        table_layout.addWidget(self.download_table)
        self.download_table_group.setLayout(table_layout)
        self.main_layout.addWidget(self.download_table_group)

    def t(self, key):
        """Shortcut to get translation."""
        return get_translation(key, self.lang)

    def browse_save_location(self):
        directory = QFileDialog.getExistingDirectory(self, self.t('dialog_choose_folder'))
        if directory:
            self.save_path_input.setText(directory)

    def add_downloads(self):
        urls = self.url_input.toPlainText().strip().split('\n')
        save_path = self.save_path_input.text()

        if not urls or not save_path or not urls[0]:
            QMessageBox.warning(self, self.t('message_warning'), 
                              f"Please enter at least one valid URL and save path.")
            return
            
        for url in urls:
            if url.strip():
                self._add_single_download(url.strip(), save_path)
        
        self.url_input.clear()

    def _add_single_download(self, url, save_path):
        row_position = self.download_table.rowCount()
        self.download_table.insertRow(row_position)
        
        task_id = self.task_id_counter
        self.download_table.setItem(row_position, 0, QTableWidgetItem(str(task_id)))
        self.download_table.setItem(row_position, 1, QTableWidgetItem(self.t('status_parsing')))
        self.download_table.setItem(row_position, 2, QTableWidgetItem(self.t('status_waiting')))

        progress_bar = QProgressBar()
        progress_bar.setValue(0)
        progress_bar.setTextVisible(True)
        self.download_table.setCellWidget(row_position, 3, progress_bar)
        
        cancel_button = QPushButton(self.t('button_cancel_task'))
        cancel_button.clicked.connect(lambda _, t_id=task_id: self.cancel_task(t_id))
        self.download_table.setCellWidget(row_position, 4, cancel_button)

        # Detect URL type and use appropriate worker
        url_type = detect_url_type(url)
        
        if url_type == 'youtube':
            worker = YouTubeDownloadWorker(task_id=task_id, url=url, save_path=save_path)
            # YouTube worker doesn't have title_found signal, so we'll skip that connection
        elif url_type == 'gimy':
            worker = GimyDownloadWorker(task_id=task_id, url=url, save_path=save_path)
            worker.signals.title_found.connect(self.update_title)
        else:
            QMessageBox.warning(self, self.t('message_unsupported'), 
                              f"{self.t('message_cannot_detect')}: {url}")
            self.download_table.removeRow(row_position)
            return

        worker.signals.progress.connect(self.update_progress)
        worker.signals.finished.connect(self.on_finished)
        worker.signals.error.connect(self.on_error)
        
        self.workers[task_id] = worker
        self.threadpool.start(worker)
        self.task_id_counter += 1
        
    def update_title(self, task_id, title):
        row = self._find_row_by_task_id(task_id)
        if row is not None:
            self.download_table.item(row, 1).setText(title)

    def update_progress(self, task_id, message):
        row = self._find_row_by_task_id(task_id)
        if row is None: return
        
        status_item = self.download_table.item(row, 2)
        progress_bar = self.download_table.cellWidget(row, 3)
        
        progress_match = re.search(r'\[download\]\s+([\d\.]+)%', message)
        if progress_match:
            percent = float(progress_match.group(1))
            progress_bar.setValue(int(percent))
            status_item.setText(self.t('status_downloading'))
        else:
            status_item.setText(message)


    def on_finished(self, task_id, message):
        row = self._find_row_by_task_id(task_id)
        if row is not None:
            self.download_table.item(row, 2).setText(message)
            progress_bar = self.download_table.cellWidget(row, 3)
            progress_bar.setValue(100)
            progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #78B754; }")
            self.download_table.cellWidget(row, 4).setEnabled(False)

    def on_error(self, task_id, message):
        row = self._find_row_by_task_id(task_id)
        if row is not None:
            self.download_table.item(row, 2).setText(message)
            progress_bar = self.download_table.cellWidget(row, 3)
            progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #DA4453; }")
            self.download_table.cellWidget(row, 4).setEnabled(False)
            
    def cancel_task(self, task_id):
        if task_id in self.workers:
            self.workers[task_id].cancel()
            
    def _find_row_by_task_id(self, task_id):
        for row in range(self.download_table.rowCount()):
            if self.download_table.item(row, 0).text() == str(task_id):
                return row
        return None

    def show_context_menu(self, pos):
        row = self.download_table.rowAt(pos.y())
        if row < 0: return
        
        task_id = int(self.download_table.item(row, 0).text())
        menu = QMenu()
        
        open_folder_action = QAction(self.t('context_open_folder'), self)
        open_folder_action.triggered.connect(lambda: self.open_folder(task_id))
        menu.addAction(open_folder_action)
        
        remove_action = QAction(self.t('context_remove'), self)
        remove_action.triggered.connect(lambda: self.remove_task(row))
        menu.addAction(remove_action)
        
        menu.exec(self.download_table.mapToGlobal(pos))
        
    def open_folder(self, task_id):
        row = self._find_row_by_task_id(task_id)
        if row is None: return
        
        title = self.download_table.item(row, 1).text()
        base_path = self.save_path_input.text()
        folder_path = os.path.join(base_path, re.sub(r'[\\/*?:"<>|]', "", title).strip())

        if os.path.isdir(folder_path):
            try:
                if sys.platform == "win32":
                    os.startfile(folder_path)
                elif sys.platform == "darwin": # macOS
                    subprocess.Popen(["open", folder_path])
                else: # linux and other Unix-like systems
                    subprocess.Popen(["xdg-open", folder_path])
            except Exception as e:
                QMessageBox.warning(self, self.t('message_warning'), 
                                  f"Failed to open folder: {str(e)}")
        else:
            QMessageBox.information(self, self.t('message_info'), 
                                  self.t('dialog_folder_not_exists'))

    def remove_task(self, row):
        self.download_table.removeRow(row)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
