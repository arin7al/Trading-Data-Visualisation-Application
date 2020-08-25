import React, { useState } from "react";
import { Link, Redirect, useHistory } from "react-router-dom";
import axios from 'axios';
import { useAuth } from "../context/auth";

const DBURL = 'http://localhost:8090/authentication?'; 

function Loginnew(props) {
  const existingTokens = localStorage.getItem("tokens");
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [isError, setIsError] = useState(false);
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const { setAuthTokens } = useAuth();
  // const referer = props.location.state.referer || '/';
  const history = useHistory();

  function postLogin() {
    let reqURL = DBURL+'username='+userName+'&password='+password; 
    axios.get(reqURL, {}).then(result => {
      if (result.status === 200) {
        console.log(result.data.success+typeof(result.data.success));
        if (result.data.success === true) {
            setAuthTokens(result.data.success);
            setLoggedIn(true);
            //console.log('Here')
            //history.push('/data')
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
    console.log('HERE')  
    //console.log(referer)
    //history.push('data')
    return <Redirect to='/table' />;
  }
  //if ((isLoggedIn)|(existingTokens === 'true')) {
  //if ((existingTokens === 'true')) {
  //  return <Redirect to="/data" />;
  //}

  return (
    <><h1>Login into Data Visualisation Application</h1>
    <hr />
    <div>
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
        </div>
        <div>
        <input
          type="password"
          value={password}
          onChange={e => {
            setPassword(e.target.value);
          }}
          placeholder="password"
        />
        </div>
        <div>
        <button onClick={postLogin}>Sign In</button>
        </div>
      </div>
    </div>
    </>
  );
}

export default Loginnew;