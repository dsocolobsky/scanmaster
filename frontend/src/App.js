import React from 'react';
import './App.css';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';

import Landing from './components/Landing';
import Host from './components/Host';

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route exact path="/"> <Landing /> </Route>
          <Route path="/landing"> <Landing /> </Route>
          <Route path="/host/:ip"> <Host /> </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
