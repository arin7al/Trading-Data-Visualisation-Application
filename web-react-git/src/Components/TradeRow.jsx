import React from "react";

const ProductRow = props => {
  return <tr>
    <td>
    {
      props.product.instrumentName
    }
    </td>
    <td>
      {props.product.cpty}
    </td>
    <td>
      {props.product.price}
    </td>
    <td>
      {props.product.quantity}
    </td>
    <td>
      {props.product.time}
    </td>
  </tr> ;
};

export default ProductRow;
