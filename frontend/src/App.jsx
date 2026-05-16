import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import GenerateForm from './components/GenerateForm';
import QuestionCard from './components/QuestionCard';
import './App.css';

const MOCK_QUESTIONS = [
  { id: 1, category: 'Technical', question: 'How do you optimize a React application with a large number of components?' },
  { id: 2, category: 'Behavioral', question: 'Describe a time you had to deal with a difficult team member and how you resolved it.' },
  { id: 3, category: 'Leadership', question: 'How do you mentor junior developers and ensure their growth within the team?' },
  { id: 4, category: 'Product', question: 'How do you balance technical debt with the need for rapid feature development?' },
];

function App() {
  const [activeTab, setActiveTab] = useState('generate');
  const [questions, setQuestions] = useState(MOCK_QUESTIONS);
  const [loading, setLoading] = useState(false);

  const handleGenerate = (role) => {
    setLoading(true);
    // Simulate AI generation
    setTimeout(() => {
      setQuestions([
        { id: Date.now(), category: 'AI Generated', question: `As a ${role}, how would you approach a critical system failure during peak hours?` },
        ...questions
      ]);
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="app-container">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="main-content">
        <div className="container">
          <Hero />
          
          {activeTab === 'generate' && (
            <div className="tab-content animate-in">
              <GenerateForm onGenerate={handleGenerate} />
              
              {loading && (
                <div className="loading-indicator">
                  <div className="spinner"></div>
                  <span>Generating expert questions...</span>
                </div>
              )}
              
              <div className="questions-grid">
                {questions.map((q) => (
                  <QuestionCard key={q.id} {...q} />
                ))}
              </div>
            </div>
          )}

          {activeTab === 'saved' && (
            <div className="tab-content animate-in">
              <h2>Saved Questions</h2>
              <p>You haven't saved any questions yet.</p>
            </div>
          )}

          {activeTab === 'tips' && (
            <div className="tab-content animate-in">
              <h2>Interview Tips</h2>
              <div className="tips-grid">
                <div className="card tip-card">
                  <h3>STAR Method</h3>
                  <p>Situation, Task, Action, Result. Use this to structure your behavioral answers.</p>
                </div>
                <div className="card tip-card">
                  <h3>Body Language</h3>
                  <p>Maintain eye contact and sit upright to convey confidence.</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
