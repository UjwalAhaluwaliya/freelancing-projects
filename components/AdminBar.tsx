"use client";

import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale } from "chart.js";
import { useEffect, useState } from "react";

ChartJS.register(BarElement, CategoryScale, LinearScale);

export default function AdminBar() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const interval = setInterval(async () => {
      const res = await fetch("http://127.0.0.1:5000/admin/hospitals");
      const metrics = await res.json();

      setData({
        labels: Object.keys(metrics).map((h) => `Hospital ${h}`),
        datasets: [
          {
            label: "Average Accuracy",
            data: Object.values(metrics),
            backgroundColor: "purple",
          },
        ],
      });
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  if (!data) return <p className="text-gray-400">Loading hospital comparison...</p>;

  return (
    <div className="text-white">

      <Bar data={data} />

      <p className="text-gray-400 mt-4 text-center text-sm">
        This chart compares the average contribution of each hospital to the
        federated model. Higher accuracy indicates stronger local learning
        influence on the global model.
      </p>

    </div>
  );
}
