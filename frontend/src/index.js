import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';


function Square(props) {

    return (
        <button className="square" onClick={props.onClick}>
            {props.value}
        </button>
    );
}

function getReq() {
    fetch('http://localhost:5001/new-game', {
        method: 'POST',
        credentials: 'include', //to send cookies on cross origin request
        headers: {
            'Accept': 'application/json'
        }
    })
    .then((response) => response.json())
    .then((value) => console.log(value))
    .catch(() => {console.log("Something went wrong.")});
}


// ========================================

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Square onClick={getReq} value={1}/>);
