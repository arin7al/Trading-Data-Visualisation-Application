import React from "react";
import { BrowserRouter as Router } from 
'react-router-dom';


import FilterableTradeTable from "./FilterableTradeTable";

function App() {
  return (
    <Router>
      <h1>Data Visualisation Application (Trading)</h1>
      <hr />
      <FilterableTradeTable />
    </Router>
  );
}

export default App;
