// src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from "react-redux";
import { ToastContainer } from "react-toastify";

import store from "./store";
import App from './App';

import "react-toastify/dist/ReactToastify.css";
import './index.css';

ReactDOM.render(
    <Provider store={store}>
    <React.StrictMode>
        <ToastContainer position="top-right" autoClose={3000} />
        <App />
    </React.StrictMode>
    </Provider>,
    document.getElementById('root')
);