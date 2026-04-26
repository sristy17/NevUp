"use client";

import { useEffect, useState } from "react";
import { getMetrics, createTrade, Metrics } from "./services/api";

export default function Home() {
  const [data, setData] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(false);

  const userId = "f412f236-4edc-47a2-8f54-8763a6ed2ce8";
  const token = "PASTE_YOUR_TOKEN";

  const loadMetrics = () => {
    getMetrics(userId, token).then((res) => setData(res || null));
  };

  useEffect(() => {
    loadMetrics();
  }, []);

  const generateTrade = () => {
    const isWin = Math.random() > 0.5;
    const emotions = ["calm", "anxious", "fearful", "neutral"];

    return {
      tradeId: "ui-" + Date.now() + Math.random(),
      userId,
      sessionId: "session-" + Math.floor(Math.random() * 4),
      asset: "AAPL",
      assetClass: "equity",
      direction: "long",
      entryPrice: 100,
      exitPrice: isWin ? 120 : 80,
      quantity: Math.floor(Math.random() * 10) + 1,
      entryAt: new Date().toISOString(),
      exitAt: new Date().toISOString(),
      status: "closed",
      planAdherence: Math.floor(Math.random() * 5),
      emotionalState: emotions[Math.floor(Math.random() * emotions.length)],
      entryRationale: "Simulated trade",
    };
  };

  const handleSubmit = async () => {
    setLoading(true);
    await createTrade(generateTrade(), token);
    setLoading(false);
    loadMetrics();
  };

  const simulateTrades = async () => {
    setLoading(true);
    for (let i = 0; i < 20; i++) {
      await createTrade(generateTrade(), token);
    }
    setLoading(false);
    loadMetrics();
  };

  if (!data) return <p>Loading...</p>;

  const winRateByEmotion = data.winRateByEmotion || {};
  const sessionTilt = data.sessionTilt || {};

  return (
    <div style={{ padding: 30, fontFamily: "Arial", color: "#fff", background: "#0f172a", minHeight: "100vh" }}>
      <h1 style={{ marginBottom: 20 }}>Trading Dashboard</h1>

      <div style={{ marginBottom: 20, background: "#1e293b", padding: 15, borderRadius: 10 }}>
        <h3>Insights</h3>
        <p>Best performance observed in calm emotional state.</p>
        <p>{data.revengeTrades > 5 ? "Frequent revenge trading detected" : "Revenge trading is under control"}</p>
        <p>{data.overtradingDetected ? "Overtrading behavior detected" : "No overtrading detected"}</p>
      </div>

      <div style={{ marginBottom: 20 }}>
        <button
          onClick={handleSubmit}
          disabled={loading}
          style={{
            padding: "10px 20px",
            background: "#2563eb",
            color: "#fff",
            border: "none",
            borderRadius: 8,
            cursor: "pointer",
            marginRight: 10,
          }}
        >
          {loading ? "Submitting..." : "Add Trade"}
        </button>

        <button
          onClick={simulateTrades}
          disabled={loading}
          style={{
            padding: "10px 20px",
            background: "#16a34a",
            color: "#fff",
            border: "none",
            borderRadius: 8,
            cursor: "pointer",
          }}
        >
          Simulate Trades
        </button>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: 15 }}>
        {[
          { label: "Total Trades", value: data.totalTrades || 0 },
          { label: "Wins", value: data.wins || 0 },
          { label: "Plan Adherence", value: data.planAdherenceScore ? data.planAdherenceScore.toFixed(2) : "0.00" },
          { label: "Revenge Trades", value: data.revengeTrades || 0 },
          { label: "Overtrading", value: data.overtradingDetected ? "Yes" : "No" },
        ].map((item) => (
          <div
            key={item.label}
            style={{
              background: "#1e293b",
              padding: 15,
              borderRadius: 10,
              textAlign: "center",
            }}
          >
            <p style={{ fontSize: 12, color: "#94a3b8" }}>{item.label}</p>
            <h2>{item.value}</h2>
          </div>
        ))}
      </div>

      <h2 style={{ marginTop: 30 }}>Win Rate by Emotion</h2>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 10 }}>
        {Object.entries(winRateByEmotion).map(([k, v]) => (
          <div
            key={k}
            style={{
              background: "#1e293b",
              padding: 10,
              borderRadius: 8,
              textAlign: "center",
            }}
          >
            <p>{k}</p>
            <strong>{((v as number) * 100).toFixed(0)}%</strong>
          </div>
        ))}
      </div>

      <h2 style={{ marginTop: 30 }}>Session Tilt</h2>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 10 }}>
        {Object.entries(sessionTilt).map(([k, v]) => {
          const val = v as number;
          const isRisky = val > 0.5;

          return (
            <div
              key={k}
              style={{
                background: isRisky ? "#7f1d1d" : "#1e293b",
                padding: 10,
                borderRadius: 8,
                border: isRisky ? "1px solid red" : "none",
              }}
            >
              <p style={{ fontSize: 12 }}>{k.slice(0, 10)}...</p>
              <strong>{(val * 100).toFixed(0)}%</strong>
              {isRisky && <p style={{ color: "red" }}>Risky Session</p>}
            </div>
          );
        })}
      </div>
    </div>
  );
}