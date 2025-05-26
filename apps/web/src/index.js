import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
} from 'react-router-dom';

const API = 'http://localhost:8000';

function Dashboard() {
  const [todaySessions, setTodaySessions] = useState([]);

  useEffect(() => {
    fetch(`${API}/sessions/today`)
      .then((res) => res.json())
      .then((data) => setTodaySessions(data));
  }, []);

  return (
    <div>
      <h1>Mes séances du jour</h1>
      <ul>
        {todaySessions.map((s) => (
          <li key={s.id}>
            {s.sport} - {s.duration_min} min
          </li>
        ))}
      </ul>
    </div>
  );
}

function Calendar() {
  const [weekSessions, setWeekSessions] = useState([]);

  useEffect(() => {
    fetch(`${API}/sessions/week`)
      .then((res) => res.json())
      .then((data) => setWeekSessions(data));
  }, []);

  return (
    <div>
      <h1>Calendrier hebdomadaire</h1>
      <ul>
        {weekSessions.map((s) => (
          <li key={s.id}>
            {s.date} - {s.sport}
          </li>
        ))}
      </ul>
    </div>
  );
}

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">Dashboard</Link> |{' '}
        <Link to="/calendar">Calendrier</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/calendar" element={<Calendar />} />
      </Routes>
    </Router>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
