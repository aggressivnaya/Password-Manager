import { useState, useEffect } from "react"
import { useAuth } from "../AuthContext"

function PrivatePasswords() {
  const [passwords, setPasswords] = useState([])
  const [newPassword, setNewPassword] = useState({ name: "", username: "", password: "" })
  const { token } = useAuth()

  useEffect(() => {
    fetchPasswords()
  }, [])

  const fetchPasswords = async () => {
    const response = await fetch("http://localhost:5000/passwords", {
      headers: {
        Authorization: token,
      },
    })
    const data = await response.json()
    setPasswords(data)
  }

  const addPassword = async () => {
    if (newPassword.name && newPassword.username && newPassword.password) {
      const response = await fetch("http://localhost:5000/passwords/add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: token,
        },
        body: JSON.stringify(newPassword),
      })
      const data = await response.json()
      setPasswords([...passwords, data])
      setNewPassword({ name: "", username: "", password: "" })
    }
  }

  return (
    <div className="private-passwords">
      <h2>Private Passwords</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Username</th>
            <th>Password</th>
          </tr>
        </thead>
        <tbody>
          {passwords.map((pw) => (
            <tr key={pw.id}>
              <td>{pw.name}</td>
              <td>{pw.username}</td>
              <td>{pw.password}</td>
            </tr>
          ))}
        </tbody>
      </table>
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
    </div>
  )
}

export default PrivatePasswords

