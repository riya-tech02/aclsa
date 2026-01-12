import { useState } from "react";

const API = import.meta.env.VITE_API_URL;

export default function Register({ onRegister }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function register() {
    const res = await fetch(`${API}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    if (res.ok) onRegister();
    else alert("Registration failed");
  }

  return (
    <div style={{ padding: 40 }}>
      <h2>Register</h2>
      <input placeholder="Email" onChange={e => setEmail(e.target.value)} />
      <br />
      <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
      <br />
      <button onClick={register}>Create Account</button>
    </div>
  );
}
