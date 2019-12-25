import { createStore, applyMiddleware } from 'redux';
import logger from 'redux-logger';
import thunk from 'redux-thunk';

import reducer from './reducer';

export default function configureStore(initialState) {

    const store = createStore(reducer, initialState, applyMiddleware(logger, thunk));
    return store;

}
