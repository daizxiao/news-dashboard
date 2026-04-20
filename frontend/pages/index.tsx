import React, { useState, useEffect } from 'react';
import Head from 'next/head';

const Dashboard = () => {
  const [news, setNews] = useState([]);
  const [heatMapData, setHeatMapData] = useState({});
  const [wsStatus, setWsStatus] = useState('Disconnected');

  useEffect(() => {
    // WebSocket setup
    const socket = new WebSocket('ws://localhost:8000/ws');

    socket.onopen = () => {
      setWsStatus('Connected');
      console.log('Connected to WebSocket server');
    };

    socket.onmessage = (event) => {
      const newsItem = JSON.parse(event.data);
      
      // Update news list (keep last 10)
      setNews((prevNews) => [newsItem, ...prevNews].slice(0, 10));
      
      // Update heatmap data (cumulative or latest impact)
      setHeatMapData((prevData) => ({
        ...prevData,
        ...newsItem.sector_impacts
      }));
    };

    socket.onclose = () => {
      setWsStatus('Disconnected');
      console.log('Disconnected from WebSocket server');
    };

    return () => {
      socket.close();
    };
  }, []);

  // Helper to color code sector impact
  const getImpactColor = (impact) => {
    if (impact > 3) return 'bg-green-600 text-white';
    if (impact > 0) return 'bg-green-200 text-green-800';
    if (impact < -3) return 'bg-red-600 text-white';
    if (impact < 0) return 'bg-red-200 text-red-800';
    return 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6 font-sans">
      <Head>
        <title>Financial NewsBoard | Real-time Dashboard</title>
      </Head>

      <header className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Real-time Financial NewsBoard</h1>
        <div className="flex items-center space-x-4">
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${wsStatus === 'Connected' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
            Status: {wsStatus}
          </span>
          <span className="text-gray-500 text-sm">{new Date().toLocaleTimeString()}</span>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* News Stream */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-xl font-semibold mb-4 border-b pb-2">Live News Stream</h2>
          {news.length === 0 ? (
            <p className="text-gray-500 italic">Waiting for incoming news...</p>
          ) : (
            news.map((item) => (
              <div key={item.id} className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-1 rounded">
                    {item.platform}
                  </span>
                  <span className={`text-xs font-semibold px-2 py-1 rounded ${item.credibility_score >= 80 ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                    Score: {item.credibility_score}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-gray-800 mb-2">{item.title}</h3>
                <div className="text-sm text-gray-600 mb-4 whitespace-pre-wrap bg-gray-50 p-3 rounded italic border-l-4 border-gray-300">
                  {item.ai_summary}
                </div>
                <div className="flex flex-wrap gap-2 mt-2">
                  {Object.entries(item.sector_impacts).map(([sector, impact]) => (
                    <span key={sector} className={`text-xs px-2 py-1 rounded font-medium ${getImpactColor(impact)}`}>
                      {sector}: {impact > 0 ? `+${impact}` : impact}
                    </span>
                  ))}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Heatmap/Sector Impact */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4 border-b pb-2">Sector Impact Heatmap</h2>
          <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
            <div className="grid grid-cols-2 gap-2">
              {Object.keys(heatMapData).length === 0 ? (
                <p className="col-span-2 text-gray-400 text-center py-10">No impact data yet</p>
              ) : (
                Object.entries(heatMapData).map(([sector, impact]) => (
                  <div key={sector} className={`p-3 rounded-md text-center text-xs font-bold flex flex-col justify-center items-center h-16 ${getImpactColor(impact)}`}>
                    <div className="opacity-80">{sector}</div>
                    <div className="text-sm mt-1">{impact > 0 ? `+${impact}` : impact}</div>
                  </div>
                ))
              )}
            </div>
          </div>
          
          {/* Legend */}
          <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 mt-4">
            <h4 className="text-xs font-bold uppercase text-gray-500 mb-2">Legend</h4>
            <div className="flex items-center justify-between text-xs">
              <span className="bg-red-600 text-white px-2 py-0.5 rounded">High Risk (-5)</span>
              <span className="bg-gray-100 text-gray-800 px-2 py-0.5 rounded">Neutral (0)</span>
              <span className="bg-green-600 text-white px-2 py-0.5 rounded">High Opportunity (+5)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
