import React from 'react';
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";

import HomePage from "./Pages/Home";
import LoginPage from "./Pages/Login";


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
                <Link to="/login">Login</Link>
            </nav>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/home" element={<HomePage />} />
                <Route path="/login" element={<LoginPage />} />
            </Routes>
        </BrowserRouter>
    );
}
