"use client";

import Link from "next/link";
import { auth } from "@/lib/firebase";
import { signOut, onAuthStateChanged } from "firebase/auth";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function Navbar() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (u) => {
      setUser(u);
    });
    return () => unsub();
  }, []);

  const logout = async () => {
    await signOut(auth);
    router.push("/");
  };

  return (
    <nav className="bg-gray-900 text-white px-6 py-4 flex justify-between items-center">

      <div className="font-bold text-lg">
        <Link href="/">Federated AI System</Link>
      </div>

      <div className="flex gap-6 items-center">

        <Link href="/">Home</Link>

        {/* PATIENT */}
        <Link href={user ? "/patient" : "/patient-auth"}>
          Patient
        </Link>

        {/* HOSPITAL */}
        <Link href={user ? "/hospital" : "/login"}>
          Hospital
        </Link>

        {/* ADMIN */}
        <Link href={user ? "/admin" : "/login"}>
          Admin
        </Link>

        {/* AUTH BUTTON */}
        {user && (
          <button
            onClick={logout}
            className="bg-red-600 px-3 py-1 rounded"
          >
            Logout
          </button>
        )}

      </div>
    </nav>
  );
}