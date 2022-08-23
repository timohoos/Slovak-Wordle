import React from 'react';
import { keyBy } from 'lodash';

import { getStateColor } from './utils';

class Key extends React.Component {
    render() {
        return (
            <button className={`text-center w-9 h-12 rounded key ${getStateColor(this.props.state)}`} onClick={this.props.onClick}>
                {this.props.value.toUpperCase()}
            </button>
        )
    }
}


class SpecialKey extends React.Component {
    render() {
        return (
            <button className='text-center w-16 h-12 rounded key empty' onClick={this.props.onClick}>
                {this.props.value.toUpperCase()}
            </button>
        )
    }
}


export class Keyboard extends React.Component {
    render() {
        const layout = ['ďľščťžýáíéĺŕ', 'qwertzuiopúäň', 'asdfghjklôó', 'yxcvbnm'];
        const keysByValue = keyBy(this.props.keys, 'value');
        const enterKey = {value: 'Enter', state: null};
        const backspaceKey = {value: 'Backspace', state: null};

        const keyboard = layout.map((row) => {
            return <div className='flex flex-row justify-center space-x-2 my-2'>
                {
                    row.split('').map((value) => {
                        const key = keysByValue[value]
                        let keyComp = <Key key={key.value} value={key.value} state={key.state} onClick={() => this.props.onClick(key)}/>
                        if (value === 'y') {
                            keyComp = [<SpecialKey key={enterKey.value} value={enterKey.value}
                                       onClick={() => this.props.onClick(enterKey)}/>, keyComp]
                        } else if (value === 'm') {
                            keyComp = [keyComp, <SpecialKey key={backspaceKey.value} value='BACK'
                                       onClick={() => this.props.onClick(backspaceKey)}/>]
                        }
                        return keyComp
                    })
                }
            </div>
        })

        return (
            <div >
                {keyboard}
            </div>
        )
    }
}
