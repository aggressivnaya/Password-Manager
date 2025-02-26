import { useState, useEffect } from "react"

function GroupDetails({ group }) {
  const [passwords, setPasswords] = useState([])
  const [newPassword, setNewPassword] = useState({ name: "", username: "", password: "" })
  const [changeRequests, setChangeRequests] = useState([])

  useEffect(() => {
    fetchGroupPasswords()
  }, [group.id]) // Updated dependency

  const fetchGroupPasswords = async () => {
    const response = await fetch(`http://localhost:5000/groups/${group.id}/passwords`)
    const data = await response.json()
    setPasswords(data)
  }

  const addPassword = async () => {
    if (newPassword.name && newPassword.username && newPassword.password) {
      const response = await fetch(`http://localhost:5000/groups/${group.id}/passwords/add`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newPassword),
      })
      const data = await response.json()
      setPasswords([...passwords, data])
      setNewPassword({ name: "", username: "", password: "" })
    }
  }

  const requestChange = (passwordId) => {
    setChangeRequests([...changeRequests, { id: changeRequests.length + 1, passwordId, status: "pending" }])
  }

  const approveChange = (requestId) => {
    setChangeRequests(changeRequests.map((req) => (req.id === requestId ? { ...req, status: "approved" } : req)))
  }

  return (
    <div className="group-details">
      <h3>Group Passwords</h3>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Username</th>
            <th>Password</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {passwords.map((pw) => (
            <tr key={pw.id}>
              <td>{pw.name}</td>
              <td>{pw.username}</td>
              <td>{pw.password}</td>
              <td>
                {group.isManager ? (
                  <button
                    onClick={() =>
                      setPasswords(passwords.map((p) => (p.id === pw.id ? { ...p, password: "newpassword" } : p)))
                    }
                  >
                    Change Password
                  </button>
                ) : (
                  <button onClick={() => requestChange(pw.id)}>Request Change</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {group.isManager && (
        <div className="add-password">
          <input
            type="text"
            placeholder="Name"
            value={newPassword.name}
            onChange={(e) => setNewPassword({ ...newPassword, name: e.target.value })}
          />
          <input
            type="text"
            placeholder="Username"
            value={newPassword.username}
            onChange={(e) => setNewPassword({ ...newPassword, username: e.target.value })}
          />
          <input
            type="password"
            placeholder="Password"
            value={newPassword.password}
            onChange={(e) => setNewPassword({ ...newPassword, password: e.target.value })}
          />
          <button onClick={addPassword}>Add Password</button>
        </div>
      )}
      {group.isManager && changeRequests.length > 0 && (
        <div className="change-requests">
          <h4>Change Requests</h4>
          <ul>
            {changeRequests.map((req) => (
              <li key={req.id}>
                <span>Request for password ID: {req.passwordId}</span>
                <span>Status: {req.status}</span>
                {req.status === "pending" && <button onClick={() => approveChange(req.id)}>Approve</button>}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default GroupDetails

