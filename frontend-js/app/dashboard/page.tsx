"use client"

import { useState, useEffect } from "react"
import { getPasswords, addPassword, updatePassword, deletePassword } from "@/lib/api"
import AuthCheck from "@/components/auth-check"
import Navbar from "@/components/navbar"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { Plus, Edit, Trash2, Copy, Eye, EyeOff, Search, RefreshCw } from "lucide-react"
import { toast } from "@/components/ui/use-toast"
import { Toaster } from "@/components/ui/toaster"

interface Password {
  id: number
  name: string
  password: string
  shared: boolean
  created_at?: string
}

export default function Dashboard() {
  const [passwords, setPasswords] = useState<Password[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [searchTerm, setSearchTerm] = useState("")
  const [showPassword, setShowPassword] = useState<Record<number, boolean>>({})

  // Add password state
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false)
  const [newPasswordName, setNewPasswordName] = useState("")
  const [newPasswordValue, setNewPasswordValue] = useState("")
  const [newPasswordShared, setNewPasswordShared] = useState(false)

  // Edit password state
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [editPasswordId, setEditPasswordId] = useState<number | null>(null)
  const [editPasswordName, setEditPasswordName] = useState("")
  const [editPasswordValue, setEditPasswordValue] = useState("")
  const [editPasswordShared, setEditPasswordShared] = useState(false)

  const fetchPasswords = async () => {
    setLoading(true)
    try {
      const data = await getPasswords()
      setPasswords(data || [])
      setError("")
    } catch (error) {
      console.error("Error fetching passwords:", error)
      setError("Failed to load passwords. Please try again.")
      setPasswords([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchPasswords()
  }, [])

  const handleAddPassword = async () => {
    try {
      if (!newPasswordName || !newPasswordValue) {
        toast({
          title: "Error",
          description: "Please fill in all fields",
          variant: "destructive",
        })
        return
      }

      await addPassword(newPasswordValue, newPasswordName, newPasswordShared ? "true" : "false")
      setIsAddDialogOpen(false)
      setNewPasswordName("")
      setNewPasswordValue("")
      setNewPasswordShared(false)
      fetchPasswords()
      toast({
        title: "Success",
        description: "Password added successfully",
      })
    } catch (error) {
      console.error("Error adding password:", error)
      toast({
        title: "Error",
        description: "Failed to add password",
        variant: "destructive",
      })
    }
  }

  const handleEditPassword = async () => {
    try {
      if (!editPasswordId || !editPasswordName || !editPasswordValue) {
        toast({
          title: "Error",
          description: "Please fill in all fields",
          variant: "destructive",
        })
        return
      }

      await updatePassword(editPasswordId, editPasswordValue, editPasswordName, editPasswordShared ? "true" : "false")
      setIsEditDialogOpen(false)
      fetchPasswords()
      toast({
        title: "Success",
        description: "Password updated successfully",
      })
    } catch (error) {
      console.error("Error updating password:", error)
      toast({
        title: "Error",
        description: "Failed to update password",
        variant: "destructive",
      })
    }
  }

  const handleDeletePassword = async (id: number) => {
    if (confirm("Are you sure you want to delete this password?")) {
      try {
        await deletePassword(id)
        fetchPasswords()
        toast({
          title: "Success",
          description: "Password deleted successfully",
        })
      } catch (error) {
        console.error("Error deleting password:", error)
        toast({
          title: "Error",
          description: "Failed to delete password",
          variant: "destructive",
        })
      }
    }
  }

  const openEditDialog = (password: Password) => {
    setEditPasswordId(password.id)
    setEditPasswordName(password.name)
    setEditPasswordValue(password.password)
    setEditPasswordShared(password.shared)
    setIsEditDialogOpen(true)
  }

  const togglePasswordVisibility = (id: number) => {
    setShowPassword((prev) => ({
      ...prev,
      [id]: !prev[id],
    }))
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    toast({
      title: "Copied",
      description: "Password copied to clipboard",
    })
  }

  const filteredPasswords = passwords.filter((password) =>
    password.name.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  return (
    <AuthCheck>
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
        <Navbar />
        <main className="container mx-auto py-6 px-4">
          <div className="flex flex-col md:flex-row justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-purple-dark dark:text-purple-light mb-4 md:mb-0">
              Private Passwords
            </h1>
            <div className="flex flex-col sm:flex-row gap-4 w-full md:w-auto">
              <div className="relative w-full sm:w-64">
                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search passwords..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Button onClick={() => fetchPasswords()} variant="outline" className="flex items-center gap-2">
                <RefreshCw className="h-4 w-4" />
                Refresh
              </Button>
              <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
                <DialogTrigger asChild>
                  <Button className="bg-gradient-to-r from-pink-light to-purple hover:from-pink hover:to-purple-dark transition-all duration-300">
                    <Plus className="mr-2 h-4 w-4" /> Add Password
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Add New Password</DialogTitle>
                    <DialogDescription>Enter the details for your new password.</DialogDescription>
                  </DialogHeader>
                  <div className="space-y-4 py-4">
                    <div className="space-y-2">
                      <Label htmlFor="name">Name</Label>
                      <Input
                        id="name"
                        placeholder="e.g., Gmail, Facebook"
                        value={newPasswordName}
                        onChange={(e) => setNewPasswordName(e.target.value)}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="password">Password</Label>
                      <Input
                        id="password"
                        type="password"
                        placeholder="Enter password"
                        value={newPasswordValue}
                        onChange={(e) => setNewPasswordValue(e.target.value)}
                      />
                    </div>
                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="shared"
                        checked={newPasswordShared}
                        onCheckedChange={(checked) => setNewPasswordShared(checked === true)}
                      />
                      <Label htmlFor="shared">Shared password</Label>
                    </div>
                  </div>
                  <DialogFooter>
                    <Button variant="outline" onClick={() => setIsAddDialogOpen(false)}>
                      Cancel
                    </Button>
                    <Button onClick={handleAddPassword}>Save Password</Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            </div>
          </div>

          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple"></div>
            </div>
          ) : error ? (
            <div className="text-center text-destructive p-4 bg-destructive/10 rounded-md">{error}</div>
          ) : filteredPasswords.length === 0 ? (
            <div className="text-center p-8 bg-muted rounded-lg">
              <p className="text-lg text-muted-foreground">
                {searchTerm ? "No passwords match your search" : "No passwords found. Add your first password!"}
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredPasswords.map((password) => (
                <Card
                  key={password.id}
                  className="overflow-hidden border-2 border-purple-light/20 hover:shadow-md transition-shadow"
                >
                  <CardHeader className="bg-gradient-to-r from-purple-light/10 to-blue-light/10 pb-2">
                    <CardTitle className="text-xl text-purple-dark dark:text-purple-light">{password.name}</CardTitle>
                    {password.created_at && (
                      <CardDescription>Created: {new Date(password.created_at).toLocaleDateString()}</CardDescription>
                    )}
                  </CardHeader>
                  <CardContent className="pt-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex-1 relative">
                        <Input
                          type={showPassword[password.id] ? "text" : "password"}
                          value={password.password}
                          readOnly
                          className="pr-20"
                        />
                        <div className="absolute right-2 top-1/2 transform -translate-y-1/2 flex">
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => togglePasswordVisibility(password.id)}
                            className="h-8 w-8"
                          >
                            {showPassword[password.id] ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                          </Button>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => copyToClipboard(password.password)}
                            className="h-8 w-8"
                          >
                            <Copy className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </div>
                    {password.shared && (
                      <div className="mt-2">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100">
                          Shared
                        </span>
                      </div>
                    )}
                  </CardContent>
                  <CardFooter className="flex justify-between pt-0">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => openEditDialog(password)}
                      className="text-blue hover:text-blue-dark hover:border-blue"
                    >
                      <Edit className="mr-2 h-4 w-4" /> Edit
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDeletePassword(password.id)}
                      className="text-destructive hover:text-destructive-foreground hover:bg-destructive"
                    >
                      <Trash2 className="mr-2 h-4 w-4" /> Delete
                    </Button>
                  </CardFooter>
                </Card>
              ))}
            </div>
          )}
        </main>

        {/* Edit Password Dialog */}
        <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Edit Password</DialogTitle>
              <DialogDescription>Update your password details.</DialogDescription>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label htmlFor="edit-name">Name</Label>
                <Input
                  id="edit-name"
                  placeholder="e.g., Gmail, Facebook"
                  value={editPasswordName}
                  onChange={(e) => setEditPasswordName(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit-password">Password</Label>
                <Input
                  id="edit-password"
                  type="text"
                  placeholder="Enter password"
                  value={editPasswordValue}
                  onChange={(e) => setEditPasswordValue(e.target.value)}
                />
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="edit-shared"
                  checked={editPasswordShared}
                  onCheckedChange={(checked) => setEditPasswordShared(checked === true)}
                />
                <Label htmlFor="edit-shared">Shared password</Label>
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsEditDialogOpen(false)}>
                Cancel
              </Button>
              <Button onClick={handleEditPassword}>Update Password</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
        <Toaster />
      </div>
    </AuthCheck>
  )
}
