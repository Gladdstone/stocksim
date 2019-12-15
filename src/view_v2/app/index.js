import React from "react";
import ReactDOM from "react-dom";
import { Route, Link, BrowserRouter as Router } from 'react-router-dom';

import App from './App';
import Login from './login/login.jsx';
import Registration from './registration/registration.jsx';

import './index.less';

const routing = (
    <Router>
        <div>
            <ul>
                <li>
                    <Link to="/">Home</Link>
                </li>
                <li>
                    <Link to="/login">Login</Link>
                </li>
                <li>
                    <Link to="/register">Register</Link>
                </li>
            </ul>
            <Route path="/" component={App} />
            <Route path="/login" component={Login} />
            <Route path="/register" component={Registration} />
        </div>
    </Router>
);

ReactDOM.render(routing, document.getElementById('root'));
