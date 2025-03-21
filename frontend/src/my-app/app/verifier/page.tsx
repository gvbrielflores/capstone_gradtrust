"use client"

import { useState } from "react"
import Navbar from "@/components/navbar"
import Footer from "@/components/footer"

export default function AboutPage() {
  const [address, setAddress] = useState("")

  const handleSubmit = () => {
    console.log("Submitted Address:", address)
    // Add your submission logic here
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
          <section className="w-full max-w-lg bg-white/10 p-6 rounded-2xl shadow-md backdrop-blur-md text-center">
          <section className="w-full max-w-7xl mb-16 text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">Verifier</h1>
          </section>

          {/* Address Input Section */}
            <label htmlFor="address" className="block text-lg font-semibold mb-2">
              Enter Recipient Address
            </label>
            <input
              id="address"
              type="text"
              placeholder="Enter recipient address here..."
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              className="w-full p-3 rounded-lg bg-white/20 text-white placeholder-gray-300 outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={handleSubmit}
              className="bg-teal-500 hover:bg-teal-600 text-white font-medium py-3 px-6 rounded-lg transition-colors mt-6"
            >
              Submit
            </button>
          </section>
        </main>
        <Footer />
      </div>
    </div>
  )
}
// Once I sign in I need to get my address and then I will see the credentials 