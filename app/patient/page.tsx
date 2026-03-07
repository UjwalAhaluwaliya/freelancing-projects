"use client";

import { useState } from "react";

export default function Patient() {
  const [glucose, setGlucose] = useState("");
  const [cholesterol, setCholesterol] = useState("");
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async () => {
    const res = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ glucose, cholesterol }),
    });

    const data = await res.json();
    setResult(data);
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center p-8">

      <h1 className="text-3xl font-bold mb-6">
        Patient Risk Assessment 🧑‍⚕️
      </h1>

      <div className="bg-gray-900 p-6 rounded-xl w-full max-w-md">

        <label className="block mb-2">Glucose Level</label>
        <input
          type="number"
          className="w-full p-2 mb-4 bg-black border border-gray-600 rounded"
          value={glucose}
          onChange={(e) => setGlucose(e.target.value)}
        />

        <label className="block mb-2">Cholesterol Level</label>
        <input
          type="number"
          className="w-full p-2 mb-4 bg-black border border-gray-600 rounded"
          value={cholesterol}
          onChange={(e) => setCholesterol(e.target.value)}
        />

        <button
          onClick={handleSubmit}
          className="w-full bg-purple-600 py-2 rounded mt-2"
        >
          Analyze
        </button>

      </div>

      {result && (
  <div className="mt-8 bg-gray-900 p-6 rounded-xl w-full max-w-md text-center">

    <h2 className="text-xl font-bold mb-4">
      Risk Assessment Result
    </h2>

    <p>
      Detected Condition:{" "}
      <span className="text-green-400 font-bold">
        {result.predicted_disease.toUpperCase()}
      </span>
    </p>

    <p className="mt-2">
      Risk Score:{" "}
      <span className="text-yellow-400 font-bold">
        {result.risk_score}%
      </span>
    </p>

    <p className="mt-2 text-gray-400">
      Model Used: {result.model_used}
    </p>

    {/* 🏥 Hospital Recommendation */}
    <div className="mt-6 border-t border-gray-700 pt-4">

      <h3 className="text-lg font-bold mb-2">
        Recommended Hospital
      </h3>

      <p>
        Hospital {result.recommended_hospital}
      </p>

      <p className="text-sm text-gray-400 mt-2">
        This hospital has the highest model accuracy (
        {result.hospital_accuracy}% ) for
        {result.predicted_disease} prediction.
      </p>

      <p className="mt-3 text-gray-500 text-sm">
        Recommendation is based on federated model performance
        comparison across hospitals.
      </p>

    </div>

  </div>
)}

    </div>
  );
}