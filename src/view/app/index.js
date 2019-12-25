import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';
import { Provider } from 'react-redux';
import configureStore from './modules/store';

import App from './App';

import './index.less';
import 'bootstrap/dist/css/bootstrap.css';

const store = configureStore(window.REDUX_INITIAL_DATA);

ReactDOM.render(
    <Provider store={store}>
        <Router>
            <App />
        </Router>
    </Provider>,
    document.getElementById('root'));
