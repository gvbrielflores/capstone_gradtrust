import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-background text-foreground p-4">
      <nav className="flex justify-between items-center mb-8">
        <div className="text-xl font-bold">Amane Soft</div>
        <div className="space-x-4">
          <Link href="#" className="hover:text-primary">Solutions</Link>
          <Link href="#" className="hover:text-primary">Industries</Link>
          <Link href="#" className="hover:text-primary">About Us</Link>
          <Link href="#" className="hover:text-primary">GitHub</Link>
          <Link href="#" className="hover:text-primary">Contact</Link>
          <Link href="#" className="bg-primary text-white px-4 py-2 rounded">Get a Demo</Link>
        </div>
      </nav>

      <section className="mb-12">
        <h1 className="text-4xl font-bold mb-4">Innovate Faster with Amane Soft</h1>
        <p className="mb-4">Empowering businesses with cutting-edge software solutions. From AI-driven analytics to seamless cloud integrations, we're shaping the future of technology.</p>
        <div className="space-x-4">
          <Link href="#" className="bg-primary text-white px-6 py-2 rounded">Explore Solutions</Link>
          <Link href="#" className="border border-primary text-primary px-6 py-2 rounded">Schedule a Demo</Link>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-4">Cutting-Edge Solutions</h2>
        <p>Discover how Amane Soft can transform your business with our innovative technologies.</p>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-4">AI-Powered Analytics</h2>
        <p>Harness the power of machine learning to derive actionable insights from your data.</p>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-4">Cloud-Native Architecture</h2>
        <p>Scalable, resilient, and efficient solutions built for the modern cloud ecosystem.</p>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-4">Enterprise-Grade Security</h2>
        <p>State-of-the-art security measures to protect your most valuable assets.</p>
      </section>

      <section>
        <h2 className="text-2xl font-bold mb-4">High-Performance Systems</h2>
        <p>Optimized for speed and efficiency, our solutions deliver unparalleled performance.</p>
      </section>
    </main>
  )
}