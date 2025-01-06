const express = require('express');
const passport = require('passport');
const router = express.Router();

// Ruta para iniciar sesión con Google
router.get('/google',
  passport.authenticate('google', { scope: ['profile', 'email'] })
);

// Ruta de callback de autenticación de Google
router.get('/google/callback',
  passport.authenticate('google', { failureRedirect: '/login' }),
  (req, res) => {
    // Redirigir al usuario después de la autenticación exitosa
    res.redirect('/');
  }
);

module.exports = router;