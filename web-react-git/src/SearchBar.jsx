import React from "react";

const SearchBar = props => {
  return (
  <form>
    <input type="text" placeholder="Search..."
    value={props.searchDetails.filterText}
    onChange={event => props.handleFilterTextChange(event.target.value)}
    ></input>
  </form>);
};

export default SearchBar;
