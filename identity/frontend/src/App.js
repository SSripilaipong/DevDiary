import React from 'react';
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";

import { RegisterPage } from "./Pages/Register";


export default function App() {
    return (
        <BrowserRouter>
            <nav
                style={{
                    borderBottom: "solid 1px",
                    paddingBottom: "1rem"
                }}
            >
                <Link to="/">Home</Link> | {" "}
                <Link to="/register">Register</Link>
            </nav>
            <Routes>
                <Route path="/" element={<div>Home</div>} />
                <Route path="/register" element={<RegisterPage />} />
            </Routes>
        </BrowserRouter>
    );
}
