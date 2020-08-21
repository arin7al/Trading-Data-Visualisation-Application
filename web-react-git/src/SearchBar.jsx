import React from "react";

const SearchBar = props => {
  return (
  <form>
    <input type="text" placeholder="Search..."
    value={props.searchDetails.filterText}
    onChange={event => props.handleFilterTextChange(event.target.value)}
    ></input>
    <p>
      <input type="checkbox"
      checked={props.searchDetails.inStockOnly}
      onChange={event => props.handleInStockOnlyChange(event.target.checked)}
      ></input>Only show products in stock
    </p>
  </form>);
};

export default SearchBar;
