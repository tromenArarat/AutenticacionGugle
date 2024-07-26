const express = require('express');
const session = require('express-session');
const passport = require('passport');
require('dotenv').config(); // Cargar las variables de entorno
require('./models');
require('./config/passport')(passport);

const sequelize = require('./models');
sequelize.sync()
    .then(() => console.log('Database & tables created!'))
    .catch(err => console.log('Error: ' + err));

const authRoutes = require('./routes/auth');
const profileRoutes = require('./routes/profile'); // Mover esta línea después de la sincronización de sequelize

const app = express();

app.use(
    session({
        secret: process.env.SESSION_SECRET,
        resave: false,
        saveUninitialized: true
    })
);

app.use(passport.initialize());
app.use(passport.session());

app.use('/auth', authRoutes);
app.use('/', profileRoutes); // Mover esta línea después de la inicialización de passport

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server started on port ${PORT}`));