const backendAddress = 'https://flask.testways.online/api/v1';
// const backendAddress = 'http://localhost:5000/api/v1';

function post(url, data) {
    return new Promise((resolve, reject) => {
        fetch(`${backendAddress}/${url}`, {
            method: 'post',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(async (response) => {
            const isJson = response.headers.get('content-type')?.includes('application/json');
            const data = isJson ? await response.json() : null;
            const error = document.getElementById('error')
            const errorText = document.getElementById('error-text')

            if (!response.ok) {
                const errors = data || response.status;
                error.classList.remove('hidden')

                if (errors.hasOwnProperty('message')) {
                    errorText.innerHTML = errors.message
                }
                return reject({errors, status_code: response.status});
            }

            error.classList.add('hidden')
            errorText.innerHTML = ''
            return resolve(data)
        })
    })

}