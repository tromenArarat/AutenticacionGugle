const express = require('express');
const router = express.Router();

router.get('/profile', (req, res) => {
    if (!req.isAuthenticated()) {
        return res.redirect('/');
    }
    res.send(`Hello ${req.user.name}, your email is ${req.user.email}`);
});

module.exports = router;