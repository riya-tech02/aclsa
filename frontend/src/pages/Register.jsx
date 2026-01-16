// Register.jsx
import { useState } from "react";

export default function Register({ onRegister, onSwitchToLogin }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleRegister(e) {
    e.preventDefault();
    setError("");

    if (!name || !email || !password || !confirmPassword) {
      setError("Please fill in all fields");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords don't match");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    setLoading(true);
    setTimeout(() => {
      localStorage.setItem("token", "demo-token");
      localStorage.setItem("userEmail", email);
      localStorage.setItem("userName", name);
      onSwitchToLogin();
    }, 1000);
  }

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      padding: "20px"
    }}>
      <div style={{
        background: "white",
        borderRadius: "16px",
        boxShadow: "0 20px 60px rgba(0,0,0,0.3)",
        padding: "48px",
        width: "100%",
        maxWidth: "440px"
      }}>
        {/* Logo/Title */}
        <div style={{ textAlign: "center", marginBottom: "32px" }}>
          <div style={{
            width: "64px",
            height: "64px",
            background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            borderRadius: "16px",
            margin: "0 auto 16px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "32px",
            fontWeight: "bold",
            color: "white"
          }}>
            A
          </div>
          <h1 style={{ 
            fontSize: "28px", 
            fontWeight: "700",
            margin: "0 0 8px 0",
            color: "#1a202c"
          }}>
            Create Account
          </h1>
          <p style={{ 
            color: "#718096", 
            margin: 0,
            fontSize: "14px"
          }}>
            Start your AI-powered learning journey
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div style={{
            background: "#fee",
            color: "#c33",
            padding: "12px 16px",
            borderRadius: "8px",
            marginBottom: "24px",
            fontSize: "14px",
            border: "1px solid #fcc"
          }}>
            {error}
          </div>
        )}

        {/* Register Form */}
        <form onSubmit={handleRegister}>
          <div style={{ marginBottom: "20px" }}>
            <label style={{
              display: "block",
              fontSize: "14px",
              fontWeight: "600",
              color: "#374151",
              marginBottom: "8px"
            }}>
              Full Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="John Doe"
              style={{
                width: "100%",
                padding: "12px 16px",
                border: "2px solid #e5e7eb",
                borderRadius: "8px",
                fontSize: "14px",
                outline: "none",
                transition: "all 0.2s",
                boxSizing: "border-box"
              }}
              onFocus={(e) => e.target.style.borderColor = "#667eea"}
              onBlur={(e) => e.target.style.borderColor = "#e5e7eb"}
            />
          </div>

          <div style={{ marginBottom: "20px" }}>
            <label style={{
              display: "block",
              fontSize: "14px",
              fontWeight: "600",
              color: "#374151",
              marginBottom: "8px"
            }}>
              Email Address
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              style={{
                width: "100%",
                padding: "12px 16px",
                border: "2px solid #e5e7eb",
                borderRadius: "8px",
                fontSize: "14px",
                outline: "none",
                transition: "all 0.2s",
                boxSizing: "border-box"
              }}
              onFocus={(e) => e.target.style.borderColor = "#667eea"}
              onBlur={(e) => e.target.style.borderColor = "#e5e7eb"}
            />
          </div>

          <div style={{ marginBottom: "20px" }}>
            <label style={{
              display: "block",
              fontSize: "14px",
              fontWeight: "600",
              color: "#374151",
              marginBottom: "8px"
            }}>
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              style={{
                width: "100%",
                padding: "12px 16px",
                border: "2px solid #e5e7eb",
                borderRadius: "8px",
                fontSize: "14px",
                outline: "none",
                transition: "all 0.2s",
                boxSizing: "border-box"
              }}
              onFocus={(e) => e.target.style.borderColor = "#667eea"}
              onBlur={(e) => e.target.style.borderColor = "#e5e7eb"}
            />
          </div>

          <div style={{ marginBottom: "24px" }}>
            <label style={{
              display: "block",
              fontSize: "14px",
              fontWeight: "600",
              color: "#374151",
              marginBottom: "8px"
            }}>
              Confirm Password
            </label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••"
              style={{
                width: "100%",
                padding: "12px 16px",
                border: "2px solid #e5e7eb",
                borderRadius: "8px",
                fontSize: "14px",
                outline: "none",
                transition: "all 0.2s",
                boxSizing: "border-box"
              }}
              onFocus={(e) => e.target.style.borderColor = "#667eea"}
              onBlur={(e) => e.target.style.borderColor = "#e5e7eb"}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: "14px",
              background: loading ? "#9ca3af" : "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
              color: "white",
              border: "none",
              borderRadius: "8px",
              fontSize: "16px",
              fontWeight: "600",
              cursor: loading ? "not-allowed" : "pointer",
              transition: "transform 0.2s",
              marginBottom: "16px"
            }}
            onMouseOver={(e) => !loading && (e.target.style.transform = "translateY(-2px)")}
            onMouseOut={(e) => e.target.style.transform = "translateY(0)"}
          >
            {loading ? "Creating account..." : "Create Account"}
          </button>
        </form>

        {/* Sign In Link */}
        <div style={{ textAlign: "center" }}>
          <p style={{ color: "#6b7280", fontSize: "14px", margin: 0 }}>
            Already have an account?{" "}
            <button
              onClick={onSwitchToLogin}
              style={{
                background: "none",
                border: "none",
                color: "#667eea",
                fontWeight: "600",
                cursor: "pointer",
                fontSize: "14px",
                textDecoration: "none"
              }}
              onMouseOver={(e) => e.target.style.textDecoration = "underline"}
              onMouseOut={(e) => e.target.style.textDecoration = "none"}
            >
              Sign in
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
