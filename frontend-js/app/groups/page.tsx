"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { getGroups, createGroup, enterGroup } from "@/lib/api"
import AuthCheck from "@/components/auth-check"
import Navbar from "@/components/navbar"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
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
import { Label } from "@/components/ui/label"
import { Plus, Users, Search, RefreshCw, UserPlus, ArrowRight } from "lucide-react"
import { toast } from "@/components/ui/use-toast"
import { Toaster } from "@/components/ui/toaster"

interface Group {
  id: number
  name: string
  description: string
  created_at?: string
  member_count?: number
  role?: string
}

export default function GroupsPage() {
  const [groups, setGroups] = useState<Group[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [searchTerm, setSearchTerm] = useState("")
  const router = useRouter()

  // Create group state
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [newGroupName, setNewGroupName] = useState("")
  const [newGroupDescription, setNewGroupDescription] = useState("")

  // Join group state
  const [isJoinDialogOpen, setIsJoinDialogOpen] = useState(false)
  const [joinGroupName, setJoinGroupName] = useState("")

  const fetchGroups = async () => {
    setLoading(true)
    try {
      const data = await getGroups()
      setGroups(data || [])
      setError("")
    } catch (error) {
      console.error("Error fetching groups:", error)
      setError("Failed to load groups. Please try again.")
      setGroups([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchGroups()
  }, [])

  const handleCreateGroup = async () => {
    try {
      if (!newGroupName) {
        toast({
          title: "Error",
          description: "Please enter a group name",
          variant: "destructive",
        })
        return
      }

      await createGroup(newGroupName, newGroupDescription)
      setIsCreateDialogOpen(false)
      setNewGroupName("")
      setNewGroupDescription("")
      fetchGroups()
      toast({
        title: "Success",
        description: "Group created successfully",
      })
    } catch (error) {
      console.error("Error creating group:", error)
      toast({
        title: "Error",
        description: "Failed to create group",
        variant: "destructive",
      })
    }
  }

  const handleJoinGroup = async () => {
    try {
      if (!joinGroupName) {
        toast({
          title: "Error",
          description: "Please enter a group name",
          variant: "destructive",
        })
        return
      }

      await enterGroup(joinGroupName)
      setIsJoinDialogOpen(false)
      setJoinGroupName("")
      fetchGroups()
      toast({
        title: "Success",
        description: "Join request sent successfully",
      })
    } catch (error) {
      console.error("Error joining group:", error)
      toast({
        title: "Error",
        description: "Failed to join group",
        variant: "destructive",
      })
    }
  }

  const navigateToGroup = (groupName: string) => {
    router.push(`/groups/${encodeURIComponent(groupName)}`)
  }

  const filteredGroups = groups.filter(
    (group) =>
      group.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      group.description.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  return (
    <AuthCheck>
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-purple-50 dark:from-gray-900 dark:to-gray-800">
        <Navbar />
        <main className="container mx-auto py-6 px-4">
          <div className="flex flex-col md:flex-row justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-green-dark dark:text-green-light mb-4 md:mb-0">Password Groups</h1>
            <div className="flex flex-col sm:flex-row gap-4 w-full md:w-auto">
              <div className="relative w-full sm:w-64">
                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search groups..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Button onClick={fetchGroups} variant="outline" className="flex items-center gap-2">
                <RefreshCw className="h-4 w-4" />
                Refresh
              </Button>
              <Dialog open={isJoinDialogOpen} onOpenChange={setIsJoinDialogOpen}>
                <DialogTrigger asChild>
                  <Button
                    variant="outline"
                    className="bg-gradient-to-r from-blue-light to-blue hover:from-blue hover:to-blue-dark transition-all duration-300"
                  >
                    <UserPlus className="mr-2 h-4 w-4" /> Join Group
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Join Existing Group</DialogTitle>
                    <DialogDescription>Enter the name of the group you want to join.</DialogDescription>
                  </DialogHeader>
                  <div className="space-y-4 py-4">
                    <div className="space-y-2">
                      <Label htmlFor="join-group-name">Group Name</Label>
                      <Input
                        id="join-group-name"
                        placeholder="Enter group name"
                        value={joinGroupName}
                        onChange={(e) => setJoinGroupName(e.target.value)}
                      />
                    </div>
                  </div>
                  <DialogFooter>
                    <Button variant="outline" onClick={() => setIsJoinDialogOpen(false)}>
                      Cancel
                    </Button>
                    <Button onClick={handleJoinGroup}>Send Join Request</Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
              <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
                <DialogTrigger asChild>
                  <Button className="bg-gradient-to-r from-green-light to-green hover:from-green hover:to-green-dark transition-all duration-300">
                    <Plus className="mr-2 h-4 w-4" /> Create Group
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Create New Group</DialogTitle>
                    <DialogDescription>Create a new group to share passwords with others.</DialogDescription>
                  </DialogHeader>
                  <div className="space-y-4 py-4">
                    <div className="space-y-2">
                      <Label htmlFor="group-name">Group Name</Label>
                      <Input
                        id="group-name"
                        placeholder="e.g., Family, Work Team"
                        value={newGroupName}
                        onChange={(e) => setNewGroupName(e.target.value)}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="group-description">Description</Label>
                      <Textarea
                        id="group-description"
                        placeholder="Describe the purpose of this group"
                        value={newGroupDescription}
                        onChange={(e) => setNewGroupDescription(e.target.value)}
                        rows={3}
                      />
                    </div>
                  </div>
                  <DialogFooter>
                    <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                      Cancel
                    </Button>
                    <Button onClick={handleCreateGroup}>Create Group</Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            </div>
          </div>

          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green"></div>
            </div>
          ) : error ? (
            <div className="text-center text-destructive p-4 bg-destructive/10 rounded-md">{error}</div>
          ) : filteredGroups.length === 0 ? (
            <div className="text-center p-8 bg-muted rounded-lg">
              <p className="text-lg text-muted-foreground">
                {searchTerm ? "No groups match your search" : "No groups found. Create your first group!"}
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredGroups.map((group) => (
                <Card
                  key={group.id}
                  className="overflow-hidden border-2 border-green-light/20 hover:shadow-md transition-shadow"
                >
                  <CardHeader className="bg-gradient-to-r from-green-light/10 to-purple-light/10 pb-2">
                    <CardTitle className="text-xl text-green-dark dark:text-green-light">{group.name}</CardTitle>
                    {group.created_at && (
                      <CardDescription>Created: {new Date(group.created_at).toLocaleDateString()}</CardDescription>
                    )}
                  </CardHeader>
                  <CardContent className="pt-4">
                    <p className="text-muted-foreground mb-4">{group.description || "No description"}</p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <Users className="h-5 w-5 text-muted-foreground mr-2" />
                        <span className="text-sm text-muted-foreground">{group.member_count || 0} members</span>
                      </div>
                      {group.role && (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-100">
                          {group.role}
                        </span>
                      )}
                    </div>
                  </CardContent>
                  <CardFooter className="pt-0">
                    <Button
                      onClick={() => navigateToGroup(group.name)}
                      className="w-full bg-gradient-to-r from-green to-purple hover:from-green-dark hover:to-purple-dark transition-all duration-300"
                    >
                      View Group <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </CardFooter>
                </Card>
              ))}
            </div>
          )}
        </main>
        <Toaster />
      </div>
    </AuthCheck>
  )
}
