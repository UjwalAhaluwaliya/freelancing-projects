"use client";

import { Line } from "react-chartjs-2";
import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale } from "chart.js";
import { useEffect, useState } from "react";

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale);

export default function HospitalGraph({
  start,
  hid,
}: {
  start: boolean;
  hid: number;
}) {
  const [metrics, setMetrics] = useState<any>({
    round: [],
    accuracy: [],
    loss: [],
  });

  useEffect(() => {
    if (!start) return;

    const interval = setInterval(async () => {
      const res = await fetch(`http://127.0.0.1:5000/metrics/${hid}`);
      const data = await res.json();

      setMetrics(data);

      if (data.round.length >= 5) clearInterval(interval);
    }, 2000);

    return () => clearInterval(interval);
  }, [start, hid]);

  if (!start) return <p className="text-gray-400 text-center">Training not started</p>;
  if (metrics.round.length === 0) return <p>Loading graph...</p>;

  const bestAcc = Math.max(...metrics.accuracy).toFixed(2);
  const avgAcc = (
    metrics.accuracy.reduce((a: number, b: number) => a + b, 0) /
    metrics.accuracy.length
  ).toFixed(2);

  const finalLoss = metrics.loss[metrics.loss.length - 1].toFixed(2);

  const chartData = {
    labels: metrics.round,
    datasets: [
      { label: "Accuracy", data: metrics.accuracy, borderColor: "lime" },
      { label: "Loss", data: metrics.loss, borderColor: "red" },
    ],
  };

  return (
    <div className="text-white">

      <Line data={chartData} />

      <div className="grid grid-cols-2 gap-4 mt-6 text-sm">
        <div className="bg-gray-900 p-3 rounded">
          <p>Best Accuracy</p>
          <p className="text-green-400 font-bold">{bestAcc}</p>
        </div>

        <div className="bg-gray-900 p-3 rounded">
          <p>Average Accuracy</p>
          <p className="text-blue-400 font-bold">{avgAcc}</p>
        </div>

        <div className="bg-gray-900 p-3 rounded">
          <p>Final Loss</p>
          <p className="text-red-400 font-bold">{finalLoss}</p>
        </div>

        <div className="bg-gray-900 p-3 rounded">
          <p>Total Rounds</p>
          <p className="text-purple-400 font-bold">{metrics.round.length}</p>
        </div>
      </div>

      {metrics.round.length >= 5 && (
        <p className="text-green-400 mt-4 text-center font-semibold">
          Federated training completed successfully ✔
        </p>
      )}

      <p className="text-gray-400 mt-4 text-center text-sm">
        Local hospital training improved prediction accuracy without exposing raw patient data,
        demonstrating privacy-preserving collaborative learning.
      </p>

    </div>
  );
}
