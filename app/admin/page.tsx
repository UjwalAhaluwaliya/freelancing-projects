"use client";

import AdminGraph from "@/components/AdminGraph";
import { useEffect, useState } from "react";
import { auth } from "@/lib/firebase";
import { onAuthStateChanged } from "firebase/auth";
import { useRouter } from "next/navigation";

export default function Admin() {
  const router = useRouter();

  const [winner, setWinner] = useState<string>("");

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (user) => {
      if (!user) router.push("/login");
    });

    return () => unsub();
  }, [router]);

  // Simple winner logic (based on backend static values)
  useEffect(() => {
    async function checkWinner() {
      const d = await fetch(
        "http://127.0.0.1:5000/admin/global/diabetes"
      );
      const h = await fetch(
        "http://127.0.0.1:5000/admin/global/heart"
      );

      const diabetes = await d.json();
      const heart = await h.json();

      if (
        diabetes.accuracy &&
        heart.accuracy &&
        diabetes.accuracy.length > 0 &&
        heart.accuracy.length > 0
      ) {
        const dBest = Math.max(...diabetes.accuracy);
        const hBest = Math.max(...heart.accuracy);

        setWinner(dBest > hBest ? "Diabetes" : "Heart");
      }
    }

    checkWinner();
  }, []);

  return (
    <div className="min-h-screen bg-black text-white p-8">

      <h1 className="text-4xl font-bold text-center mb-10">
        Multi-Disease Federated Admin Dashboard 🌍
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-10">

        <div className="bg-gray-900 p-6 rounded-xl">
          <h2 className="text-xl font-bold mb-4">🩸 Diabetes Network</h2>
          <AdminGraph disease="diabetes" />
        </div>

        <div className="bg-gray-900 p-6 rounded-xl">
          <h2 className="text-xl font-bold mb-4">❤️ Heart Network</h2>
          <AdminGraph disease="heart" />
        </div>

      </div>

      {/* Winner Section */}
      {winner && (
        <div className="mt-12 bg-gray-900 p-6 rounded-xl text-center">
          <h2 className="text-xl font-bold mb-4">
            🏆 Stronger Network: {winner}
          </h2>

          <p className="text-gray-300">
            Based on current training results, the {winner} network
            shows higher predictive reliability across hospitals.
          </p>

          <p className="mt-4 text-gray-400 text-sm">
            Higher accuracy means the AI system is more confident
            and consistent in identifying patients correctly.
          </p>
        </div>
      )}

      {/* Simple Explanation */}
      <div className="mt-8 bg-gray-900 p-6 rounded-xl text-center">
        <h2 className="text-xl font-bold mb-4">
          💡 What This Means
        </h2>

        <p className="text-gray-300">
          Hospitals collaborate without sharing patient data.
          Each hospital improves the shared AI model locally.
        </p>

        <p className="mt-3 text-gray-300">
          The system combines learning from all hospitals
          to create a stronger global model.
        </p>

        <p className="mt-4 text-gray-400 text-sm">
          The more stable and higher the accuracy,
          the more reliable the AI predictions become.
        </p>
      </div>

    </div>
  );
}