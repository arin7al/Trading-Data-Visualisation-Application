import React, { useState, useCallback } from "react";
import { useHistory } from "react-router-dom";

const DBURL = 'http://localhost:8090/authentication?'; //username=selvyn&password=gradprog2016`;

const Login = props => {     
    const [username, setUsername] = useState(``);
    const [password, setPassword] = useState(``);

    const history = useHistory();
    let isAuthorized = true;
    const checkLogin = useCallback(()=> {
        async function* getCredentials(apiURL) {
            const utf8Decoder = new TextDecoder('utf-8');
            const response = await fetch(apiURL);
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
        
        async function getAnswer(url) {
            for await (let chunk of getCredentials(url)) {
                console.log(chunk);
                if (chunk === 'True') {
                    history.push('/');
                }
                else {
                    alert('Authorization failed');
                }
            }
        }

        let reqURL = DBURL+'username='+username+'&password='+password;
        console.log(reqURL);
        getAnswer(reqURL);
    },[username, password]);
        


    var buttonStyle;
    
    return(
        <><h1>Login into Data Visualisation Application</h1>
        <hr />
        <div>
            <div>
            <input type="text" name="username" placeholder="Username" 
            value={username} onChange={e => setUsername(e.target.value)}/>
            </div>
            <div>
            <input type="password" name="password" placeholder="Password"
            value={password} onChange={e => setPassword(e.target.value)}/>
            </div>
            <button
                className="btn btn-default"
                style={buttonStyle}
                onClick={checkLogin}>Login
            </button>    
        </div></>
    )}

export default Login;