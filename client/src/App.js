import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import axios from 'axios';
import Login from './components/Login';
import Signup from './components/Signup';
import MemberPage from './components/MemberPage';
import AdminPage from './components/AdminPage';
import AdvisorPage from './components/AdvisorPage';
import CoordinatorPage from './components/CoordinatorPage';

function App() {
    const [userRole, setUserRole] = useState(null);

    const login = async (username, password) => {
        try {
            const response = await axios.post('http://localhost:5000/api/auth/login', { username, password });
            setUserRole(response.data.role);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login onLogin={login} />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="/member" element={userRole === 'club member' ? <MemberPage /> : <Navigate to="/login" />} />
                <Route path="/admin" element={userRole === 'club administrator' ? <AdminPage /> : <Navigate to="/login" />} />
                <Route path="/advisor" element={userRole === 'faculty advisor' ? <AdvisorPage /> : <Navigate to="/login" />} />
                <Route path="/coordinator" element={userRole === 'event coordinator' ? <CoordinatorPage /> : <Navigate to="/login" />} />
                <Route path="/" element={<Navigate to="/login" />} />
            </Routes>
        </Router>
    );
}

export default App;
