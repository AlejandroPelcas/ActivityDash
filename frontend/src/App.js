import './App.css';
import GetDataButton from './getDataButton';
import RefreshToken from './RefreshToken';
import {useState} from 'react';

function App() {
  const [refreshToken, setRefreshToken] = useState([]);
  const [runningData, setRunningData] = useState([]);

  return (
    <div className="App">
      <header className="App-header">
        <p>Strava Activity Tracker</p>
        <GetDataButton 
          runningData={runningData}
          setRunningData={setRunningData}/>
        <RefreshToken
          refreshToken={refreshToken}
          setRefreshToken={setRefreshToken} 
        />
      </header>
    </div>
  );
}

export default App;
