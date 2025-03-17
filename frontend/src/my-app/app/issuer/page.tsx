"use client"

import { useState } from "react";
import Navbar from "@/components/navbar";
import Footer from "@/components/footer";

export default function IssuerPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [holderAddress, setHolderAddress] = useState("");
  const [issuerAddress, setIssuerAddress] = useState("");
  const [issuerName, setIssuerName] = useState("");
  const [result, setResult] = useState<{ success: boolean; message: string } | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleIssueCredential = async () => {
    if (!selectedFile || !holderAddress || !issuerAddress || !issuerName) {
      setResult({ success: false, message: "Please fill out all fields and select a file." });
      return;
    }

    try {
      const pdfArrayBuffer = await selectedFile.arrayBuffer();
      const hashBuffer = await crypto.subtle.digest("SHA-256", pdfArrayBuffer);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      const credentialHash = "0x" + hashArray.map(b => b.toString(16).padStart(2, "0")).join("");

      const formData = new FormData();
      formData.append("credentialHash", credentialHash);
      formData.append("holderAddress", holderAddress);
      formData.append("issuerAddress", issuerAddress);
      formData.append("issuerName", issuerName);

      const response = await fetch("http://localhost:5000/api/issue-credential", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      if (result.success) {
        setResult({ success: true, message: `Credential Issued! Transaction Hash: ${result.transactionHash}` });
      } else {
        setResult({ success: false, message: `Error: ${result.error}` });
      }
    } catch (error: any) {
      setResult({ success: false, message: `Error: ${error.message}` });
    }
  };

  return (
    <div className="relative min-h-screen">
      {/* Background gradients */}
      <div className="pointer-events-none fixed inset-0">
        <div className="absolute inset-0 bg-gradient-to-b from-background via-background/90 to-background" />
        <div className="absolute right-0 top-0 h-[500px] w-[500px] bg-blue-500/10 blur-[100px] animate-fade-in" />
        <div className="absolute bottom-0 left-0 h-[500px] w-[500px] bg-purple-500/10 blur-[100px] animate-fade-in" />
      </div>

      <div className="relative z-10">
        <Navbar />
        <main className="flex flex-col items-center p-8 md:p-24 text-white">
          <section className="w-full max-w-7xl mb-16 text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6 animate-slide-up">Issue New Credential</h1>
            <p className="text-lg text-gray-300 mb-6">Fill out the details below and upload a PDF.</p>

            <div className="space-y-4">
              <input
                type="file"
                accept="application/pdf"
                onChange={handleFileChange}
                className="block w-full p-2 border border-gray-300 rounded-lg bg-white text-black"
              />
              <input
                type="text"
                placeholder="Recipient's Ethereum Address"
                value={holderAddress}
                onChange={(e) => setHolderAddress(e.target.value)}
                className="block w-full p-2 border border-gray-300 rounded-lg bg-white text-black"
              />
              <input
                type="text"
                placeholder="Your Issuer Address"
                value={issuerAddress}
                onChange={(e) => setIssuerAddress(e.target.value)}
                className="block w-full p-2 border border-gray-300 rounded-lg bg-white text-black"
              />
              <input
                type="text"
                placeholder="Institution Name"
                value={issuerName}
                onChange={(e) => setIssuerName(e.target.value)}
                className="block w-full p-2 border border-gray-300 rounded-lg bg-white text-black"
              />
            </div>

            <button
              onClick={handleIssueCredential}
              className="bg-teal-500 hover:bg-teal-600 text-white font-medium py-3 px-6 rounded-lg transition-colors mt-6"
            >
              Issue Credential
            </button>

            {result && (
              <div className={`mt-4 p-4 rounded-lg ${result.success ? "bg-green-500" : "bg-red-500"}`}>
                {result.message}
              </div>
            )}
          </section>
        </main>
        <Footer />
      </div>
    </div>
  );
}
