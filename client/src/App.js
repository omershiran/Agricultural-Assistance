import React from 'react';
import RequestForm from './components/RequestForm';
import RequestsList from './components/RequestsList';
import VolunteerForm from './components/VolunteerForm'
import './App.css';

function App() {
  return (
    <div className="App">
      <VolunteerForm />
      {/* <RequestsList /> */}
    </div>
  );
}

export default App;
