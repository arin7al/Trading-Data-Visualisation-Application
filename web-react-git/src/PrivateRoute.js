import React from 'react';
import { Route, Redirect } from "react-router-dom";
import { useAuth } from "./context/auth";
import axios from 'axios';

function PrivateRoute({ component: Component, ...rest }) {
    const { authTokens } = useAuth();
  
    return (
      <Route
        {...rest}
        render={props =>
          (authTokens === 'true') ? (
            <Component {...props} />
          ) : (
            <Redirect to={{ pathname: "/login", state: { referer: props.location } }} />
          )
        }
      />
    );
  }

export default PrivateRoute;