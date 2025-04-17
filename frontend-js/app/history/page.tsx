"use client"

import { useState, useEffect } from "react"
import { getHistory } from "@/lib/api"
import AuthCheck from "@/components/auth-check"
import Navbar from "@/components/navbar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Search, Clock, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"

interface HistoryItem {
  id: number
  action: string
  timestamp: string
  details?: string
}

export default function HistoryPage() {
  const [history, setHistory] = useState<HistoryItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [searchTerm, setSearchTerm] = useState("")

  const fetchHistory = async () => {
    setLoading(true)
    try {
      const data = await getHistory()
      setHistory(data || [])
      setError("")
    } catch (error) {
      console.error("Error fetching history:", error)
      setError("Failed to load history. Please try again.")
      setHistory([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchHistory()
  }, [])

  const filteredHistory = history.filter(
    (item) =>
      item.action.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (item.details && item.details.toLowerCase().includes(searchTerm.toLowerCase())),
  )

  return (
    <AuthCheck>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50 dark:from-gray-900 dark:to-gray-800">
        <Navbar />
        <main className="container mx-auto py-6 px-4">
          <div className="flex flex-col md:flex-row justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-blue-dark dark:text-blue-light mb-4 md:mb-0">Password History</h1>
            <div className="flex flex-col sm:flex-row gap-4 w-full md:w-auto">
              <div className="relative w-full sm:w-64">
                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search history..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Button onClick={fetchHistory} variant="outline" className="flex items-center gap-2">
                <RefreshCw className="h-4 w-4" />
                Refresh
              </Button>
            </div>
          </div>

          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue"></div>
            </div>
          ) : error ? (
            <div className="text-center text-destructive p-4 bg-destructive/10 rounded-md">{error}</div>
          ) : filteredHistory.length === 0 ? (
            <div className="text-center p-8 bg-muted rounded-lg">
              <p className="text-lg text-muted-foreground">
                {searchTerm ? "No history items match your search" : "No history found."}
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredHistory.map((item) => (
                <Card key={item.id} className="border-2 border-blue-light/20 hover:shadow-md transition-shadow">
                  <CardHeader className="bg-gradient-to-r from-blue-light/10 to-green-light/10 pb-2">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg text-blue-dark dark:text-blue-light flex items-center">
                        <Clock className="mr-2 h-5 w-5" />
                        {item.action}
                      </CardTitle>
                      <CardDescription>{new Date(item.timestamp).toLocaleString()}</CardDescription>
                    </div>
                  </CardHeader>
                  {item.details && (
                    <CardContent className="pt-4">
                      <p className="text-muted-foreground">{item.details}</p>
                    </CardContent>
                  )}
                </Card>
              ))}
            </div>
          )}
        </main>
      </div>
    </AuthCheck>
  )
}
