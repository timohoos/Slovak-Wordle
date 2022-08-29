function baseURL() {
    return process.env.REACT_APP_BACKEND_URL || "http://localhost:5001";
}


export function startNewGame() {
    fetch(`${baseURL()}/new-game`, {
        method: 'POST',
        credentials: 'include', //to send cookies on cross origin request
        headers: {
            'Accept': 'application/json'
        }
    })
        .then((response) => response.json())
        .then((data) => console.log('Success:', data))
        .catch((error) => console.error('Error:', error))
}


export async function guessWord(guess) {
    try {
        const response = await fetch(`${baseURL()}/guess`, {
            method: 'POST',
            credentials: 'include', //to send cookies on cross origin request
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({guess: guess})
        })
        return await response.json();
    } catch(error) {
        console.error('Error: ', error)
    }
}


export async function getGame() {
    try {
        const response = await fetch(`${baseURL()}/get-game`, {
            method: 'POST',
            credentials: 'include', //to send cookies on cross origin request
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        })
        return await response.json();
    } catch(error) {
        console.error('Error: ', error)
    }
}


export async function getWord() {
    try {
        const response = await fetch(`${baseURL()}/get-word`, {
            method: 'POST',
            credentials: 'include', //to send cookies on cross origin request
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        })
        return await response.json();
    } catch(error) {
        console.error('Error: ', error)
    }
}
