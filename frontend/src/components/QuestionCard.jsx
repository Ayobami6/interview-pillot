import React from 'react';
import './QuestionCard.css';

const QuestionCard = ({ question, category }) => {
  return (
    <div className="question-card card">
      <div className="card-header">
        <span className="category-tag">{category}</span>
        <div className="card-actions">
          <button className="icon-btn">🔖</button>
          <button className="icon-btn">📋</button>
        </div>
      </div>
      <p className="question-text">{question}</p>
    </div>
  );
};

export default QuestionCard;
