import serviceApi from '../api/serviceApi';

const loginUser = user => ({
    type: 'LOGIN_USER',
    payload: user
});

export const userPostRegistration = user => {

    return dispatch => {

        return serviceApi.register(user).then(data => {

            if (!data.error) {

                console.log(data.error);

            } else {

                console.log('response received');
                localStorage.setItem('token', data.access_token);
                dispatch(loginUser(data.user));

            }

        });

    };

};

export const userPostLogin = user => {

    return dispatch => {

        return serviceApi.login(user).then(data => {

            if (!data.error) {

                console.log(data.error);

            } else {

                localStorage.setItem('token', data.access_token);
                dispatch(loginUser(data.user));

            }

        });

    };

};
