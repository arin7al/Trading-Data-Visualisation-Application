import React, { useState, useEffect } from "react";

const Login = props => { 
    isButtonClickedHandler = () => {
        this.setState({isButtonClicked = true});
    }
 
    var buttonStyle;
    var detailAboutUs = this.state.isButtonClicked == true ? <DetailAboutUs> 
                        </DetailAboutUs> : null;
    
    return(
        <div>
    
            <button
                className="btn btn-default"
                style={buttonStyle}
                onClick={this.isButtonClickedHandler()}>About Us
    
            </button>
        {detailAboutUs} //This will load only after the button click//
    
        </div>
    )}

export default Login;