class serviceApi {

    static register(credentials) {

        const request = new Request('http://localhost:5000/registration', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ credentials })
        });

        return fetch(request).then(response => {

            return response.json();

        }).catch(error => {

            return error;

        });

    }

    static login(credentials) {

        const request = new Request('https://localhost:5000/login/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ credentials })
        });

        return fetch(request).then(response => {

            return response.json();

        }).catch(error => {

            return error;

        });

    }

}

export default serviceApi;
