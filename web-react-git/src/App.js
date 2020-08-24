import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Switch} from 
'react-router-dom';


import FilterableTradeTable from "./Components/FilterableTradeTable";
import Login from "./Components/Login";
import Loginnew from "./Components/Loginnew";
import PrivateRoute from './PrivateRoute';
import { AuthContext } from "./context/auth";

const DBURL = `http://localhost:8090/connection`;

const Status = props => { 
  const [dbstatus, setStatus] = useState('Database cant be accessed');

  const [temp, setTemp] = useState(0)

  useEffect(()=>{
    setInterval(()=>{
      setTemp((prevTemp)=>prevTemp+1)
    }, 2000)
  }, [])

  useEffect(()=>{
    async function* getStatus(apiURL) {
      const utf8Decoder = new TextDecoder('utf-8');
      const response = await fetch(apiURL);
      //console.log(response);
      const reader = response.body.getReader();
      let { value: chunk, done: readerDone } = await reader.read();
      chunk = chunk ? utf8Decoder.decode(chunk) : '';
      yield chunk;

      for (;;) {
        if (readerDone) {
          break;
        }
        ({ value: chunk, done: readerDone } = await reader.read());
        chunk = chunk ? utf8Decoder.decode(chunk) : '';
        if (chunk !== '') {
          yield chunk;
        }
      }
    }

    async function getStatusDB() {
      for await (let chunk of getStatus(DBURL)) {
        if (chunk === 'true') {
          setStatus("DB is accessible")
        }
      }
    }
    
    setTimeout(() => { getStatusDB() }, 1000);
  }, [temp])
  return(
    <label>{dbstatus}</label>);
}

function App(props) {
  const existingTokens = localStorage.getItem("tokens");
  console.log(existingTokens);
  const [authTokens, setAuthTokens] = useState(existingTokens);
  
  const setTokens = (data) => {
    localStorage.setItem("tokens", data);
    setAuthTokens(data);
  }

  return (
    <AuthContext.Provider value={{ authTokens, setAuthTokens: setTokens }}>
    <form><Status /></form>
    <Router>
      <Switch>
        <Route exact path="/" component={Loginnew}/>
        <Route path="/login" component={Loginnew} />
        <PrivateRoute path="/data" component={FilterableTradeTable}/>
      </Switch>
    </Router>
    </AuthContext.Provider>
  );
}

export default App;
