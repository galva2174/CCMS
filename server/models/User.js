const db = require('..config/db'); // Assuming you have a db module for database interaction

const User = {
    create: async (userData) => {
        const { username, password, role } = userData;
        try {
            const result = await db.query('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', [username, password, role]);
            return result;
        } catch (error) {
            throw error;
        }
    },

    findByUsername: async (username) => {
        try {
            const result = await db.query('SELECT * FROM users WHERE username = ?', [username]);
            return result;
        } catch (error) {
            throw error;
        }
    },
};

module.exports = User;
