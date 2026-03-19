import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Sidebar from './Sidebar';
import './MainChat.css';

const BACKEND_URL = 'http://127.0.0.1:8000';

function MainChat() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [papersIndexed, setPapersIndexed] = useState(false);
  const [topic, setTopic] = useState('');
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [fetchingPapers, setFetchingPapers] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [sessionStats, setSessionStats] = useState({
    topic: 'Not selected',
    papersIndexed: 0,
    retrievalQuality: 'N/A'
  });

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }
    setUser({ name: 'User' });
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const handleFetchPapers = async (e) => {
    e.preventDefault();
    
    if (!topic.trim()) {
      setError('Please enter a research topic');
      return;
    }

    setError('');
    setFetchingPapers(true);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${BACKEND_URL}/fetch_papers`,
        { topic, max_results: 5 },
        { headers: { 'Authorization': `Bearer ${token}` } }
      );

      if (response.data.papers && response.data.papers.length > 0) {
        localStorage.setItem('indexedPapers', JSON.stringify(response.data.papers));
      }
      
      setPapersIndexed(true);
      setSessionStats(prev => ({
        ...prev,
        topic: topic,
        papersIndexed: response.data.papers?.length || 5
      }));
      
      setTopic('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch papers');
    } finally {
      setFetchingPapers(false);
    }
  };

  const saveSummary = (queryText, answer, researchGaps) => {
    try {
      const newSummary = {
        id: Date.now(),
        query: queryText,
        answer,
        researchGaps,
        date: new Date().toLocaleString(),
        topic: sessionStats.topic
      };

      const saved = localStorage.getItem('savedSummaries');
      const summaries = saved ? JSON.parse(saved) : [];
      summaries.unshift(newSummary);
      
      if (summaries.length > 20) {
        summaries.pop();
      }

      localStorage.setItem('savedSummaries', JSON.stringify(summaries));
    } catch (err) {
      console.error('Error saving summary:', err);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a research question');
      return;
    }

    if (!papersIndexed) {
      setError('Please fetch papers first');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${BACKEND_URL}/research_query`,
        { query, top_k: 6 },
        { headers: { 'Authorization': `Bearer ${token}` } }
      );

      setResult(response.data);
      saveSummary(query, response.data.answer, response.data.research_gaps);
      
      setSessionStats(prev => ({
        ...prev,
        retrievalQuality: response.data.meta?.quality || 'N/A'
      }));
      
      setQuery('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch results');
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return <div className="loading">Initializing Core Systems...</div>;
  }

  return (
    <div className="main-chat-container">
      <div className="sidebar-wrapper">
        <Sidebar onLogout={handleLogout} userName={user.name} />
      </div>

      <div className="chat-main">
        {/* Scrollable Results / Fetch Area */}
        <div className="chat-scroll-area">
          {!papersIndexed ? (
            <div className="fetch-container-centered">
              <div className="fetch-glow-box">
                <h2 className="title-glow">CEREBRA</h2>
                <p className="subtitle">Initialize knowledge base sequence.</p>
                
                {error && <div className="error-box">{error}</div>}
                
                <form onSubmit={handleFetchPapers} className="fetch-form-crazy">
                  <input
                    type="text"
                    className="fetch-input-crazy"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    placeholder="ENTER RESEARCH TOPIC..."
                    disabled={fetchingPapers}
                  />
                  <button 
                    type="submit"
                    className="fetch-btn-crazy"
                    disabled={fetchingPapers}
                  >
                    {fetchingPapers ? 'INDEXING...' : 'EXECUTE'}
                  </button>
                </form>
              </div>
            </div>
          ) : (
            <div className="results-container">
              {loading && (
                <div className="loading-box">
                  <div className="spinner"></div>
                  <p className="loading-text">SYNTHESIZING RESPONSE MATRIX...</p>
                </div>
              )}
              
              {error && papersIndexed && <div className="error-box">{error}</div>}

              {result && !loading && (
                <div className="result-fade-in">
                  <div className="card answer-card pulse-glow">
                    <h3 className="section-title">AI SYNTHESIS</h3>
                    <p className="answer-text">{result.answer}</p>
                  </div>

                  {result.research_gaps && result.research_gaps.length > 0 && (
                    <div className="section">
                      <h3 className="section-title">IDENTIFIED GAP VECTORS</h3>
                      <div className="gaps-grid">
                        {result.research_gaps.map((gap, idx) => (
                          <div key={idx} className="gap-card crazy-hover" style={{ animationDelay: `${idx * 0.1}s` }}>
                            <h4 className="gap-title">{gap.hypothesis}</h4>
                            <div className="gap-item-box">
                              <span className="gap-label">MECHANISM</span> 
                              <span className="gap-value">{gap.mechanism}</span>
                            </div>
                            <div className="gap-item-box">
                              <span className="gap-label">METRIC</span> 
                              <span className="gap-value">{gap.metric}</span>
                            </div>
                            <div className="gap-item-box">
                              <span className="gap-label">EXP. DESIGN</span> 
                              <span className="gap-value">{gap.experiment}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {!result && !loading && papersIndexed && (
                <div className="empty-state">
                  <div className="pulsing-icon"></div>  
                  <span>SYSTEM ONLINE. AWAITING PROMPT...</span>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Pinned Bottom Query Box */}
        {papersIndexed && (
          <div className="query-bottom-bar">
            <div className="query-box-inner">
               <button 
                  onClick={() => setPapersIndexed(false)}
                  className="btn-change-topic-icon"
                  title="RESET TOPIC"
                >
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
                    <path d="M3 3v5h5" />
                  </svg>
                </button>
              <form onSubmit={handleSearch} className="query-form-crazy">
                <input
                  type="text"
                  className="query-input-crazy"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="INPUT QUERY PARAMETERS..."
                  disabled={loading}
                />
                <button 
                  type="submit"
                  className="query-btn-crazy"
                  disabled={loading || !query.trim()}
                >
                  {loading ? (
                    <div className="mini-spinner"></div>
                  ) : (
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <line x1="22" y1="2" x2="11" y2="13"></line>
                      <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                    </svg>
                  )}
                </button>
              </form>
            </div>
          </div>
        )}
      </div>

      <div className="session-info">
        <div className="info-card">
          <h3>SESSION TELEMETRY</h3>
          <div className="info-item">
            <span className="info-label">TARGET:</span>
            <span className="info-value">{sessionStats.topic}</span>
          </div>
          <div className="info-item">
            <span className="info-label">NODES:</span>
            <span className="info-value">{sessionStats.papersIndexed}</span>
          </div>
          <div className="info-item">
            <span className="info-label">QUALITY:</span>
            <span className="info-value">{sessionStats.retrievalQuality}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MainChat;