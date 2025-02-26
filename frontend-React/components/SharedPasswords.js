import { useState, useEffect } from "react"

function SharedPasswords() {
  const [sharedPasswords, setSharedPasswords] = useState([])

  useEffect(() => {
    // In a real application, you'd fetch shared passwords from the server
    setSharedPasswords([
      { id: 1, name: "Company Wiki", username: "team@company.com", password: "********", sharedWith: "Marketing Team" },
      {
        id: 2,
        name: "Project Management",
        username: "pm@company.com",
        password: "********",
        sharedWith: "Project Managers",
      },
    ])
  }, [])

  return (
    <div className="shared-passwords">
      <h2>Shared Passwords</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Username</th>
            <th>Password</th>
            <th>Shared With</th>
          </tr>
        </thead>
        <tbody>
          {sharedPasswords.map((pw) => (
            <tr key={pw.id}>
              <td>{pw.name}</td>
              <td>{pw.username}</td>
              <td>{pw.password}</td>
              <td>{pw.sharedWith}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default SharedPasswords

