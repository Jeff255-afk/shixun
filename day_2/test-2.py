import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QGroupBox, QFormLayout, QComboBox
from PyQt5.QtCore import QThread, pyqtSignal
import socket
from concurrent.futures import ThreadPoolExecutor

class PortScanner(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, host, ports, protocol):
        super().__init__()
        self.host = host
        self.ports = ports
        self.protocol = protocol

    def run(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self.scan_port, port): port for port in range(self.ports[0], self.ports[1] + 1)}
            for future in futures:
                try:
                    result = future.result()
                    if result:
                        self.update_signal.emit(result)
                except Exception as e:
                    self.update_signal.emit(f"扫描端口时发生错误: {e}")

    def scan_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((self.host, port))
        sock.close()
        if result == 0:
            return f"{self.protocol.upper()} 端口 {port} 是开放的"
        else:
            return f"{self.protocol.upper()} 端口 {port} 是关闭的"

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = '端口扫描器'
        self.initUI()
        self.scanner_thread = None

    def initUI(self):
        self.setWindowTitle(self.title)
        main_layout = QVBoxLayout()

        # 主机和端口输入组
        input_group = QGroupBox("请输入目标主机和端口范围")
        input_layout = QFormLayout()

        self.host_input = QLineEdit()
        input_layout.addRow(QLabel("主机或URL:"), self.host_input)

        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems(["http", "https"])
        input_layout.addRow(QLabel("协议:"), self.protocol_combo)

        self.start_port_input = QLineEdit()
        input_layout.addRow(QLabel("起始端口:"), self.start_port_input)

        self.end_port_input = QLineEdit()
        input_layout.addRow(QLabel("结束端口:"), self.end_port_input)

        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # 扫描按钮
        self.scan_button = QPushButton('开始扫描')
        self.scan_button.clicked.connect(self.on_scan_click)
        main_layout.addWidget(self.scan_button)

        # 输出文本区域
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        main_layout.addWidget(self.output_text)

        self.setLayout(main_layout)

    def on_scan_click(self):
        host_or_url = self.host_input.text().strip()
        protocol = self.protocol_combo.currentText()
        try:
            start_port = int(self.start_port_input.text())
            end_port = int(self.end_port_input.text())
        except ValueError:
            self.output_text.append("请输入有效的端口号。")
            return

        if self.scanner_thread and self.scanner_thread.isRunning():
            self.output_text.append("正在扫描中，请稍后...")
            return

        try:
            host = socket.gethostbyname(host_or_url)
        except socket.gaierror:
            self.output_text.append("无法解析主机名或URL。")
            return

        self.scanner_thread = PortScanner(host, (start_port, end_port), protocol)
        self.scanner_thread.update_signal.connect(self.update_output)
        self.scanner_thread.finished.connect(lambda: self.scan_button.setEnabled(True))
        self.scan_button.setEnabled(False)
        self.scanner_thread.start()

    def update_output(self, message):
        self.output_text.append(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())



