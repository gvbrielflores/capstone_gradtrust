import { Button } from "@/components/ui/button"
import { ArrowRight } from "lucide-react"

export default function Hero() {
  return (
    <section className="container flex min-h-[calc(100vh-4rem)] max-w-screen-2xl flex-col items-center justify-center space-y-8 py-24 text-center md:py-32">
      <div className="space-y-6">
        <h1 className="bg-gradient-to-br from-white from-30% via-white/90 to-white/70 bg-clip-text text-4xl font-bold tracking-tight text-transparent sm:text-5xl md:text-6xl lg:text-7xl">
          Innovate Faster with
          <br />
          Amane Soft
        </h1>
        <p className="mx-auto max-w-[42rem] leading-normal text-muted-foreground sm:text-xl sm:leading-8">
          Empowering businesses with cutting-edge software solutions. From AI-driven analytics to seamless cloud
          integrations, we're shaping the future of technology.
        </p>
      </div>
      <div className="flex flex-col sm:flex-row gap-4 mt-6">
        <Button size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90">
          Explore Solutions
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
        <Button variant="outline" size="lg" className="border-primary/20 hover:bg-primary/10">
          Schedule a Demo
        </Button>
      </div>
    </section>
  )
}

