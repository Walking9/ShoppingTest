# iMaotai

基于 Python + ADB + 离线 OCR 的安卓自动化抢购引擎。

## 环境搭建

### 1. 创建虚拟环境
建议使用 Python 3.9+。

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. ADB 配置
确保宿主机已安装 `adb` 命令行工具，且 `adb server` 已启动：
```bash
adb start-server
```

## 目录结构
- `src/adb`: 设备控制模块
- `src/ocr`: 视觉识别模块
- `src/engine`: 任务调度引擎
- `config`: 配置文件
- `data`: 模型与模板数据
