import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import GenerateForm from './components/GenerateForm';
import QuestionCard from './components/QuestionCard';
import './App.css';

import axios from 'axios';

function App() {
  const [activeTab, setActiveTab] = useState('generate');
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async (role) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:8001/api/v1/questions/generate', {
        role: role,
        count: 3
      });
      
      if (response.data && response.data.success) {
        setQuestions(response.data.data);
      } else {
        setError('Failed to generate questions. Please try again.');
      }
    } catch (err) {
      console.error("Error generating questions:", err);
      setError('An error occurred while connecting to the server.');
    } finally {
      setLoading(false);
    }
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
              
              {error && (
                <div className="error-message" style={{ color: 'red', marginBottom: '1rem' }}>
                  {error}
                </div>
              )}
              
              <div className="questions-grid">
                {questions.map((q, index) => (
                  <QuestionCard key={q.id || index} question={q.text} category={q.category} difficulty={q.difficulty} />
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
