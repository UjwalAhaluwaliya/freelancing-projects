import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-[calc(100vh-64px)] flex flex-col items-center justify-center text-center px-6">
      
      {/* Hero Section */}
      <h1 className="text-5xl md:text-6xl font-extrabold mb-6 bg-gradient-to-r from-blue-400 to-teal-400 bg-clip-text text-transparent">
        Multi-Disease Federated AI Platform
      </h1>

      <p className="max-w-3xl text-gray-400 text-lg md:text-xl mb-10">
        Empowering hospitals to collaboratively train AI models 
        <span className="text-white"> without moving patient data</span>. 
        Privacy-first healthcare intelligence.
      </p>

      {/* Feature Grid */}
      <div className="grid md:grid-cols-3 gap-6 w-full max-w-6xl">
        <FeatureCard 
          title="Hospitals" 
          desc="Train disease-specific AI models locally while preserving patient privacy." 
        />
        <FeatureCard 
          title="Admin" 
          desc="Monitor global convergence and compare federated network performance." 
        />
        <FeatureCard 
          title="Patients" 
          desc="Submit medical indicators to receive AI-based risk assessment." 
        />
      </div>
    </div>
  );
}

// Reusable Card Component for cleaner code
function FeatureCard({ title, desc }: { title: string; desc: string }) {
  return (
    <div className="bg-gray-900/50 border border-gray-800 p-8 rounded-2xl hover:border-blue-500/50 transition-colors">
      <h2 className="text-2xl font-bold mb-3 text-blue-400">{title}</h2>
      <p className="text-gray-400 text-sm leading-relaxed">
        {desc}
      </p>
    </div>
  );
}