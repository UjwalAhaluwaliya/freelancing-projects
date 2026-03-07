import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyD3oceBdS-f668aHgwbk_PreyXKBnorFGE",
  authDomain: "federated-healthcare.firebaseapp.com",
  projectId: "federated-healthcare",
  storageBucket: "federated-healthcare.firebasestorage.app",
  messagingSenderId: "329166704294",
  appId: "1:329166704294:web:5e683cf5ec5843c970ee67"
};


const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db = getFirestore(app);
