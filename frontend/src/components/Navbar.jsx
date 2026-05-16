import React from 'react';
import './Navbar.css';

const Navbar = ({ activeTab, setActiveTab }) => {
  const navItems = [
    { id: 'generate', label: 'Generate', icon: '🧠' },
    { id: 'saved', label: 'Saved Questions', icon: '🔖' },
    { id: 'tips', label: 'Interview Tips', icon: '💡' },
  ];

  return (
    <nav className="navbar">
      <div className="nav-logo">
        <span className="logo-icon">🚀</span>
        <span className="logo-text">InterviewPilot</span>
      </div>
      <div className="nav-links">
        {navItems.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
            onClick={() => setActiveTab(item.id)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
};

export default Navbar;
