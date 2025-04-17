"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { logout } from "@/lib/api"
import { Lock, History, Users, Menu, X, LogOut, Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false)
  const router = useRouter()
  const { theme, setTheme } = useTheme()

  const handleLogout = async () => {
    try {
      await logout()
      router.push("/auth")
    } catch (error) {
      console.error("Logout failed:", error)
    }
  }

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark")
  }

  return (
    <nav className="bg-gradient-to-r from-pink-light via-purple to-blue text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link href="/dashboard" className="flex items-center">
              <Lock className="h-8 w-8 mr-2" />
              <span className="text-xl font-bold">SecurePass</span>
            </Link>
          </div>

          <div className="hidden md:block">
            <div className="ml-10 flex items-center space-x-4">
              <Link
                href="/dashboard"
                className="px-3 py-2 rounded-md text-sm font-medium hover:bg-purple-dark transition-colors"
              >
                Passwords
              </Link>
              <Link
                href="/history"
                className="px-3 py-2 rounded-md text-sm font-medium hover:bg-purple-dark transition-colors"
              >
                History
              </Link>
              <Link
                href="/groups"
                className="px-3 py-2 rounded-md text-sm font-medium hover:bg-purple-dark transition-colors"
              >
                Groups
              </Link>
              <Button variant="ghost" size="icon" onClick={toggleTheme} className="text-white hover:bg-purple-dark">
                {theme === "dark" ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
              </Button>
              <Button
                variant="ghost"
                className="text-white hover:bg-purple-dark flex items-center"
                onClick={handleLogout}
              >
                <LogOut className="h-5 w-5 mr-1" />
                Logout
              </Button>
            </div>
          </div>

          <div className="md:hidden">
            <Button variant="ghost" size="icon" onClick={toggleTheme} className="text-white hover:bg-purple-dark mr-2">
              {theme === "dark" ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </Button>
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-white hover:bg-purple-dark focus:outline-none"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-purple-dark">
            <Link
              href="/dashboard"
              className="block px-3 py-2 rounded-md text-base font-medium text-white hover:bg-purple transition-colors"
              onClick={() => setIsOpen(false)}
            >
              <div className="flex items-center">
                <Lock className="h-5 w-5 mr-2" />
                Passwords
              </div>
            </Link>
            <Link
              href="/history"
              className="block px-3 py-2 rounded-md text-base font-medium text-white hover:bg-purple transition-colors"
              onClick={() => setIsOpen(false)}
            >
              <div className="flex items-center">
                <History className="h-5 w-5 mr-2" />
                History
              </div>
            </Link>
            <Link
              href="/groups"
              className="block px-3 py-2 rounded-md text-base font-medium text-white hover:bg-purple transition-colors"
              onClick={() => setIsOpen(false)}
            >
              <div className="flex items-center">
                <Users className="h-5 w-5 mr-2" />
                Groups
              </div>
            </Link>
            <button
              onClick={handleLogout}
              className="w-full text-left block px-3 py-2 rounded-md text-base font-medium text-white hover:bg-purple transition-colors"
            >
              <div className="flex items-center">
                <LogOut className="h-5 w-5 mr-2" />
                Logout
              </div>
            </button>
          </div>
        </div>
      )}
    </nav>
  )
}
