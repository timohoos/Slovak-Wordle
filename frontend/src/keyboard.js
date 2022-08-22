import React from 'react';

import { getStateColor } from './utils';

class Key extends React.Component {
    render() {
        return (
            <button className={`square ${getStateColor(this.props.state)}`} onClick={this.props.onClick}>
                {this.props.value.toUpperCase()}
            </button>
        )
    }
}


class SpecialKey extends React.Component {
    render() {
        return (
            <button className='rectangle' onClick={this.props.onClick}>
                {this.props.value.toUpperCase()}
            </button>
        )
    }
}


export class Keyboard extends React.Component {
    render() {
        const keyboard = this.props.keys.map((key) => <Key key={key.value}
                                                           value={key.value}
                                                           state={key.state}
                                                           onClick={() => this.props.onClick(key)}/>);
        const enterKey = {value: 'Enter', state: null};
        const backspaceKey = {value: 'Backspace', state: null};
        return (
            <div className='board-row'>
                {keyboard}
                <SpecialKey key={enterKey.value} value={enterKey.value} state={enterKey.state}
                onClick={() => this.props.onClick(enterKey)}/>
                <SpecialKey key={backspaceKey.value} value={backspaceKey.value}
                state={backspaceKey.state} onClick={() => this.props.onClick(backspaceKey)}/>
            </div>
        )
    }
}
