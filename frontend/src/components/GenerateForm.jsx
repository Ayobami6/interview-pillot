import React, { useState } from 'react';
import './GenerateForm.css';

const GenerateForm = ({ onGenerate }) => {
  const [role, setRole] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (role.trim()) {
      onGenerate(role);
    }
  };

  return (
    <form className="generate-form" onSubmit={handleSubmit}>
      <div className="input-group">
        <input
          type="text"
          placeholder="e.g. Senior Frontend Engineer"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        />
        <button type="submit" className="btn-primary">
          Generate Questions
        </button>
      </div>
    </form>
  );
};

export default GenerateForm;
