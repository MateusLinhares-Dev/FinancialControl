import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import FinanceView from './components/FinanceView';
import Dashboard from './components/Dashboard';
import Reports from './components/Reports';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <ul className="navbar-nav">
            <li className="nav-item">
              <Link to="/" className="nav-link">Finance</Link>
            </li>
            <li className="nav-item">
              <Link to="/dashboard" className="nav-link">Dashboard</Link>
            </li>
            <li className="nav-item">
              <Link to="/reports" className="nav-link">Reports</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<FinanceView />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/reports" element={<Reports />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
