import React, { useState, useEffect } from 'react';
import './MyPapers.css';

function MyPapers() {
  const [papers, setPapers] = useState([]);
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => {
    const savedPapers = localStorage.getItem('indexedPapers');
    if (savedPapers) {
      setPapers(JSON.parse(savedPapers));
    }
  }, []);

  const deletePaper = (idx) => {
    const updatedPapers = papers.filter((_, i) => i !== idx);
    setPapers(updatedPapers);
    localStorage.setItem('indexedPapers', JSON.stringify(updatedPapers));
  };

  if (papers.length === 0) {
    return (
      <div className="papers-empty">
        <div className="empty-pulsing-icon"></div>
        <p className="empty-title">NO PAPERS INDEXED</p>
        <p className="empty-text">AWAITING DATA INGESTION...</p>
      </div>
    );
  }

  return (
    <div className="papers-container">
      <div className="papers-header">
        <h3 className="papers-count">INDEXED NODES ({papers.length})</h3>
      </div>

      <div className="papers-list">
        {papers.map((paper, idx) => (
          <div 
            key={idx}
            className="paper-card crazy-hover-sidebar"
            style={{ animationDelay: `${idx * 0.1}s` }}
          >
            <div 
              className="paper-header"
              onClick={() => setExpandedId(expandedId === idx ? null : idx)}
            >
              <div className="paper-title-section">
                <h4 className={`paper-title ${expandedId === idx ? 'text-glow' : ''}`}>
                  {paper.title}
                </h4>
              </div>
              <div className="paper-header-icons">
                <button
                  className="btn-delete-paper"
                  onClick={(e) => {
                    e.stopPropagation();
                    deletePaper(idx);
                  }}
                  title="PURGE NODE"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  </svg>
                </button>
                <span className={`expand-arrow ${expandedId === idx ? 'expanded' : ''}`}>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="6 9 12 15 18 9"></polyline>
                  </svg>
                </span>
              </div>
            </div>

            {expandedId === idx && (
              <div className="paper-details slide-down-anim">
                <div className="detail-item-box">
                  <label className="detail-label">AUTHORS</label>
                  <p className="detail-value highlight-text">
                    {paper.authors && paper.authors.length > 0 
                      ? paper.authors.slice(0, 3).join(', ')
                      : 'UNKNOWN ENTITY'}
                    {paper.authors && paper.authors.length > 3 && ' ...'}
                  </p>
                </div>

                <div className="detail-item-box">
                  <label className="detail-label">SUMMARY</label>
                  <p className="detail-value paper-summary">
                    {paper.summary ? paper.summary.substring(0, 300) : 'NO DATA AVAILABLE'}
                    {paper.summary && paper.summary.length > 300 ? '...' : ''}
                  </p>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default MyPapers;