import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  Cell,
  ScatterChart,
  Scatter
} from "recharts";
import ChartCard from "./ChartCard";

const COLORS = ["#0f766e", "#ea580c", "#1d4ed8", "#4d7c0f", "#9333ea", "#be185d"];

export function RoiDistributionChart({ data }) {
  return (
    <ChartCard title="ROI Distribution">
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="bucket" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#1d4ed8" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

export function RiskDistributionChart({ data }) {
  return (
    <ChartCard title="Risk Distribution">
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={90} label>
            {data.map((entry, idx) => (
              <Cell key={entry.name} fill={COLORS[idx % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

export function PriorityChart({ data }) {
  return (
    <ChartCard title="Portfolio Priority Scores">
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data.slice(0, 10)}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" tick={{ fontSize: 10 }} interval={0} angle={-30} textAnchor="end" height={70} />
          <YAxis />
          <Tooltip />
          <Bar dataKey="score" fill="#0f766e" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

export function ClusterChart({ data }) {
  return (
    <ChartCard title="Project Clusters">
      <ResponsiveContainer width="100%" height={280}>
        <ScatterChart>
          <CartesianGrid />
          <XAxis type="number" dataKey="budget" name="Budget" />
          <YAxis type="number" dataKey="roi" name="ROI" />
          <Tooltip cursor={{ strokeDasharray: "3 3" }} />
          <Legend />
          <Scatter name="Projects" data={data} fill="#ea580c" />
        </ScatterChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}
