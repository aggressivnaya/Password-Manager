import { useState, useEffect } from "react"

function Groups({ setActiveGroup }) {
  const [groups, setGroups] = useState([])

  useEffect(() => {
    fetchGroups()
  }, [])

  const fetchGroups = async () => {
    const response = await fetch("http://localhost:5000/groups")
    const data = await response.json()
    setGroups(data)
  }

  return (
    <div className="groups">
      <h2>Your Groups</h2>
      <ul>
        {groups.map((group) => (
          <li key={group.id}>
            <span>{group.name}</span>
            {group.isManager && <span className="manager-badge">Manager</span>}
            <button onClick={() => setActiveGroup(group)}>Enter</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Groups

