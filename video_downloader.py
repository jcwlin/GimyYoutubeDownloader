import sys
import re
import requests
import subprocess
import json
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QFileDialog, QHBoxLayout, QHeaderView)
from PyQt6.QtCore import QThread, pyqtSignal, QRunnable, QThreadPool, QObject

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    Supported signals are:
    progress: int, str -> task_id, progress_string
    finished: int, str -> task_id, message
    error: int, str -> task_id, error_message
    '''
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(int, str)
    error = pyqtSignal(int, str)

class DownloadWorker(QRunnable):
    '''
    Worker thread for downloading a single video.
    Inherits from QRunnable to run on a thread in a QThreadPool.
    '''
    def __init__(self, task_id, url, save_path):
        super().__init__()
        self.task_id = task_id
        self.url = url
        self.save_path = save_path
        self.signals = WorkerSignals()

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

            if not video_url:
                self.signals.error.emit(self.task_id, "錯誤：在播放器資料中未找到 'url' 欄位。")
                return
            
            # Create a dedicated folder for the video
            sanitized_folder_name = self.sanitize_filename(vod_name)
            final_save_path = os.path.join(self.save_path, sanitized_folder_name)
            
            self.signals.progress.emit(self.task_id, f"儲存至: {sanitized_folder_name}")

            # Use -P for path and --no-check-certificate for SSL errors
            process = subprocess.Popen(
                ['yt-dlp', '--no-check-certificate', '-P', final_save_path, video_url],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8'
            )

            for line in iter(process.stdout.readline, ''):
                self.signals.progress.emit(self.task_id, line.strip())
            
            process.stdout.close()
            return_code = process.wait()

            if return_code == 0:
                self.signals.finished.emit(self.task_id, f"下載完成！")
            else:
                self.signals.error.emit(self.task_id, f"下載失敗，返回錯誤碼：{return_code}")

        except requests.RequestException as e:
            self.signals.error.emit(self.task_id, f"網路錯誤：{e}")
        except Exception as e:
            self.signals.error.emit(self.task_id, f"發生未知錯誤：{e}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gimy 影片下載器")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self._create_save_path_widgets()
        self._create_url_input_widgets()
        self._create_download_table()

        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(5)
        
        self.task_id_counter = 0
        self.task_row_map = {}

    def _create_save_path_widgets(self):
        path_layout = QHBoxLayout()
        self.save_path_input = QLineEdit()
        self.save_path_input.setPlaceholderText("請選擇影片儲存位置...")
        self.save_path_input.setText(os.path.join(os.path.expanduser("~"), "Downloads"))
        path_layout.addWidget(self.save_path_input)

        browse_button = QPushButton("瀏覽...")
        browse_button.clicked.connect(self.browse_save_location)
        path_layout.addWidget(browse_button)
        self.layout.addLayout(path_layout)

    def _create_url_input_widgets(self):
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("請在此貼上 Gimy 影片頁面的網址...")
        url_layout.addWidget(self.url_input)

        self.add_download_button = QPushButton("新增下載")
        self.add_download_button.clicked.connect(self.add_download)
        url_layout.addWidget(self.add_download_button)
        self.layout.addLayout(url_layout)

    def _create_download_table(self):
        self.download_table = QTableWidget()
        self.download_table.setColumnCount(3)
        self.download_table.setHorizontalHeaderLabels(["URL", "狀態", "進度"])
        header = self.download_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.layout.addWidget(self.download_table)

    def browse_save_location(self):
        directory = QFileDialog.getExistingDirectory(self, "選擇儲存資料夾")
        if directory:
            self.save_path_input.setText(directory)

    def add_download(self):
        url = self.url_input.text()
        save_path = self.save_path_input.text()

        if not url or not save_path:
            # Maybe show a message box here in a future version
            return

        row_position = self.download_table.rowCount()
        self.download_table.insertRow(row_position)
        
        self.download_table.setItem(row_position, 0, QTableWidgetItem(url))
        self.download_table.setItem(row_position, 1, QTableWidgetItem("等待中..."))
        self.download_table.setItem(row_position, 2, QTableWidgetItem("0%"))
        
        task_id = self.task_id_counter
        self.task_row_map[task_id] = row_position
        self.task_id_counter += 1

        worker = DownloadWorker(task_id=task_id, url=url, save_path=save_path)
        worker.signals.progress.connect(self.update_progress)
        worker.signals.finished.connect(self.on_finished)
        worker.signals.error.connect(self.on_error)
        
        self.threadpool.start(worker)
        self.url_input.clear()

    def update_progress(self, task_id, message):
        row = self.task_row_map.get(task_id)
        if row is None:
            return
        
        status_item = self.download_table.item(row, 1)
        progress_item = self.download_table.item(row, 2)
        
        # Try to parse percentage from yt-dlp output
        if message.startswith("儲存至:"):
             # Keep the "Downloading..." status but update the progress column with the path
            progress_item.setText(message)
        elif progress_match := re.search(r'\[download\]\s+([\d\.]+)%', message):
            percent = progress_match.group(1)
            status_item.setText("下載中...")
            progress_item.setText(f"{percent}%")
        else:
            status_item.setText(message)


    def on_finished(self, task_id, message):
        row = self.task_row_map.get(task_id)
        if row is not None:
            self.download_table.item(row, 1).setText(message)
            # No need to update progress text again if it was showing the path
            if "%" not in self.download_table.item(row, 2).text():
                 self.download_table.item(row, 2).setText("100%")


    def on_error(self, task_id, message):
        row = self.task_row_map.get(task_id)
        if row is not None:
            self.download_table.item(row, 1).setText("錯誤")
            # You can use the progress column to show the error message
            self.download_table.item(row, 2).setText(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
