import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
} from 'react-router-dom';

import { API_URL } from './api';

function Dashboard() {
  const [todaySessions, setTodaySessions] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/sessions/today`)
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
    fetch(`${API_URL}/sessions/week`)
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

function AddSession() {
  const [sport, setSport] = useState('');
  const [date, setDate] = useState('');
  const [duration, setDuration] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch(`${API_URL}/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: 0,
        date,
        sport,
        duration_min: parseInt(duration, 10),
      }),
    }).then(() => {
      setSport('');
      setDate('');
      setDuration('');
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h1>Ajouter une séance</h1>
      <input value={date} onChange={(e) => setDate(e.target.value)} type="date" required />
      <input value={sport} onChange={(e) => setSport(e.target.value)} placeholder="Sport" required />
      <input
        value={duration}
        onChange={(e) => setDuration(e.target.value)}
        type="number"
        placeholder="Durée"
        required
      />
      <button type="submit">Enregistrer</button>
    </form>
  );
}

function AddNutrition() {
  const [date, setDate] = useState('');
  const [calories, setCalories] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch(`${API_URL}/nutrition`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: 0,
        date,
        calories: parseInt(calories, 10),
      }),
    }).then(() => {
      setDate('');
      setCalories('');
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h1>Nutrition</h1>
      <input value={date} onChange={(e) => setDate(e.target.value)} type="date" required />
      <input
        value={calories}
        onChange={(e) => setCalories(e.target.value)}
        type="number"
        placeholder="Calories"
        required
      />
      <button type="submit">Enregistrer</button>
    </form>
  );
}

function AddInjury() {
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch(`${API_URL}/injuries`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: 0, start_date: start, end_date: end || null }),
    }).then(() => {
      setStart('');
      setEnd('');
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h1>Blessure</h1>
      <input value={start} onChange={(e) => setStart(e.target.value)} type="date" required />
      <input value={end} onChange={(e) => setEnd(e.target.value)} type="date" />
      <button type="submit">Enregistrer</button>
    </form>
  );
}

function Progress() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetch(`${API_URL}/stats/summary`).then((res) => res.json()).then(setStats);
  }, []);

  if (!stats) return <p>Chargement...</p>;

  return (
    <div>
      <h1>Progression</h1>
      <p>ACWR : {stats.acwr.toFixed(2)}</p>
      <p>Charges hebdo : {stats.weekly_loads.join(', ')}</p>
      <p>Progression : {stats.progression.toFixed(1)}%</p>
    </div>
  );
}

function Competitions() {
  const [comps, setComps] = useState([]);
  const [date, setDate] = useState('');
  const [name, setName] = useState('');

  useEffect(() => {
    fetch(`${API_URL}/competitions`).then((res) => res.json()).then(setComps);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch(`${API_URL}/competitions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: 0, date, name }),
    })
      .then((res) => res.json())
      .then((c) => {
        setComps([...comps, c]);
        setDate('');
        setName('');
      });
  };

  return (
    <div>
      <h1>Compétitions</h1>
      <ul>
        {comps.map((c) => (
          <li key={c.id}>{c.date} - {c.name}</li>
        ))}
      </ul>
      <form onSubmit={handleSubmit}>
        <input value={date} onChange={(e) => setDate(e.target.value)} type="date" required />
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Nom" required />
        <button type="submit">Ajouter</button>
      </form>
    </div>
  );
}

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">Dashboard</Link> |{' '}
        <Link to="/calendar">Calendrier</Link> |{' '}
        <Link to="/add-session">Ajouter séance</Link> |{' '}
        <Link to="/add-nutrition">Nutrition</Link> |{' '}
        <Link to="/add-injury">Blessure</Link> |{' '}
        <Link to="/competitions">Compétitions</Link> |{' '}
        <Link to="/progress">Progression</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/calendar" element={<Calendar />} />
        <Route path="/add-session" element={<AddSession />} />
        <Route path="/add-nutrition" element={<AddNutrition />} />
        <Route path="/add-injury" element={<AddInjury />} />
        <Route path="/competitions" element={<Competitions />} />
        <Route path="/progress" element={<Progress />} />
      </Routes>
    </Router>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
