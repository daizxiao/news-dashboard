# Financial NewsBoard System

## 1. System Overview
A real-time financial news processing system with sub-3s end-to-end latency.

## 2. Key Features
- **Distributed Crawling**: Scrapy-Redis cluster for 20+ platforms.
- **SimHash Deduplication**: <5% duplication rate.
- **BERT Intelligence**: Financial-specific scoring (0-100).
- **Sector Mapping**: 28 SW-Level1 sector impact analysis.
- **Real-time Dashboard**: WebSocket push with dynamic heatmaps.
- **Security & Compliance**: Audit logs, Circuit breaker, Manual audit triggers.

## 3. Quick Start

### Backend (FastAPI)
1. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Start the API server:
   ```bash
   python backend/app/main.py
   ```

### Frontend (Next.js)
1. Install dependencies:
   ```bash
   npm install
   ```
2. Start development server:
   ```bash
   npm run dev
   ```

### Running Tests
Run the 100-event backtest simulation:
```bash
python backend/scripts/test_report.py
```

## 4. API Documentation
- `GET /`: Health check.
- `WS /ws`: Real-time news stream.
- `GET /history`: (To be implemented) Retrieve historical news.

## 6. 部署指南 (Deployment)

本项目支持在多个免费静态托管平台一键部署。

### 在线演示 (Live Demo)
- **GitHub Pages**: `https://<your-username>.github.io/04_Project_news`
- **Vercel**: `https://04-project-news.vercel.app`
- **Netlify**: `https://04-project-news.netlify.app`

### 一键部署 (One-Click Deploy)

| 平台 | 部署按钮 |
| :--- | :--- |
| **Vercel** | [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2F<your-username>%2F04_Project_news) |
| **Netlify** | [![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/<your-username>/04_Project_news) |

### 手动部署步骤

#### 1. GitHub Pages
- 将代码推送至 GitHub `main` 分支。
- GitHub Actions 会自动触发 `.github/workflows/deploy.yml` 任务。
- 等待构建完成后，在仓库 `Settings > Pages` 中将源设置为 `gh-pages` 分支即可访问。

#### 2. Vercel
- 在 Vercel 控制台导入 GitHub 仓库。
- 框架预设选择 `Other`。
- 构建命令留空，输出目录设置为 `.`。
- 系统会自动识别 `vercel.json` 并处理 SPA 路由重写。

#### 3. Netlify
- 在 Netlify 控制台选择 `Import from git`。
- 发布目录设置为 `.`。
- 系统会自动识别 `netlify.toml` 并处理 SPA 重定向规则。
