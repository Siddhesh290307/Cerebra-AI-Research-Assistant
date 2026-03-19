import React, { useState, useEffect } from 'react';
import './SavedSummaries.css';

function SavedSummaries() {
  const [summaries, setSummaries] = useState([]);
  const [expandedId, setExpandedId] = useState(null);

  const loadSummaries = () => {
    const saved = localStorage.getItem('savedSummaries');
    if (saved) {
      setSummaries(JSON.parse(saved));
    } else {
      setSummaries([]);
    }
  };

  useEffect(() => {
    loadSummaries();
    const handleStorageChange = (e) => {
      if (e.key === 'savedSummaries') {
        loadSummaries();
      }
    };
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      loadSummaries();
    }, 500);
    return () => clearInterval(interval);
  }, []);

  const deleteSummary = (id) => {
    const updated = summaries.filter(s => s.id !== id);
    setSummaries(updated);
    localStorage.setItem('savedSummaries', JSON.stringify(updated));
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  if (summaries.length === 0) {
    return (
      <div className="summaries-empty">
        <div className="empty-pulsing-icon summary-pulse"></div>
        <p className="empty-title">NO QUERIES DETECTED</p>
        <p className="empty-text">AWAITING USER INPUT...</p>
      </div>
    );
  }

  return (
    <div className="summaries-container">
      <div className="summaries-header">
        <h3 className="summaries-count">QUERY LOGS ({summaries.length})</h3>
      </div>

      <div className="summaries-list">
        {summaries.map((summary, idx) => (
          <div 
            key={summary.id} 
            className="summary-card crazy-hover-sidebar"
            style={{ animationDelay: `${idx * 0.1}s` }}
          >
            <div 
              className="summary-header"
              onClick={() => setExpandedId(expandedId === summary.id ? null : summary.id)}
            >
              <div className="summary-title-section">
                <p className={`summary-query ${expandedId === summary.id ? 'text-glow-alt' : ''}`}>
                  {summary.query}
                </p>
                <span className="summary-date">{summary.date}</span>
              </div>
              <div className="summary-header-icons">
                <button
                  className="btn-delete-summary"
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteSummary(summary.id);
                  }}
                  title="PURGE LOG"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  </svg>
                </button>
                <span className={`expand-arrow ${expandedId === summary.id ? 'expanded' : ''}`}>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="6 9 12 15 18 9"></polyline>
                  </svg>
                </span>
              </div>
            </div>

            {expandedId === summary.id && (
              <div className="summary-details slide-down-anim">
                <div className="answer-section">
                  <label className="section-label">AI SYNTHESIS</label>
                  <p className="answer-text-box">{summary.answer}</p>
                  <button 
                    className="btn-copy-tech"
                    onClick={() => copyToClipboard(summary.answer)}
                  >
                    COPY TO CLIPBOARD
                  </button>
                </div>

                {summary.researchGaps && summary.researchGaps.length > 0 && (
                  <div className="gaps-section">
                    <label className="section-label">GAP VECTORS ({summary.researchGaps.length})</label>
                    <div className="gaps-list">
                      {summary.researchGaps.map((gap, idx) => (
                        <div key={idx} className="gap-item-sub">
                          <h4 className="gap-sub-title">{gap.hypothesis}</h4>
                          <div className="gap-sub-detail">
                            <span className="gap-sub-label">MECHANISM:</span> 
                            <span className="gap-sub-val">{gap.mechanism}</span>
                          </div>
                          <div className="gap-sub-detail">
                            <span className="gap-sub-label">METRIC:</span> 
                            <span className="gap-sub-val">{gap.metric}</span>
                          </div>
                          <div className="gap-sub-detail">
                            <span className="gap-sub-label">EXP. DESIGN:</span> 
                            <span className="gap-sub-val">{gap.experiment}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="summary-meta-bar">
                  <span className="meta-item-tag">TARGET: {summary.topic}</span>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default SavedSummaries;