"use client"

import { useState } from "react";
import Navbar from "@/components/navbar";
import Footer from "@/components/footer";

export default function IssuerPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [holderAddress, setHolderAddress] = useState("");
  const [issuerAddress, setIssuerAddress] = useState("");
  const [issuerName, setIssuerName] = useState("");
  const [metadata, setMetadata] = useState(""); // Added metadata state
  const [result, setResult] = useState<{ success: boolean; message: string } | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleIssueCredential = async () => {
    // Check if all required fields are filled
    if (!selectedFile || !holderAddress || !issuerAddress || !issuerName || !metadata) {
      setResult({ success: false, message: "Please fill out all fields and select a file." });
      return;
    }

    try {
      // Convert the selected PDF file to an ArrayBuffer and generate its SHA-256 hash
      const pdfArrayBuffer = await selectedFile.arrayBuffer();
      const hashBuffer = await crypto.subtle.digest("SHA-256", pdfArrayBuffer);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      const credentialHash = "0x" + hashArray.map(b => b.toString(16).padStart(2, "0")).join("");

      // Create the form data to be sent
      const formData = new FormData();
      formData.append("credentialHash", credentialHash);
      formData.append("holderAddress", holderAddress);
      formData.append("issuerAddress", issuerAddress);
      formData.append("issuerName", issuerName);
      formData.append("metadata", metadata); // Append metadata to the form data

      // Make a POST request to the API
      const response = await fetch("http://localhost:5000/api/issue-credential", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      // Handle the response from the server
      if (result.success) {
        setResult({ success: true, message: `Credential Issued! Transaction Hash: ${result.transactionHash}` });
      } else {
        setResult({ success: false, message: `Error: ${result.error || "Unknown error"}` });
      }
    } catch (error: any) {
      setResult({ success: false, message: `Error: ${error.message || "Unexpected error"}` });
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
          <section className="w-full max-w-3xl mb-16 bg-gray-800/60 p-8 rounded-xl shadow-lg">
            <h1 className="text-4xl md:text-5xl font-bold mb-6 animate-slide-up text-center">Issue New Credential</h1>
            <p className="text-lg text-gray-300 mb-6 text-center">Fill out the details below and upload a PDF.</p>

            {/* Left-aligned Form */}
            <div className="bg-gray-700/50 p-6 rounded-lg shadow-md space-y-4">
              <div className="flex flex-col">
                <label className="text-gray-300 text-sm font-medium mb-1">Upload Credential (PDF)</label>
                <input
                  type="file"
                  accept="application/pdf"
                  onChange={handleFileChange}
                  className="p-3 border border-gray-500 rounded-lg bg-gray-900 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
                />
              </div>

              <div className="flex flex-col">
                <label className="text-gray-300 text-sm font-medium mb-1">Recipient's Ethereum Address</label>
                <input
                  type="text"
                  value={holderAddress}
                  onChange={(e) => setHolderAddress(e.target.value)}
                  placeholder="Enter recipient's Ethereum address"
                  className="p-3 border border-gray-500 rounded-lg bg-gray-900 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-400"
                />
              </div>

              <div className="flex flex-col">
                <label className="text-gray-300 text-sm font-medium mb-1">Your Issuer Address</label>
                <input
                  type="text"
                  value={issuerAddress}
                  onChange={(e) => setIssuerAddress(e.target.value)}
                  placeholder="Enter your Ethereum issuer address"
                  className="p-3 border border-gray-500 rounded-lg bg-gray-900 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-400"
                />
              </div>

              <div className="flex flex-col">
                <label className="text-gray-300 text-sm font-medium mb-1">Institution Name</label>
                <input
                  type="text"
                  value={issuerName}
                  onChange={(e) => setIssuerName(e.target.value)}
                  placeholder="Enter institution name"
                  className="p-3 border border-gray-500 rounded-lg bg-gray-900 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-400"
                />
              </div>

              {/* Metadata field */}
              <div className="flex flex-col">
                <label className="text-gray-300 text-sm font-medium mb-1">Metadata</label>
                <input
                  type="text"
                  value={metadata}
                  onChange={(e) => setMetadata(e.target.value)}
                  placeholder="Enter your metadata"
                  className="p-3 border border-gray-500 rounded-lg bg-gray-900 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-400"
                />
              </div>
            </div>
            <div className="flex justify-center mt-3">
            <button
              onClick={handleIssueCredential}
              className="bg-teal-500 hover:bg-teal-600 text-white font-medium py-3 px-6 rounded-lg transition-colors mt-6"
            >
              Issue Credential
            </button>
            </div>
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
