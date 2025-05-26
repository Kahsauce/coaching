import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    fetch('/sessions')
      .then((res) => res.json())
      .then((data) => setSessions(data));
  }, []);

  return (
    <div>
      <h1>Coaching App</h1>
      <ul>
        {sessions.map((s) => (
          <li key={s.id}>
            {s.date} - {s.sport} ({s.duration_min} min)
          </li>
        ))}
      </ul>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
