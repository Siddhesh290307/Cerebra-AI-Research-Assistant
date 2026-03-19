import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Login.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Basic validation
      if (!email || !password) {
        setError('Please fill in all fields');
        setLoading(false);
        return;
      }

      // Call backend login endpoint
      const response = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || 'Login failed');
        setLoading(false);
        return;
      }

      // Save token
      localStorage.setItem('token', data.access_token);
      
      navigate('/chat');
    } catch (err) {
      setError('Login failed. Server may be down');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>CEREBRA</h1>
          <p>Login to your account</p>
        </div>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleLogin} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              placeholder="your.email@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
            />
          </div>

          <div className="form-footer">
            <Link to="#" className="forgot-password">
              Forgot Password?
            </Link>
          </div>

          <button 
            type="submit" 
            className="btn-login"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Log In'}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Don't have an account? <Link to="/signup" className="link-signup">Sign up instead.</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;