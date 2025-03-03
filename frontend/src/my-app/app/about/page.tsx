"use client"

import Link from "next/link"
import Image from "next/image"
// import { MovingBorder } from "@/components/ui/moving-border"

export default function AboutPage() {
  return (
    <main className="flex min-h-screen flex-col items-center p-8 md:p-24 bg-[#6d717f] text-white">
      {/* Navigation */}
      <nav className="w-full max-w-7xl flex justify-between items-center mb-16">
        <Link href="/" className="text-2xl font-bold">
          Streamline
        </Link>
        <div className="flex gap-8">
          <Link href="/" className="hover:text-teal-300 transition-colors">
            Home
          </Link>
          <Link href="/about" className="text-teal-300 font-medium">
            About Us
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="w-full max-w-7xl mb-16">
        <h1 className="text-4xl md:text-6xl font-bold mb-6">About Our Company</h1>
        <p className="text-xl text-gray-200 max-w-3xl">
          We're on a mission to streamline workflows and empower teams with intuitive solutions.
        </p>
      </div>

      {/* Our Story */}
      <section className="w-full max-w-7xl mb-20">
        <h2 className="text-3xl font-bold mb-8 border-b border-teal-400 pb-2 inline-block">Our Story</h2>
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <p className="text-lg mb-4">
              Founded in 2020, Streamline began with a simple idea: make complex workflows simple. Our founders
              recognized that teams were spending too much time on process and not enough on innovation.
            </p>
            <p className="text-lg mb-4">
              What started as a small project has grown into a comprehensive platform used by thousands of teams
              worldwide. We're proud of our journey and excited about the future.
            </p>
            <p className="text-lg">
              Today, we're a team of 30+ passionate individuals dedicated to creating tools that help teams work better
              together.
            </p>
          </div>
          <div className="relative h-80 w-full rounded-xl overflow-hidden">
            <Image
              src="/placeholder.svg?height=600&width=800"
              alt="Our team collaborating"
              fill
              className="object-cover"
            />
          </div>
        </div>
      </section>

      {/* Our Values */}
      <section className="w-full max-w-7xl mb-20">
        <h2 className="text-3xl font-bold mb-8 border-b border-teal-400 pb-2 inline-block">Our Values</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {/* <MovingBorder className="p-6" borderClassName="bg-gradient-to-r from-teal-400 to-emerald-400"> */}
            <div className="p-4">
              <h3 className="text-xl font-bold mb-3">Simplicity</h3>
              <p className="text-gray-200">
                We believe in making the complex simple. Our solutions are intuitive and easy to use.
              </p>
            </div>
          {/* </MovingBorder> */}

          {/* <MovingBorder className="p-6" borderClassName="bg-gradient-to-r from-teal-400 to-emerald-400"> */}
            <div className="p-4">
              <h3 className="text-xl font-bold mb-3">Innovation</h3>
              <p className="text-gray-200">
                We're constantly exploring new ideas and technologies to improve our platform.
              </p>
            </div>
          {/* </MovingBorder> */}

          {/* <MovingBorder className="p-6" borderClassName="bg-gradient-to-r from-teal-400 to-emerald-400"> */}
            <div className="p-4">
              <h3 className="text-xl font-bold mb-3">Collaboration</h3>
              <p className="text-gray-200">We believe in the power of teams working together seamlessly.</p>
            </div>
          {/* </MovingBorder> */}
        </div>
      </section>

      {/* Team Section */}
      <section className="w-full max-w-7xl mb-20">
        <h2 className="text-3xl font-bold mb-8 border-b border-teal-400 pb-2 inline-block">Our Team</h2>
        <div className="grid md:grid-cols-4 gap-8">
          {[1, 2, 3, 4].map((member) => (
            <div
              key={member}
              className="bg-slate-800/40 rounded-xl overflow-hidden hover:transform hover:scale-105 transition-transform duration-300"
            >
              <div className="relative h-64 w-full">
                <Image
                  src={`/placeholder.svg?height=400&width=300&text=Team Member ${member}`}
                  alt={`Team member ${member}`}
                  fill
                  className="object-cover"
                />
              </div>
              <div className="p-4">
                <h3 className="text-lg font-bold">Team Member {member}</h3>
                <p className="text-gray-300">Co-Founder & CEO</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Contact Section */}
      <section className="w-full max-w-7xl mb-12">
        <h2 className="text-3xl font-bold mb-8 border-b border-teal-400 pb-2 inline-block">Get In Touch</h2>
        <div className="bg-slate-800/30 p-8 rounded-xl">
          <p className="text-lg mb-6">
            We'd love to hear from you! Whether you have questions about our products, need support, or are interested
            in joining our team, reach out to us.
          </p>
          <div className="flex flex-col md:flex-row gap-4">
            <a
              href="mailto:contact@streamline.com"
              className="bg-teal-500 hover:bg-teal-600 text-white font-medium py-3 px-6 rounded-lg transition-colors text-center"
            >
              Email Us
            </a>
            <a
              href="#"
              className="bg-slate-700 hover:bg-slate-600 text-white font-medium py-3 px-6 rounded-lg transition-colors text-center"
            >
              Schedule a Call
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="w-full max-w-7xl pt-8 border-t border-slate-600 mt-auto">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-300">© 2023 Streamline. All rights reserved.</p>
          <div className="flex gap-6 mt-4 md:mt-0">
            <a href="#" className="text-gray-300 hover:text-teal-300 transition-colors">
              Twitter
            </a>
            <a href="#" className="text-gray-300 hover:text-teal-300 transition-colors">
              LinkedIn
            </a>
            <a href="#" className="text-gray-300 hover:text-teal-300 transition-colors">
              GitHub
            </a>
          </div>
        </div>
      </footer>
    </main>
  )
}

