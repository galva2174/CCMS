import React, { useState } from 'react';
import axios from 'axios';

const Signup = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('club member'); // Default role
    const [errorMessage, setErrorMessage] = useState('');

    const handleSignup = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/api/auth/signup', {
                username,
                password,
                role,
            });
            console.log('Signup successful:', response.data);
            // Redirect or notify user on successful signup
        } catch (error) {
            console.error(error);
            setErrorMessage('Signup failed. Please try again.');
        }
    };

    return (
        <div>
            <h2>Signup</h2>
            <form onSubmit={handleSignup}>
                <div>
                    <label>Username:</label>
                    <input 
                        type="text" 
                        value={username} 
                        onChange={(e) => setUsername(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input 
                        type="password" 
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>Role:</label>
                    <select value={role} onChange={(e) => setRole(e.target.value)} required>
                        <option value="club member">Club Member</option>
                        <option value="club administrator">Club Administrator</option>
                        <option value="faculty advisor">Faculty Advisor</option>
                        <option value="event coordinator">Event Coordinator</option>
                    </select>
                </div>
                <button type="submit">Signup</button>
                {errorMessage && <p>{errorMessage}</p>}
            </form>
        </div>
    );
};

export default Signup;
