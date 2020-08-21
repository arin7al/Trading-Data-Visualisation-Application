import React from "react";

const ProductRow = props => {
  return <tr>
    <td>
    {
      props.product.stocked ?
        props.product.name
      :
        <span style={{ color: "red" }}>{props.product.name}</span>
    }
    </td>
    <td>
      {props.product.price}
    </td>
  </tr> ;
};

export default ProductRow;
