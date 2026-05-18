import React from 'react';
import './QuestionCard.css';

const QuestionCard = ({ question, category, difficulty }) => {
  return (
    <div className="question-card card">
      <div className="card-header">
        <div className="tags">
          <span className="category-tag">{category}</span>
          {difficulty && <span className="difficulty-tag" data-level={difficulty.toLowerCase()}>{difficulty}</span>}
        </div>
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
