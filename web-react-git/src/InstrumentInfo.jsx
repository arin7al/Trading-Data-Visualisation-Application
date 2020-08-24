import React from "react";
import { $, jQuery } from 'jquery';
import axios from 'axios';


export default class InstrumentInfo extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            instrument: 'Astronomica',
            average: 0.0
        };
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        this.setState({ instrument: event.target.value })
    }

    averageInstrumentValue = () => {
        fetch("URL", {
            method: 'POST',
            body: JSON.stringify({
                instrument: this.state.instrument
            })
        })
            .then(function (response) {
                console.log("It worked, response is: ", response)
                this.setState({average: 88.8});
            }).catch(function () {
                this.setState({average: 88.8});
                console.log("error");
            }.bind(this));
    };

    render() {
        const { average } = this.state;
        return (
            <div>
                <div>{average}</div>
                <p><select value={this.state.instrument} onChange={this.handleChange} name="instrument">
                    <option value="Astronomica">Astronomica</option>
                    <option value="Borealis">Borealis</option>
                    <option value="Celestial">Celestial</option>
                    <option value="Deuteronic">Deuteronic</option>
                    <option value="Eclipse">Eclipse</option>
                    <option value="Floral">Floral</option>
                    <option value="Galactia">Galactia</option>
                    <option value="Heliosphere">Heliosphere</option>
                    <option value="Interstella">Interstella</option>
                    <option value="Jupiter">Jupiter</option>
                    <option value="Koronis">Koronis</option>
                    <option value="Lunatic">Lunatic</option>
                </select></p>
                <button onClick={this.averageInstrumentValue}>Confirm</button>
            </div>
        );
    }
}

export { InstrumentInfo };