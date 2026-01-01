import './App.css';
import GetDataButton from './getDataButton';
import RefreshToken from './RefreshToken';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>Strava Activity Tracker</p>
        <GetDataButton />
        <RefreshToken></RefreshToken>
      </header>
    </div>
  );
}

export default App;
