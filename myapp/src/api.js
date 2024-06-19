import axios from 'axios';

const baseURL = 'http://127.0.0.1:8000'; // Substitua pelo endereço da sua API

const instance = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'text/xml',
    'Authorization': 'basic ' + btoa('mlinhares:1234')
  }
});

export const getBalances = async () => {
  try {
    const response = await instance.get('/api/v1/balance/');
    return response.data;
  } catch (error) {
    console.error("Houve um erro ao buscar os saldos!", error);
    throw error;
  }
};
