const BASE_URL = "http://127.0.0.1:8000";

export type Metrics = {
  totalTrades: number;
  wins: number;
  planAdherenceScore: number;
  revengeTrades: number;
  sessionTilt: Record<string, number>;
  winRateByEmotion: Record<string, number>;
  overtradingDetected: boolean;
};

export const getMetrics = async (
  userId: string,
  token: string
): Promise<Metrics> => {
  const res = await fetch(`${BASE_URL}/users/${userId}/metrics`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.json();
};

export const createTrade = async (
  data: any,
  token: string
) => {
  const res = await fetch(`${BASE_URL}/trades`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });
  return res.json();
};