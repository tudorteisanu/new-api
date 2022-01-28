// const backendAddress = 'https://flask.testways.online/api/v1';
const backendAddress = 'http://localhost:5000/api/v1';

function post(url, data) {
    return new Promise((resolve, reject)=> {
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

            if (response.status !== 422) {
                errorText.innerHTML = errors.message
            } else {
                errorText.innerHTML = JSON.stringify(errors)
            }
            return reject(errors);
        }

        error.classList.add('hidden')
        errorText.innerHTML = ''
        return resolve(data)
    })
    })

}