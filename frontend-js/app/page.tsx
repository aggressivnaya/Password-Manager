"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { isAuthenticated } from "@/lib/api"

export default function Home() {
  const router = useRouter()

  useEffect(() => {
    // Redirect to dashboard if authenticated, otherwise to login
    if (isAuthenticated()) {
      router.push("/dashboard")
    } else {
      router.push("/auth")
    }
  }, [router])

  return null
}
