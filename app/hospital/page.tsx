"use client";

import { useEffect, useState } from "react";
import HospitalGraph from "@/components/HospitalGraph";
import { auth } from "@/lib/firebase";
import { onAuthStateChanged } from "firebase/auth";
import { useRouter } from "next/navigation";

const hospitalMeta: any = {
  1: { disease: "Diabetes", quality: "High" },
  2: { disease: "Diabetes", quality: "Medium" },
  3: { disease: "Heart", quality: "High" },
  4: { disease: "Heart", quality: "Low" },
};

export default function Hospital() {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("idle");
  const [startGraph, setStartGraph] = useState(false);
  const [hospitalId, setHospitalId] = useState<number | null>(null);

  const router = useRouter();

  // 🔐 Protect Route
  useEffect(() => {
    const unsub = onAuthStateChanged(auth, async (user) => {
      if (!user) {
        router.push("/login");
        return;
      }

      const email = user.email || "";
      let hid = 1;

      if (email.includes("hospital2")) hid = 2;
      if (email.includes("hospital3")) hid = 3;
      if (email.includes("hospital4")) hid = 4;

      setHospitalId(hid);

      

      setStartGraph(false);
      setProgress(0);
      setStatus("idle");
    });

    return () => unsub();
  }, [router]);

  const startTraining = async () => {
    if (!hospitalId) return;

    await fetch("http://127.0.0.1:5000/start-training");

    setStartGraph(true);

    const interval = setInterval(async () => {
      const res = await fetch("http://127.0.0.1:5000/status");
      const data = await res.json();

      setProgress(data.progress);
      setStatus(data.status);

      if (data.status === "complete") clearInterval(interval);
    }, 200);
  };

  if (!hospitalId)
    return <p className="text-white text-center mt-20">Loading hospital...</p>;

  const meta = hospitalMeta[hospitalId];

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center gap-6 p-6">

      <h1 className="text-3xl font-bold">
        Hospital {hospitalId} Node 🏥
      </h1>

      <div className="bg-gray-900 p-4 rounded-xl text-center w-full max-w-md">

        <p>
          🩺 Specialization:{" "}
          <span className={`font-bold ${
            meta.disease === "Diabetes"
              ? "text-green-400"
              : "text-red-400"
          }`}>
            {meta.disease}
          </span>
        </p>

        <p>
          📊 Data Quality:{" "}
          <span className="text-yellow-400">
            {meta.quality}
          </span>
        </p>

        <p className="text-gray-400 mt-2 text-sm">
          This hospital contributes to the {meta.disease} federated learning network.
        </p>

      </div>

      <button
        onClick={startTraining}
        className="bg-purple-600 px-6 py-3 rounded-lg hover:scale-105 transition"
      >
        Start Training
      </button>

      <div className="w-80 bg-gray-800 rounded-full h-6 overflow-hidden">
        <div
          className="bg-green-500 h-full transition-all"
          style={{ width: `${progress}%` }}
        ></div>
      </div>

      <p>Status: {status}</p>

      <div className="w-full max-w-3xl mt-6">
        <HospitalGraph start={startGraph} hid={hospitalId} />
      </div>

      <p className="text-gray-400 text-sm text-center max-w-xl mt-4">
        Accuracy represents how correctly the AI model predicts patient outcomes.
        If accuracy increases over training rounds, it means the hospital's
        patient data is improving the shared federated model.
        Loss represents prediction error — lower loss means fewer mistakes.
      </p>

    </div>
  );
}