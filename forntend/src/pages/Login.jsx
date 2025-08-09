import React, { useState } from "react";
import "./Signup.css";
import { Link } from "react-router-dom";
import sideImage from "../assets/side.png";
import { FcGoogle } from "react-icons/fc";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/lgin/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const result = await response.json().catch(() => ({}));

      if (!response.ok) {
        setError(
          result.detail || `Error ${response.status}: ${response.statusText}`
        );
        setTimeout(() => setError(""), 2000);
        return;
      }

      setSuccess(`Welcome, ${result?.username || email}! Successfully login.`);
      setTimeout(() => setSuccess(""), 2000);

      setEmail("");
      setPassword("");
    } catch (err) {
      setError(err.message || "Something went wrong.");
      setTimeout(() => setError(""), 2000);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup">
      <div className="info">
        <div className="uper_info">
          <h1>Welcome back</h1>
          <span>Welcome back, please fill your details.</span>
        </div>
        <div className="form-info">
          <form onSubmit={handleSubmit} className="form">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              placeholder="Enter your email"
              required
              onChange={(e) => setEmail(e.target.value)}
            />

            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              placeholder="Enter your password"
              required
              onChange={(e) => setPassword(e.target.value)}
            />

            <div className="remember">
              <div className="check">
                <input type="checkbox" />
                <span>Remember me</span>
              </div>
              <a href="#">Forgot password</a>
            </div>

            <div className="btn">
              <button type="submit" disabled={loading} className="btn-1">
                {loading ? "Logging..." : "Login"}
              </button>
              <button type="button" className="google">
                <FcGoogle size={24} />
                Login with Google
              </button>
            </div>

            {error && <p style={{ color: "crimson" }}>{error}</p>}
            {success && <p style={{ color: "green" }}>{success}</p>}
            <span>
              Don’t have an account? <Link to="/signup">Signup</Link>
            </span>
          </form>
        </div>
      </div>
      <div className="img">
        <img src={sideImage} alt="Side" className="img-1" />
      </div>
    </div>
  );
};

export default Login;
