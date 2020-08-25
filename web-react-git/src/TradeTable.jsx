import React from "react";
import TradeRow from "./TradeRow";

const TradeTable = props => {
  let rows = [];
  props.products.forEach(product => {
    const lowerCaseProductName = product.instrumentName.toLowerCase();
    const lowerCaseFilterText = 
      props.searchDetails.filterText.toLowerCase();
    if(
      lowerCaseProductName.indexOf(lowerCaseFilterText) === -1
    ) {
      return;
    }
    rows.push(<TradeRow product={product} key={product.time} />);
  });
  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Cpty</th>
          <th>Price</th>
          <th>Quantity</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  );
};

export default TradeTable;
