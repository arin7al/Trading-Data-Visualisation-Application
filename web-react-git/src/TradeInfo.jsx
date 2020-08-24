import React, { useState, useEffect } from "react";

const TradeInfo = props => {
    return (
        <table>
        <thead>
            <tr>
            <th>Profit/Loss</th>
            <th>Eff. Profit/Loss</th>
            <th>End Position</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>
                    12.59
                </td>
                <td>
                    13.59
                </td>
                <td>
                    14.59
                </td>
            </tr>
        </tbody>
      </table>
    );
  };

export default TradeInfo;