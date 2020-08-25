import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Switch} from 
'react-router-dom';
import axios from 'axios';


import FilterableTradeTable from "./Components/FilterableTradeTable";
import Loginnew from "./Components/Loginnew";
import PrivateRoute from './PrivateRoute';
import { AuthContext } from "./context/auth";

const DBURL = `http://localhost:8090/connection`;

const Status = props => { 
  const [dbstatus, setStatus] = useState('Database cant be accessed');

  const [temp, setTemp] = useState(0)

  //useEffect(()=>{
  //  setInterval(()=>{
  //    setTemp((prevTemp)=>prevTemp+1)
  //  }, 1000)
  //}, [])

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

    function getStatusDBnew() {
    axios.get(DBURL, {}).then(result => {
      if (result.status === 200) {
        if (result.data.connected === true) {
            setStatus("DB is accessible")
        } else {
            setStatus('Database cant be accessed')
        }
      } else {
        setStatus('Database cant be accessed')
      }
    }).catch(e => {
      setStatus('Database cant be accessed')
    });}
    
    setTimeout(() => { getStatusDBnew() }, 500);
  //}, [temp])
}, [])
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
      <div>
        <Switch>
        <Route path="/" component={Loginnew} />
        <Route exact path="/table" component={FilterableTradeTable}/>
        <PrivateRoute exact path="/data" component={FilterableTradeTable}/>
        </Switch>
      </div>
    </Router>
    </AuthContext.Provider>
  );
}

export default App;
