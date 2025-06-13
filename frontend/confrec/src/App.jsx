import { useState } from 'react'
import './App.css'

function App() {
  const [text, setText] = useState('')
  const [results, setResults] = useState([])

  async function fetchRecs() {
    const r = await fetch('/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ company_description: text })
    })
    setResults(await r.json())
  }

  return (
    <div className="container">
      <h1>SOFWEEK Recommender</h1>
      <textarea value={text} onChange={e => setText(e.target.value)} rows={4} style={{width:'100%'}} />
      <br />
      <button onClick={fetchRecs}>Recommend</button>
      <ul>
        {results.map(r => (
          <li key={r.type + r.id}>
            {r.type}: {r.text || r.id} (score {r.score.toFixed(3)})
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App
