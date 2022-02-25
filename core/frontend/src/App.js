import React from 'react';
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";

import HomePage from "./Pages/Home";
import LoginPage from "./Pages/Login";
import RegisterPage from "./Pages/Register";

export default function App() {
    return (
        <BrowserRouter>
            <nav
                style={{
                    borderBottom: "solid 1px",
                    paddingBottom: "1rem"
                }}
            >
                <Link to="/home">Home</Link> | {" "}
                <Link to="/login">Login</Link> | {" "}
                <Link to="/register">Register</Link>
            </nav>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/home" element={<HomePage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
            </Routes>
        </BrowserRouter>
    );
}
