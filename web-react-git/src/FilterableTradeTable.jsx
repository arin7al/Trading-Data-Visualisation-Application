import React, { useState } from "react";
import SearchBar  from "./SearchBar";
import TradeTable from "./TradeTable";
import { PRODUCTS } from "./products"

const FilterableTradeTable = props => {
  const handleFilterTextChange = changedFilterText => {
    setFilterText(changedFilterText);
  };
  const handleInStockOnlyChange = changedInStockOnly => {
    setInStockOnly (changedInStockOnly);
  };


  const [filterText, setFilterText] = useState(``);
  const [inStockOnly, setInStockOnly] = useState(false);

  return (<div>
    <SearchBar 
      searchDetails={{filterText, inStockOnly}}
      handleFilterTextChange={ handleFilterTextChange}
      handleInStockOnlyChange={ handleInStockOnlyChange}
    />
    <TradeTable products ={PRODUCTS} 
      searchDetails={{filterText, inStockOnly}}
    />
    </div> );
};

export default FilterableTradeTable;
