"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"
import {
  getGroup,
  getGroupRequests,
  addPasswordToGroup,
  updatePasswordInGroup,
  deletePasswordFromGroup,
  approveRequest,
  declineRequest,
  acceptUser,
  removeUser,
  insertRequest,
  leaveGroup,
  removeGroup,
} from "@/lib/api"
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Label } from "@/components/ui/label"
import {
  Plus,
  Edit,
  Trash2,
  Copy,
  Eye,
  EyeOff,
  UserMinus,
  CheckCircle,
  XCircle,
  AlertCircle,
  LogOut,
  RefreshCw,
} from "lucide-react"
import { toast } from "@/components/ui/use-toast"
import { Toaster } from "@/components/ui/toaster"

interface Password {
  id: number
  name: string
  password: string
  shared: boolean
  created_at?: string
}

interface User {
  id: number
  username: string
  role: string
}

interface Request {
  id: number
  username: string
  command: string
  timestamp: string
}

interface GroupDetails {
  name: string
  description: string
  created_at?: string
  role?: string
  users: User[]
  passwords: Password[]
}

export default function GroupPage() {
  const params = useParams()
  const groupName = decodeURIComponent(params.groupName as string)

  const [groupDetails, setGroupDetails] = useState<GroupDetails | null>(null)
  const [requests, setRequests] = useState<Request[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [showPassword, setShowPassword] = useState<Record<number, boolean>>({})

  // Add password state
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false)
  const [newPasswordName, setNewPasswordName] = useState("")
  const [newPasswordValue, setNewPasswordValue] = useState("")

  // Edit password state
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [editPasswordId, setEditPasswordId] = useState<number | null>(null)
  const [editPasswordName, setEditPasswordName] = useState("")
  const [editPasswordValue, setEditPasswordValue] = useState("")

  // Request state
  const [isRequestDialogOpen, setIsRequestDialogOpen] = useState(false)
  const [requestCommand, setRequestCommand] = useState("")

  const isAdmin = groupDetails?.role === "admin"
  const isMember = groupDetails?.role === "member" || isAdmin

  const fetchGroupData = async () => {
    setLoading(true)
    try {
      const data = await getGroup(groupName)
      setGroupDetails(data)
      setError("")

      // If user is admin, fetch requests
      if (data.role === "admin") {
        const requestsData = await getGroupRequests(groupName)
        setRequests(requestsData || [])
      }
    } catch (error) {
      console.error("Error fetching group details:", error)
      setError("Failed to load group details. Please try again.")
      setGroupDetails(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (groupName) {
      fetchGroupData()
    }
  }, [groupName])

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

      if (isAdmin) {
        await addPasswordToGroup(groupName, newPasswordValue, newPasswordName)
        toast({
          title: "Success",
          description: "Password added successfully",
        })
      } else {
        await insertRequest(groupName, `Add password: ${newPasswordName}`)
        toast({
          title: "Success",
          description: "Password add request sent to admin",
        })
      }

      setIsAddDialogOpen(false)
      setNewPasswordName("")
      setNewPasswordValue("")
      fetchGroupData()
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

      if (isAdmin) {
        await updatePasswordInGroup(groupName, editPasswordId, editPasswordValue, editPasswordName)
        toast({
          title: "Success",
          description: "Password updated successfully",
        })
      } else {
        await insertRequest(groupName, `Update password: ${editPasswordName} (ID: ${editPasswordId})`)
        toast({
          title: "Success",
          description: "Password update request sent to admin",
        })
      }

      setIsEditDialogOpen(false)
      fetchGroupData()
    } catch (error) {
      console.error("Error updating password:", error)
      toast({
        title: "Error",
        description: "Failed to update password",
        variant: "destructive",
      })
    }
  }

  const handleDeletePassword = async (id: number, name: string) => {
    if (confirm("Are you sure you want to delete this password?")) {
      try {
        if (isAdmin) {
          await deletePasswordFromGroup(groupName, id)
          toast({
            title: "Success",
            description: "Password deleted successfully",
          })
        } else {
          await insertRequest(groupName, `Delete password: ${name} (ID: ${id})`)
          toast({
            title: "Success",
            description: "Password delete request sent to admin",
          })
        }
        fetchGroupData()
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

  const handleApproveRequest = async (requestId: number) => {
    try {
      await approveRequest(groupName, requestId)
      toast({
        title: "Success",
        description: "Request approved successfully",
      })
      fetchGroupData()
    } catch (error) {
      console.error("Error approving request:", error)
      toast({
        title: "Error",
        description: "Failed to approve request",
        variant: "destructive",
      })
    }
  }

  const handleDeclineRequest = async (requestId: number) => {
    try {
      await declineRequest(groupName, requestId)
      toast({
        title: "Success",
        description: "Request declined successfully",
      })
      fetchGroupData()
    } catch (error) {
      console.error("Error declining request:", error)
      toast({
        title: "Error",
        description: "Failed to decline request",
        variant: "destructive",
      })
    }
  }

  const handleAcceptUser = async (username: string) => {
    try {
      await acceptUser(groupName, username)
      toast({
        title: "Success",
        description: "User accepted successfully",
      })
      fetchGroupData()
    } catch (error) {
      console.error("Error accepting user:", error)
      toast({
        title: "Error",
        description: "Failed to accept user",
        variant: "destructive",
      })
    }
  }

  const handleRemoveUser = async (username: string) => {
    if (confirm(`Are you sure you want to remove ${username} from the group?`)) {
      try {
        await removeUser(groupName, username)
        toast({
          title: "Success",
          description: "User removed successfully",
        })
        fetchGroupData()
      } catch (error) {
        console.error("Error removing user:", error)
        toast({
          title: "Error",
          description: "Failed to remove user",
          variant: "destructive",
        })
      }
    }
  }

  const handleLeaveGroup = async () => {
    if (confirm("Are you sure you want to leave this group?")) {
      try {
        await leaveGroup(groupName)
        toast({
          title: "Success",
          description: "You have left the group",
        })
        window.location.href = "/groups"
      } catch (error) {
        console.error("Error leaving group:", error)
        toast({
          title: "Error",
          description: "Failed to leave group",
          variant: "destructive",
        })
      }
    }
  }

  const handleDeleteGroup = async () => {
    if (confirm("Are you sure you want to delete this group? This action cannot be undone.")) {
      try {
        await removeGroup(groupName)
        toast({
          title: "Success",
          description: "Group deleted successfully",
        })
        window.location.href = "/groups"
      } catch (error) {
        console.error("Error deleting group:", error)
        toast({
          title: "Error",
          description: "Failed to delete group",
          variant: "destructive",
        })
      }
    }
  }

  const handleSendRequest = async () => {
    try {
      if (!requestCommand) {
        toast({
          title: "Error",
          description: "Please enter a request",
          variant: "destructive",
        })
        return
      }

      await insertRequest(groupName, requestCommand)
      setIsRequestDialogOpen(false)
      setRequestCommand("")
      toast({
        title: "Success",
        description: "Request sent successfully",
      })
    } catch (error) {
      console.error("Error sending request:", error)
      toast({
        title: "Error",
        description: "Failed to send request",
        variant: "destructive",
      })
    }
  }

  const openEditDialog = (password: Password) => {
    setEditPasswordId(password.id)
    setEditPasswordName(password.name)
    setEditPasswordValue(password.password)
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

  return (
    <AuthCheck>
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50 dark:from-gray-900 dark:to-gray-800">
        <Navbar />
        <main className="container mx-auto py-6 px-4">
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple"></div>
            </div>
          ) : error ? (
            <div className="text-center text-destructive p-4 bg-destructive/10 rounded-md">{error}</div>
          ) : groupDetails ? (
            <>
              <div className="flex flex-col md:flex-row justify-between items-start mb-6">
                <div>
                  <h1 className="text-3xl font-bold text-purple-dark dark:text-purple-light mb-2">
                    {groupDetails.name}
                  </h1>
                  <p className="text-muted-foreground mb-4">{groupDetails.description}</p>
                  {groupDetails.role && (
                    <div className="mb-4">
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-100">
                        Your role: {groupDetails.role}
                      </span>
                    </div>
                  )}
                </div>
                <div className="flex flex-wrap gap-2 mt-4 md:mt-0">
                  <Button onClick={fetchGroupData} variant="outline" className="flex items-center gap-2">
                    <RefreshCw className="h-4 w-4" />
                    Refresh
                  </Button>
                  {!isAdmin && isMember && (
                    <Dialog open={isRequestDialogOpen} onOpenChange={setIsRequestDialogOpen}>
                      <DialogTrigger asChild>
                        <Button variant="outline" className="flex items-center gap-2">
                          <AlertCircle className="h-4 w-4" />
                          Send Request
                        </Button>
                      </DialogTrigger>
                      <DialogContent>
                        <DialogHeader>
                          <DialogTitle>Send Request to Admin</DialogTitle>
                          <DialogDescription>Describe your request for the group admin.</DialogDescription>
                        </DialogHeader>
                        <div className="space-y-4 py-4">
                          <div className="space-y-2">
                            <Label htmlFor="request-command">Request</Label>
                            <Input
                              id="request-command"
                              placeholder="e.g., Please add me as admin"
                              value={requestCommand}
                              onChange={(e) => setRequestCommand(e.target.value)}
                            />
                          </div>
                        </div>
                        <DialogFooter>
                          <Button variant="outline" onClick={() => setIsRequestDialogOpen(false)}>
                            Cancel
                          </Button>
                          <Button onClick={handleSendRequest}>Send Request</Button>
                        </DialogFooter>
                      </DialogContent>
                    </Dialog>
                  )}
                  {isMember && (
                    <Button
                      variant="outline"
                      className="flex items-center gap-2 text-destructive hover:bg-destructive hover:text-destructive-foreground"
                      onClick={handleLeaveGroup}
                    >
                      <LogOut className="h-4 w-4" />
                      Leave Group
                    </Button>
                  )}
                  {isAdmin && (
                    <Button variant="destructive" className="flex items-center gap-2" onClick={handleDeleteGroup}>
                      <Trash2 className="h-4 w-4" />
                      Delete Group
                    </Button>
                  )}
                </div>
              </div>

              <Tabs defaultValue="passwords" className="w-full">
                <TabsList className="grid w-full grid-cols-3">
                  <TabsTrigger value="passwords">Passwords</TabsTrigger>
                  <TabsTrigger value="members">Members</TabsTrigger>
                  {isAdmin && <TabsTrigger value="requests">Requests</TabsTrigger>}
                </TabsList>

                <TabsContent value="passwords" className="mt-6">
                  <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-semibold text-purple-dark dark:text-purple-light">Group Passwords</h2>
                    <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
                      <DialogTrigger asChild>
                        <Button className="bg-gradient-to-r from-pink-light to-purple hover:from-pink hover:to-purple-dark transition-all duration-300">
                          <Plus className="mr-2 h-4 w-4" /> Add Password
                        </Button>
                      </DialogTrigger>
                      <DialogContent>
                        <DialogHeader>
                          <DialogTitle>Add New Password</DialogTitle>
                          <DialogDescription>
                            {isAdmin
                              ? "Enter the details for the new password."
                              : "Your request will be sent to the group admin for approval."}
                          </DialogDescription>
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
                        </div>
                        <DialogFooter>
                          <Button variant="outline" onClick={() => setIsAddDialogOpen(false)}>
                            Cancel
                          </Button>
                          <Button onClick={handleAddPassword}>{isAdmin ? "Save Password" : "Send Request"}</Button>
                        </DialogFooter>
                      </DialogContent>
                    </Dialog>
                  </div>

                  {groupDetails.passwords.length === 0 ? (
                    <div className="text-center p-8 bg-muted rounded-lg">
                      <p className="text-lg text-muted-foreground">No passwords found in this group.</p>
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {groupDetails.passwords.map((password) => (
                        <Card
                          key={password.id}
                          className="overflow-hidden border-2 border-purple-light/20 hover:shadow-md transition-shadow"
                        >
                          <CardHeader className="bg-gradient-to-r from-purple-light/10 to-pink-light/10 pb-2">
                            <CardTitle className="text-xl text-purple-dark dark:text-purple-light">
                              {password.name}
                            </CardTitle>
                            {password.created_at && (
                              <CardDescription>
                                Created: {new Date(password.created_at).toLocaleDateString()}
                              </CardDescription>
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
                                    {showPassword[password.id] ? (
                                      <EyeOff className="h-4 w-4" />
                                    ) : (
                                      <Eye className="h-4 w-4" />
                                    )}
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
                              onClick={() => handleDeletePassword(password.id, password.name)}
                              className="text-destructive hover:text-destructive-foreground hover:bg-destructive"
                            >
                              <Trash2 className="mr-2 h-4 w-4" /> Delete
                            </Button>
                          </CardFooter>
                        </Card>
                      ))}
                    </div>
                  )}
                </TabsContent>

                <TabsContent value="members" className="mt-6">
                  <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-semibold text-purple-dark dark:text-purple-light">Group Members</h2>
                  </div>

                  {groupDetails.users.length === 0 ? (
                    <div className="text-center p-8 bg-muted rounded-lg">
                      <p className="text-lg text-muted-foreground">No members found in this group.</p>
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {groupDetails.users.map((user) => (
                        <Card
                          key={user.id}
                          className="overflow-hidden border-2 border-blue-light/20 hover:shadow-md transition-shadow"
                        >
                          <CardHeader className="bg-gradient-to-r from-blue-light/10 to-green-light/10 pb-2">
                            <CardTitle className="text-xl text-blue-dark dark:text-blue-light">
                              {user.username}
                            </CardTitle>
                            <CardDescription>Role: {user.role}</CardDescription>
                          </CardHeader>
                          {isAdmin && user.role !== "admin" && (
                            <CardFooter className="pt-4">
                              <Button
                                variant="destructive"
                                size="sm"
                                onClick={() => handleRemoveUser(user.username)}
                                className="w-full"
                              >
                                <UserMinus className="mr-2 h-4 w-4" /> Remove User
                              </Button>
                            </CardFooter>
                          )}
                        </Card>
                      ))}
                    </div>
                  )}
                </TabsContent>

                {isAdmin && (
                  <TabsContent value="requests" className="mt-6">
                    <div className="flex justify-between items-center mb-6">
                      <h2 className="text-2xl font-semibold text-purple-dark dark:text-purple-light">
                        Pending Requests
                      </h2>
                    </div>

                    {requests.length === 0 ? (
                      <div className="text-center p-8 bg-muted rounded-lg">
                        <p className="text-lg text-muted-foreground">No pending requests.</p>
                      </div>
                    ) : (
                      <div className="space-y-4">
                        {requests.map((request) => (
                          <Card
                            key={request.id}
                            className="overflow-hidden border-2 border-green-light/20 hover:shadow-md transition-shadow"
                          >
                            <CardHeader className="bg-gradient-to-r from-green-light/10 to-blue-light/10 pb-2">
                              <div className="flex justify-between">
                                <CardTitle className="text-xl text-green-dark dark:text-green-light">
                                  Request from {request.username}
                                </CardTitle>
                                <CardDescription>{new Date(request.timestamp).toLocaleString()}</CardDescription>
                              </div>
                            </CardHeader>
                            <CardContent className="pt-4">
                              <p className="text-foreground mb-4">{request.command}</p>
                            </CardContent>
                            <CardFooter className="flex justify-between pt-0">
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleApproveRequest(request.id)}
                                className="text-green hover:text-green-foreground hover:bg-green"
                              >
                                <CheckCircle className="mr-2 h-4 w-4" /> Approve
                              </Button>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleDeclineRequest(request.id)}
                                className="text-destructive hover:text-destructive-foreground hover:bg-destructive"
                              >
                                <XCircle className="mr-2 h-4 w-4" /> Decline
                              </Button>
                            </CardFooter>
                          </Card>
                        ))}
                      </div>
                    )}
                  </TabsContent>
                )}
              </Tabs>
            </>
          ) : (
            <div className="text-center p-8 bg-muted rounded-lg">
              <p className="text-lg text-muted-foreground">Group not found or you don't have access.</p>
            </div>
          )}
        </main>

        {/* Edit Password Dialog */}
        <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Edit Password</DialogTitle>
              <DialogDescription>
                {isAdmin
                  ? "Update the password details."
                  : "Your request will be sent to the group admin for approval."}
              </DialogDescription>
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
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsEditDialogOpen(false)}>
                Cancel
              </Button>
              <Button onClick={handleEditPassword}>{isAdmin ? "Update Password" : "Send Request"}</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
        <Toaster />
      </div>
    </AuthCheck>
  )
}
