import Login from './components/Login';
import Signup from './components/Signup';
import Eventos from './components/Eventos'
import React, { useState } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

function App() {
  const [token, setToken] = useState();

  return (
    <Router>
      <div>
        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Switch>
          <Route path="/signup">
            <Signup />
          </Route>
          <Route path="/">
            {token?
            <Eventos token = {token} />
            :
            <Login setToken = {setToken} />
            }
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
