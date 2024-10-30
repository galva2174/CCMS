const express = require('express');
const bcrypt = require('bcryptjs'); // Using bcryptjs for consistency
const jwt = require('jsonwebtoken');
const User = require('../models/User');

const router = express.Router();

// Signup
router.post('/signup', async (req, res) => {
    const { username, password, role } = req.body;

    // Basic validation
    if (!username || !password || !role) {
        return res.status(400).json({ message: 'Please fill in all fields.' });
    }

    try {
        const hashedPassword = bcrypt.hashSync(password, 8);
        await User.create({ username, password: hashedPassword, role });
        res.status(201).json({ message: 'User registered successfully.' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error registering user.' });
    }
});

// Login
router.post('/login', async (req, res) => {
    const { username, password } = req.body;

    try {
        const results = await User.findByUsername(username);
        if (results.length === 0) return res.status(404).json({ message: 'User not found.' });

        const user = results[0];
        const passwordIsValid = bcrypt.compareSync(password, user.password);
        if (!passwordIsValid) return res.status(401).json({ auth: false, token: null, message: 'Invalid password.' });

        const token = jwt.sign({ id: user.id, role: user.role }, process.env.JWT_SECRET, { expiresIn: 86400 });
        res.status(200).json({ auth: true, token, role: user.role });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error logging in.' });
    }
});

module.exports = router;
