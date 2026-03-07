"use client";

import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "@/lib/firebase";
import { useState } from "react";
import { useRouter } from "next/navigation"; // Optimized for Next.js

export default function Login() {
  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async () => {
    if (!email || !pass) return alert("Please fill in all fields");
    
    setLoading(true);
    try {
      await signInWithEmailAndPassword(auth, email, pass);

      // 🧭 Role-Based Redirection Logic
      const lowerEmail = email.toLowerCase();

      if (lowerEmail.includes("admin")) {
        router.push("/admin");
      } else if (lowerEmail.includes("hospital")) {
        router.push("/hospital");
      } else if (lowerEmail.includes("patient")) {
        router.push("/patient-dashboard");
      } else {
        // Default fallback for general users
        router.push("/patient-dashboard");
      }

    } catch (err: any) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gradient-to-br from-black via-purple-950 to-black overflow-hidden">
      
      {/* Background Glow */}
      <div className="absolute w-[600px] h-[600px] bg-purple-600 blur-[150px] opacity-20 rounded-full animate-pulse"></div>

      <div className="relative backdrop-blur-2xl bg-white/5 border border-white/10 p-10 rounded-3xl shadow-2xl w-full max-w-md mx-4">
        
        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            Federated <span className="text-purple-400">AI</span>
          </h1>
          <p className="text-gray-400 text-sm mt-2">Secure Healthcare Portal Access</p>
        </div>

        <div className="space-y-4">
          <div>
            <label className="text-xs font-semibold text-purple-300 uppercase ml-1">Email Address</label>
            <input
              type="email"
              placeholder="e.g. patient@test.com"
              className="w-full p-3 mt-1 rounded-xl bg-black/50 border border-purple-500/20 text-white focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-purple-300 uppercase ml-1">Password</label>
            <input
              type="password"
              placeholder="••••••••"
              className="w-full p-3 mt-1 rounded-xl bg-black/50 border border-purple-500/20 text-white focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
              onChange={(e) => setPass(e.target.value)}
            />
          </div>

          <button
            onClick={handleLogin}
            disabled={loading}
            className={`w-full py-4 mt-4 rounded-xl bg-gradient-to-r from-purple-600 to-pink-500 text-white font-bold shadow-lg shadow-purple-500/20 hover:shadow-purple-500/40 hover:scale-[1.02] active:scale-95 transition-all ${
              loading ? "opacity-50 cursor-not-allowed" : ""
            }`}
          >
            {loading ? "Authenticating..." : "Sign In"}
          </button>
        </div>

        <p className="text-center text-gray-500 text-xs mt-6">
          Access restricted to authorized personnel and registered patients.
        </p>
      </div>
    </div>
  );
}