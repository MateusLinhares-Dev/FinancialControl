import React, { useEffect, useState } from 'react';
import axios from 'axios';

const FinanceView = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/v1/balance/', {
      headers: {
        'Content-Type': 'text/xml',
        'Authorization': 'basic ' + btoa('mlinhares:1234')
      }
    })
    .then(response => {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(response.data, "text/xml");
      const balances = xmlDoc.getElementsByTagName("Balance");
      const balanceArray = Array.from(balances).map(balance => ({
        id: balance.getElementsByTagName("id")[0].textContent,
        valueInsert: balance.getElementsByTagName("balance")[0].textContent,
        user: balance.getElementsByTagName("user")[0].textContent,
        money: balance.getElementsByTagName("money")[0].textContent,
        description: balance.getElementsByTagName("description")[0].textContent,
      }));
      console.log(parser)
      setData(balanceArray);
    })
    .catch(error => {
      console.error('Erro ao buscar dados:', error);
    });
  }, []);

  return (
    <div>
      <h1>Finance Data</h1>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Value Insert</th>
            <th>User</th>
            <th>Money</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.id}</td>
              <td>{item.valueInsert}</td>
              <td>{item.user}</td>
              <td>{item.money}</td>
              <td>{item.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FinanceView;
