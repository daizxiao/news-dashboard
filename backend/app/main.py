from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import uuid
from datetime import datetime
from typing import List

# Import local modules
from analysis.bert_analyzer import FinancialBERTAnalyzer
from crawlers.deduplication import NewsDeduplicator

app = FastAPI(title="Financial NewsBoard API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared resources
deduplicator = NewsDeduplicator()
analyzer = FinancialBERTAnalyzer()

# Active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def root():
    return {"status": "ok", "message": "NewsBoard API is running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Just keep connection open, we will push data from background tasks
            data = await websocket.receive_text()
            # Handle client-side pings if necessary
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def news_stream_simulator():
    """
    Simulate incoming news from crawlers and broadcast to clients.
    In production, this would be a consumer from Redis/Kafka.
    """
    mock_news = [
        {"title": "Fed indicates potential interest rate hike in Q3.", "platform": "Bloomberg"},
        {"title": "China manufacturing data beats expectations, tech stocks surge.", "platform": "Caixin"},
        {"title": "Oil prices stabilize as OPEC+ maintains current production levels.", "platform": "Reuters"},
        {"title": "New trade agreement signed between EU and Mercosur.", "platform": "Bloomberg"},
        {"title": "Banking sector shows resilience in stress tests.", "platform": "Reuters"}
    ]
    
    import random
    
    while True:
        # Pick random news to simulate
        news_item = random.choice(mock_news).copy()
        news_item['timestamp'] = datetime.now().isoformat()
        news_item['id'] = str(uuid.uuid4())
        
        # 1. Deduplication
        if not deduplicator.is_duplicate(news_item['title']):
            # 2. Analysis
            news_item['credibility_score'] = analyzer.get_credibility_score(news_item)
            news_item['sector_impacts'] = analyzer.analyze_sector_impact(news_item['title'])
            news_item['ai_summary'] = analyzer.generate_investment_logic(news_item)
            
            # 3. Security Check (Circuit Breaker example)
            # if is_extreme_negative(news_item): ...
            
            # 4. Broadcast
            await manager.broadcast(json.dumps(news_item))
            print(f"Broadcasted news: {news_item['title']}")
            
        await asyncio.sleep(3) # Simulate a 3-second news cycle

@app.on_event("startup")
async def startup_event():
    # Start the background news simulation
    asyncio.create_task(news_stream_simulator())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
