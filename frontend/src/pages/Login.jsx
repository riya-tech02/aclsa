import { useState } from "react";

const API = import.meta.env.VITE_API_URL;

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function login() {
    const res = await fetch(`${API}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
      onLogin();
    } else {
      alert("Login failed");
    }
  }

  return (
    <div style={{ padding: 40 }}>
      <h2>Login</h2>
      <input placeholder="Email" onChange={e => setEmail(e.target.value)} />
      <br />
      <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
      <br />
      <button onClick={login}>Login</button>
    </div>
  );
}
