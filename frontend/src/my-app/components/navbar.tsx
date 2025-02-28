import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Github } from "lucide-react"

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 max-w-screen-2xl items-center">
        <Link href="/" className="mr-6 flex items-center space-x-2">
          <span className="text-xl font-bold">GradTrust</span>
        </Link>
        <nav className="hidden md:flex flex-1 items-center space-x-6 text-sm font-medium">
          <Link href="/solutions" className="transition-colors hover:text-primary">
            About Us
          </Link>
          <Link href="/industries" className="transition-colors hover:text-primary">
            Temporary
          </Link>
          <Link href="/about" className="transition-colors hover:text-primary">
            Really Temporary
          </Link>
        </nav>
        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="sm" className="hidden md:flex">
            Contact
          </Button>
          <Button size="sm">Get a Demo</Button>
        </div>
      </div>
    </header>
  )
}

