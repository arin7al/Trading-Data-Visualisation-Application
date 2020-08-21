import React from "react";
import TradeCategoryRow from "./TradeCategoryRow";
import TradeRow from "./TradeRow";

const TradeTable = props => {
  let rows = [];
  let lastCategory = null;
  props.products.forEach(product => {
    const lowerCaseProductName = product.name.toLowerCase();
    const lowerCaseFilterText = 
      props.searchDetails.filterText.toLowerCase();
    if(
      lowerCaseProductName.indexOf(lowerCaseFilterText) === -1 ||
      (!product.stocked && props.searchDetails.inStockOnly)
    ) {
      return;
    }
    if(product.category !== lastCategory) {
      rows.push(
        <TradeCategoryRow
          category={product.category}
          key={product.category}
        />
      );
      lastCategory = product.category;
    }
    rows.push(<TradeRow product={product} key={product.name} />);
  });
  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Price</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  );
};

export default TradeTable;
