# NewsBoard System Architecture Design

## 1. Overview
A real-time financial news dashboard with distributed crawling, BERT-based intelligence analysis, and sub-3s end-to-end latency.

## 2. Technology Stack
- **Backend**: FastAPI (Python 3.9+)
- **Frontend**: Next.js, Tailwind CSS, Recharts, WebSocket (Socket.io)
- **Data Acquisition**: Scrapy-Redis (Distributed), Selenium/Playwright (JS-rendered pages)
- **Data Storage**: 
  - PostgreSQL (Structured news, audit logs, user data)
  - Redis (Real-time stream, SimHash deduplication cache, WebSocket session)
- **Analysis Engine**: 
  - BERT (Financial-specific model)
  - SimHash (Deduplication)
  - Neo4j (Knowledge Graph for sector impact)
- **Infrastructure**: Docker, Kubernetes, Nginx

## 3. System Components

### 3.1 Data Acquisition Layer
- **Crawler Cluster**: Multiple nodes running Scrapy, managed by Redis queue.
- **Event-Driven Monitor**: Specialized tasks for high-priority sites (Bloomberg, Reuters).
- **Deduplication**: SimHash-based similarity check in Redis before storage.

### 3.2 Intelligent Analysis Engine
- **BERT Scoring**: Multi-dimensional scoring (Credibility, Consistency, Traceability).
- **Sector Mapping**: Mapping entities to 28 SW-Level1 sectors.
- **Traceability**: Linking news back to official regulatory sources.

### 3.3 Real-time Dashboard
- **WebSocket Gateway**: Push updates to clients instantly.
- **Dynamic Heatmap**: Visualization of sector impact levels.
- **AI Summary**: Generates "Event-Conduction-Impact" logic.

### 3.4 Security & Compliance
- **Audit Logs**: Every step of processing is logged.
- **Circuit Breaker**: Auto-pauses on anomalous high-frequency negative news.
- **Insider Filter**: Pattern matching for potential insider trading keywords.

## 4. Scalability & Performance
- Supports 100k concurrent users via WebSocket horizontal scaling.
- 99.9% availability through multi-zone deployment.
- Standard API for brokerage integration.
