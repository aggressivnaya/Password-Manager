import { useState } from "react"
import { useAuth } from "./AuthContext"
import Login from "./components/Login"
import Signup from "./components/Signup"
import PrivatePasswords from "./components/PrivatePasswords"
import SharedPasswords from "./components/SharedPasswords"
import Groups from "./components/Groups"
import GroupDetails from "./components/GroupDetails"
import "./App.css"

function App() {
  const [activeTab, setActiveTab] = useState("private")
  const [activeGroup, setActiveGroup] = useState(null)
  const [isLogin, setIsLogin] = useState(true)
  const { token, logout } = useAuth()

  const toggleAuth = () => {
    setIsLogin(!isLogin)
  }

  if (!token) {
    return (
      <div className="app">
        <h1>Cute Password Manager</h1>
        {isLogin ? <Login onToggleAuth={toggleAuth} /> : <Signup onToggleAuth={toggleAuth} />}
      </div>
    )
  }

  return (
    <div className="app">
      <h1>Cute Password Manager</h1>
      <div className="tabs">
        <button className={activeTab === "private" ? "active" : ""} onClick={() => setActiveTab("private")}>
          Private
        </button>
        <button className={activeTab === "shared" ? "active" : ""} onClick={() => setActiveTab("shared")}>
          Shared
        </button>
        <button className={activeTab === "groups" ? "active" : ""} onClick={() => setActiveTab("groups")}>
          Groups
        </button>
        <button onClick={logout}>Logout</button>
      </div>
      <div className="content">
        {activeTab === "private" && <PrivatePasswords />}
        {activeTab === "shared" && <SharedPasswords />}
        {activeTab === "groups" && <Groups setActiveGroup={setActiveGroup} />}
      </div>
      {activeGroup && (
        <div className="group-details">
          <h2>Group: {activeGroup.name}</h2>
          <GroupDetails group={activeGroup} />
        </div>
      )}
    </div>
  )
}

export default App

