import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { GlobalStyles } from "./styles/DarkTheme";
import Login from "./components/auth/Login";
import Register from "./components/auth/Register";

const App = () => (
    <>
        <GlobalStyles />
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/register" element={<Register />} />
            </Routes>
        </Router>
    </>
);

export default App;