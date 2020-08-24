import React, { useState } from "react";
import { Link, Redirect, useHistory } from "react-router-dom";
import axios from 'axios';
import { useAuth } from "../context/auth";

const DBURL = 'http://localhost:8090/authentication?'; 

function Loginnew(props) {
  const existingTokens = localStorage.getItem("tokens");
  const [isLoggedIn, setLoggedIn] = useState(existingTokens === 'True' ? true:false);
  const [isError, setIsError] = useState(false);
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const { setAuthTokens } = useAuth();
  const referer = '/data';
  const history = useHistory();

  if (isLoggedIn) {
    return <Redirect to={referer} />;
  }

  function postLogin() {
    let reqURL = DBURL+'username='+userName+'&password='+password; 
    axios.get(reqURL, {}).then(result => {
      if (result.status === 200) {
        console.log(result.data);
        if (result.data === 'True') {
            setAuthTokens(result.data);
            setLoggedIn(true);
            history.push('/data')
        } else {
            setIsError(true);  
            alert('Authorization failed');  
        }
      } else {
        setIsError(true);
        alert('Authorization failed');
      }
    }).catch(e => {
      setIsError(true);
    });
  }

  if (isLoggedIn) {
    return <Redirect to="/data" />;
  }

  return (
    <div>
      <div>
      <input
          type="username"
          value={userName}
          onChange={e => {
            setUserName(e.target.value);
          }}
          placeholder="email"
        />
        <input
          type="password"
          value={password}
          onChange={e => {
            setPassword(e.target.value);
          }}
          placeholder="password"
        />
        <button onClick={postLogin}>Sign In</button>
      </div>
    </div>
  );
}

export default Loginnew;