import React, { useState } from 'react';
import MyPapers from './MyPapers';
import SavedSummaries from './SavedSummaries';
import './Sidebar.css';

function Sidebar({ onLogout, userName }) {
  const [activeTab, setActiveTab] = useState('papers');

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="logo-container">
          <div className="cyber-pulse-logo"></div>
          <h1 className="logo-text">CEREBRA<span className="logo-tag">OS</span></h1>
        </div>
      </div>

      <div className="tabs">
        <button
          className={`tab-button ${activeTab === 'papers' ? 'active' : ''}`}
          onClick={() => setActiveTab('papers')}
        >
          <span className="tab-icon">📄</span>
          <span className="tab-text">Papers</span>
        </button>
        <button
          className={`tab-button ${activeTab === 'summaries' ? 'active' : ''}`}
          onClick={() => setActiveTab('summaries')}
        >
          <span className="tab-icon">💡</span>
          <span className="tab-text">Queries</span>
        </button>
      </div>

      <div className="content-area">
        {activeTab === 'papers' && <MyPapers />}
        {activeTab === 'summaries' && <SavedSummaries />}
      </div>

      <div className="sidebar-footer">
        <div className="user-card">
          <div className="user-avatar">{userName?.charAt(0).toUpperCase() || 'U'}</div>
          <div className="user-info">
            <p className="user-name">{userName || 'User'}</p>
            <p className="user-badge">Premium User</p>
          </div>
        </div>
        <button className="btn-logout" onClick={onLogout}>
          Logout
        </button>
      </div>
    </div>
  );
}

export default Sidebar;