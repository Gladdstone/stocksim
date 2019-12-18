const loginUser = user => ({
    type: 'LOGIN_USER',
    payload: user
});

export const userPostRegistration = user => {

    return dispatch => {

        return fetch('http://localhost:5000/registration', { // TODO - convert to env variable
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ user })
        })
            .then(resp => resp.json())
            .then(data => {

                if (data.message) {
                // TODO - handle invalid creation error
                } else {

                    localStorage.setItem('token', data.jwt);
                    dispatch(loginUser(data.user));

                }

            });

    };

};
