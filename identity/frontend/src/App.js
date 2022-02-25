import React from 'react';
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";

import { RegisterPage } from "./Pages/Register";


export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<div>Home</div>} />
                <Route path="/register" element={<RegisterPage />} />
            </Routes>
        </BrowserRouter>
    );
}
