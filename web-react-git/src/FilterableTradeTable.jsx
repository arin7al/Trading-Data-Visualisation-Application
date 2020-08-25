import React, { useState, useEffect } from "react";
import SearchBar  from "./SearchBar";
import TradeTable from "./TradeTable";
import InstrumentInfo from "./InstrumentInfo";
import TradeInfo from "./TradeInfo";
import axios from 'axios';

//const PRODUCTSURL = `http://localhost:8080/streamTest`;
//const PRODUCTSURL = `http://localhost:8090/client/testservice`;
const PRODUCTSURL = `http://localhost:8090/deals`;

const FilterableTradeTable = props => {
  const [products, setProducts] = useState([]);
  const utf8Decoder = new TextDecoder('utf-8');
  useEffect(() => {
    let products = [];
    const getProducts = async () => {
      try {
        await fetch(PRODUCTSURL,  {method: 'GET'})
          .then(response => {
            console.log(response.status);
            console.log(response.statusText);
            console.log(response);
            console.log(response.body);
            return response.body;
          })
          .then(body => {
            console.log('GET IN BODY')
            const reader = body.getReader();
            return new ReadableStream({
              start(controller) {
                return pump();
                function pump() {
                  return reader.read().then(({ done, value }) => {
                    // When no more data needs to be consumed, close the stream
                    if (done) {
                        console.log('CHUNKS DONE');
                        controller.close();
                        return;
                    }
                    // Enqueue the next data chunk into our target stream
                    let chunk = value ? utf8Decoder.decode(value) : '';
                    console.log('CHUNK '+chunk);
                    products.push(JSON.parse(chunk));
                    if (products.length > 30) {
                      products.shift();
                    }
                    setProducts(products);
                    //getProducts();
                    controller.enqueue(value);
                    return pump();
                  });
                }
              }  
            })
          })
          .then(stream => {
            console.log('NEW STREAM');
            return new Response(stream);
          })
          .then(response => {
            console.log('RESPONSE JSON');
            return response.json()
          })
          .then(data => {
            console.log(data)
          })
          .catch(err => console.error(err))

        setProducts(products);
      }
      catch(e) {
        setProducts(e.message);
      }
    }

    async function* getProducts_new(apiURL) {
      const utf8Decoder = new TextDecoder('utf-8');
      const response = await fetch(apiURL);
      const reader = response.body.getReader();
      let { value: chunk, done: readerDone } = await reader.read();
      chunk = chunk ? utf8Decoder.decode(chunk) : '';
      yield chunk;

      for (;;) {
        if (readerDone) {
          console.log('CHUNKS DONE');
          break;
        }
        ({ value: chunk, done: readerDone } = await reader.read());
        chunk = chunk ? utf8Decoder.decode(chunk) : '';
        if (chunk !== '') {
          yield chunk;
        }
      }
    }

    async function run() {
      let counter = 0
      for await (let trade of getProducts_new(PRODUCTSURL)) {
        if (counter === 0) {products = []}
        console.log(trade.substring(5));
        // cut 'data:{}'
        products.push(JSON.parse(trade.substring(5)));
        counter += 1;
        if (counter === 10)
        {
          setProducts(products);
          counter = 0;
        }
      }
    }
    
    run();
    //getProducts();
  }, []);

  const [filterText, setFilterText] = useState(``);
  const handleFilterTextChange = changedFilterText => {
    setFilterText(changedFilterText);
  };
  let tableDisplay = [];
  if (products.length === 0) {
    tableDisplay.push(
      <h3 key="loading">
        Please wait whilst we try to load the products...
      </h3>
    );
  }
  else if (typeof products[0] !== "string") {
    tableDisplay.push(
      <TradeTable
        products={products}
        searchDetails={{ filterText }}
        key="loaded"
      />
    );
  }
  else {
    tableDisplay.push(
      <h3 key="error">
        There was a problem loading the products: {products}
      </h3>
    );
  }

  return (<div>
      <TradeInfo />
      <SearchBar 
        searchDetails={{filterText}}
        handleFilterTextChange={ handleFilterTextChange}
      />
      {tableDisplay}
      <InstrumentInfo />
    </div> 
  );
};

export default FilterableTradeTable;
