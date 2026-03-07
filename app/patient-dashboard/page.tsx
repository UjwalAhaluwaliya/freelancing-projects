"use client";

import { auth } from "@/lib/firebase";
import { onAuthStateChanged } from "firebase/auth";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function PatientDashboard() {
  const [email, setEmail] = useState("");
  const router = useRouter();

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (user) => {
      if (!user) {
        router.push("/login");
        return;
      }
      setEmail(user.email || "");
    });

    return () => unsub();
  }, [router]);

  return (
    <div className="min-h-screen text-white flex flex-col items-center justify-center">

      <h1 className="text-3xl font-bold mb-4">
        Welcome Patient
      </h1>

      <p className="text-gray-400">
        Logged in as: {email}
      </p>

      <p className="mt-4 text-gray-400 max-w-xl text-center">
        You can submit your medical data through the Patient page
        to receive AI-based disease risk assessment.
      </p>

    </div>
  );
}