FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製當前目錄所有檔案到容器內
COPY . /app

# 安裝必要套件（如果有 requirements.txt）
RUN pip install --no-cache-dir -r .devcontainer/requirements.txt

# 預設執行指令（依你的需求修改）
CMD ["python", "main.py"]