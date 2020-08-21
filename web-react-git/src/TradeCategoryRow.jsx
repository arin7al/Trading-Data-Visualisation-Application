import React from "react";

const TradeCategoryRow = props => {
  return (
    <tr>
      <th colSpan="2">{props.category}</th>
    </tr>
  );
};

export default TradeCategoryRow;
