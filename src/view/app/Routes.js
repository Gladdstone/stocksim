import React from 'react';
import { Route, Switch } from 'react-router-dom';

import Error404 from './pages/Error404/Error404.jsx';
import Login from './pages/login/login.jsx';
import Registration from './pages/registration/registration.jsx';

export default function Routes() {

    return (
        <Switch>
            <Route path='/' exact component={Login} />
            <Route path='/login' component={Login} />
            <Route path='/register' component={Registration} />
            <Route component={Error404} />
        </Switch>
    );

}
