"use client";

import { useEffect, useState } from "react";
import { getMetrics, Metrics } from "./services/api";

export default function Home() {
  const [data, setData] = useState<Metrics | null>(null);

  const userId = "f412f236-4edc-47a2-8f54-8763a6ed2ce8";
  const token = "PASTE_YOUR_TOKEN";

  useEffect(() => {
    getMetrics(userId, token).then(setData);
  }, []);

  if (!data) return <p>Loading...</p>;

  return (
    <div style={{ padding: 20 }}>
      <h1>Trading Dashboard</h1>

      <p>Total Trades: {data.totalTrades}</p>
      <p>Wins: {data.wins}</p>
      <p>Plan Adherence: {data.planAdherenceScore.toFixed(2)}</p>
      <p>Revenge Trades: {data.revengeTrades}</p>
      <p>Overtrading: {data.overtradingDetected ? "Yes" : "No"}</p>

      <h3>Win Rate by Emotion</h3>
      {Object.entries(data.winRateByEmotion).map(([k, v]) => (
        <p key={k}>
          {k}: {v.toFixed(2)}
        </p>
      ))}

      <h3>Session Tilt</h3>
      {Object.entries(data.sessionTilt).map(([k, v]) => (
        <p key={k}>
          {k}: {v.toFixed(2)}
        </p>
      ))}
    </div>
  );
}