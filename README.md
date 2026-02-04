# 自动商品试用 (AI Product Try-On)

一个基于 AI 的智能商品试用系统，支持将任意商品（不仅仅是服装）与人物照片进行智能合成，实现虚拟试用效果。系统支持自动解析淘宝/天猫商品链接，提取商品图片，并利用先进的 AI 模型生成逼真的试用效果图。
<img width="1835" height="926" alt="f20ba39f-6711-4579-99c1-8de8ced4f266" src="https://github.com/user-attachments/assets/6a1af39b-30d8-4740-815e-f0441524415c" />
<img width="1852" height="918" alt="2481cf29-f79e-415b-95b2-0bf0c77d109c" src="https://github.com/user-attachments/assets/b157da68-1641-4f5e-aaf6-bada578728a5" />
<img width="1803" height="903" alt="258d481d-b180-4ef7-be97-c4f1f37b500e" src="https://github.com/user-attachments/assets/282999a7-054d-4d15-b2f2-8006ab691a7c" />

## ✨ 核心功能

1.  **多平台商品解析**
    *   支持解析淘宝、天猫的商品链接。
    *   支持直接粘贴带有中文描述的完整分享口令（淘口令）。
    *   自动提取商品主图及 SKU（款式/颜色）细节图。

2.  **智能图片选择**
    *   解析成功后自动展示所有提取到的商品图片。
    *   支持从多张商品图中选择最合适的一张进行试用。
    *   点击缩略图即可预览大图。

3.  **任意商品试用**
    *   不局限于服装试穿，支持各种类型的商品与人物进行合成试用。
    *   只需上传一张个人照片，即可生成试用效果。

4.  **本地化图片处理**
    *   前端自动进行 Base64 编码，减少不必要的文件上传请求，提升响应速度。
    *   支持图片上传前的本地预览。

5.  **结果预览与放大**
    *   生成结果支持全屏放大查看，细节一览无余。
    *   支持生成多张试用结果供选择。

## 🛠️ 技术栈

*   **后端**: Python, FastAPI, Uvicorn
*   **前端**: React, Vite, Tailwind CSS, Framer Motion
*   **AI 服务**: 阿里云 DashScope (通义万相)
*   **工具**: Aiohttp (异步请求), Loguru (日志管理)

## 🚀 安装与运行

### 前置要求
*   Python 3.8+
*   Node.js 16+
*   阿里云 DashScope API Key

### 1. 克隆项目
```bash
git clone <repository_url>
cd 自动商品试用
```

### 2. 后端配置与运行

1.  安装 Python 依赖：
    ```bash
    pip install -r requirements.txt
    ```

2.  配置 API Key：
    ```bash
    cp config.yaml.example config.yaml
    ```
    *   打开 `config.yaml` 或相应的配置文件（如 `backend/config.py`）。
    *   填入您的阿里云 DashScope API Key。

3.  启动后端服务：
    ```bash
    python run.py
    ```
    后端服务默认运行在 `http://localhost:8000`。

### 3. 前端构建与集成

本项目已配置为后端直接托管前端静态资源，因此通常无需单独启动前端服务。如果需要修改前端代码，请按以下步骤操作：

1.  进入前端目录：
    ```bash
    cd web
    ```

2.  安装依赖：
    ```bash
    npm install
    ```

3.  开发模式（可选）：
    ```bash
    npm run dev
    ```

4.  构建生产环境代码：
    ```bash
    npm run build
    ```
    构建完成后，生成的静态文件会自动输出到 `web/dist` 目录，重启后端服务即可生效。

## 📖 使用指南

1.  **打开应用**：
    访问 `http://localhost:8000`。

2.  **输入商品**：
    在“第一步：输入商品”的文本框中，粘贴淘宝/天猫的商品链接或完整的分享口令。
    点击“解析商品”，系统会自动提取并展示商品图片。

3.  **选择商品图**：
    在展示的图片列表中，点击选择一张您想试用的商品图片。

4.  **上传照片**：
    在“第二步：上传照片”区域，点击或拖拽上传一张您的个人照片。

5.  **生成试用**：
    点击底部的“立即生成试用效果”按钮。AI 将在几十秒内生成试用结果。

6.  **查看结果**：
    生成的图片将显示在下方结果区域。点击图片可以全屏放大查看。

## ⚠️ 注意事项

*   请确保您的 API Key 有足够的额度。
*   上传的照片建议清晰、光线充足，以获得最佳的试用效果。
*   商品图片最好背景干净，主体突出。

## 📄 许可证

MIT License
