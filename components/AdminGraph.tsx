"use client";

import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
} from "chart.js";
import { useEffect, useState } from "react";

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale);

export default function AdminGraph({ disease }: { disease: string }) {
  const [metrics, setMetrics] = useState<any>({
    round: [],
    accuracy: [],
    loss: [],
  });

  useEffect(() => {
    const interval = setInterval(async () => {
      const res = await fetch(
        `http://127.0.0.1:5000/admin/global/${disease}`
      );
      const data = await res.json();
      setMetrics(data);
    }, 2000);

    return () => clearInterval(interval);
  }, [disease]);

  if (metrics.round.length === 0)
    return <p className="text-gray-400">Waiting for hospitals to train...</p>;

  const bestAcc = Math.max(...metrics.accuracy);
  const bestAccPercent = (bestAcc * 100).toFixed(0);

  const chartData = {
    labels: metrics.round,
    datasets: [
      {
        label: `${disease.toUpperCase()} Global Accuracy (%)`,
        data: metrics.accuracy.map((a: number) => a * 100),
        borderColor: "cyan",
      },
    ],
  };

  return (
    <div>
      <Line data={chartData} />

      <div className="mt-4 text-sm text-gray-300">
        <p>
          🏆 Best Global Accuracy:{" "}
          <span className="text-green-400 font-bold">
            {bestAccPercent}%
          </span>
        </p>

        <p className="mt-3 text-gray-400">
          This means the AI model for {disease} predictions is correctly
          identifying patients about {bestAccPercent}% of the time.
        </p>
      </div>
    </div>
  );
}