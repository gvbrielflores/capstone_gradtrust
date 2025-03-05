"use client"

import { useState } from "react"
import Navbar from "@/components/navbar"
import Footer from "@/components/footer"

export default function IssuerPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0])
    }
  }

  const handleUpload = () => {
    if (selectedFile) {
      // Handle file upload here (e.g., send to API or cloud storage)
      alert(`Uploading ${selectedFile.name}`)
    }
  }

  return (
    <div className="relative min-h-screen">
      {/* Background gradients */}
      <div className="pointer-events-none fixed inset-0">
        <div className="absolute inset-0 bg-gradient-to-b from-background via-background/90 to-background" />
        <div className="absolute right-0 top-0 h-[500px] w-[500px] bg-blue-500/10 blur-[100px]" />
        <div className="absolute bottom-0 left-0 h-[500px] w-[500px] bg-purple-500/10 blur-[100px]" />
      </div>

      <div className="relative z-10">
        <Navbar />
        <main className="flex flex-col items-center p-8 md:p-24 text-white">
          {/* Hero Section */}
          <section className="w-full max-w-7xl mb-16 text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">Upload a Certificate</h1>
            <p className="text-lg text-gray-300 mb-6">
              Select a PDF file to upload.
            </p>

            {/* File Upload Input styled as a button */}
            <label className="cursor-pointer bg-teal-500 hover:bg-teal-600 text-white font-medium py-3 px-6 rounded-lg transition-colors text-center">
              <input
                type="file"
                accept="application/pdf"
                onChange={handleFileChange}
                className="hidden"
              />
              Choose File
            </label>

            {/* Display Selected File Name */}
            {selectedFile && (
              <p className="mt-4 text-gray-300">
                Selected: <span className="font-semibold">{selectedFile.name}</span>
              </p>
            )}

            {/* Upload Button (Visible only when a file is selected) */}
            {selectedFile && (
              <button
                onClick={handleUpload}
                className="bg-teal-500 hover:bg-teal-600 text-white font-medium py-3 px-6 rounded-lg transition-colors mt-6"
              >
                Upload
              </button>
            )}
          </section>
        </main>
        <Footer />
      </div>
    </div>
  )
}
