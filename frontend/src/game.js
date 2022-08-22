import React from 'react';
import cloneDeep from 'lodash/cloneDeep';

import { Board } from './board';
import { Keyboard } from './keyboard';
import * as api from './api';

export class Game extends React.Component {
    constructor(props) {
        super(props);
        this.state = this.initState();
        this.timeout = null;
        this.waitingForReq = false; 
        this.keydownListener = (event) => this.handleKeyDown(event)
    }

    initState() {
        return {
            words: Array(6).fill(0).map(() => this.makeWord()),
            message: '',
            keys: 'aáäbcčdďeéfghiíjklĺľmnňoóôpqrŕsštťuúvwxyýzž'.split('').map((value) => this.makeKey(value))
        };
    }

    componentDidUpdate() {
        clearTimeout(this.timeout);
        if (this.state.message === 'Not enough letters!' || this.state.message === 'Invalid Word!') {
            this.timeout = setTimeout(() => this.setState({message:''}), 3000);
        }
    }

    async componentDidMount() {
        this.waitingForReq = true;
        api.startNewGame()
        this.waitingForReq = false;
        document.addEventListener('keydown', this.keydownListener);
    }

    componentWillUnmount() {
        document.removeEventListener('keydown', this.keydownListener);
    }

    makeKey(value) {
        return {value: value, state: null}
    }

    makeWord() {
        return {tiles: Array(5).fill(0).map(() => this.makeTile()), submitted: false};
    }

    makeTile() {
        return {value: null, state: null};
    }

    isValid(value) {
        const alphabet = 'aáäbcčdďeéfghiíjklĺľmnňoóôpqrŕsštťuúvwxyýzž'
        return alphabet.includes(value.toLowerCase())
    }

    updateState(guess, wordIndex, overallState, message) {
        let stateCopy = cloneDeep(this.state);
        for (let i = 0; i < guess.guess_state.length; i++) { //write as foreach
            stateCopy.words[wordIndex].tiles[i].state = guess.guess_state[i]
        }
        for (let i = 0; i < stateCopy.keys.length; i++) { //write as foreach
            let value = stateCopy.keys[i].value
            stateCopy.keys[i].state = overallState[value] 
        }
        stateCopy.words[wordIndex].submitted = true;

        if (message) {
            stateCopy.message = message;
        }
        this.setState(stateCopy);
    }

    updateMessage(message) {
        let stateCopy = cloneDeep(this.state);
        stateCopy.message = message;
        this.setState(stateCopy);
    }

    updateValue(value, wordIndex, tileIndex) {
        let stateCopy = cloneDeep(this.state);
        stateCopy.words[wordIndex].tiles[tileIndex].value = value;
        this.setState(stateCopy);
    }

    async handleEvent(value) {
        if (this.state.message === 'You Won!' || this.state.message === 'You Lost!' || this.waitingForReq) {
            return;
        }

        const wordIndex = this.state.words.findIndex((word) => !word.submitted);
        const tileIndex = this.state.words[wordIndex].tiles.findIndex((value) => value.value === null);

        if (value === 'Enter') {
            if (this.state.words[wordIndex].tiles[4].value === null) {
                this.updateMessage('Not enough letters!');
                return;
            }
            const guess = this.state.words[wordIndex].tiles.map((tile) => tile.value).join('');
            this.waitingForReq = true;
            const data = await api.guessWord(guess)
            this.waitingForReq = false;
            if (data.status !== 'invalid word') {
                let message;
                if (data.status === 'won') {
                    message = 'You Won!';
                } else if (data.status === 'lost') {
                    message = 'You Lost!';
                }
                this.updateState(data.game.guesses[wordIndex], wordIndex, data.game.overall_state, message);
            } else {
                this.updateMessage('Invalid Word!');
            }
        } else if (value === 'Backspace' && tileIndex !== 0) {
            const removeTileIndex = (tileIndex === -1) ? 4 : tileIndex - 1;
            this.updateValue(null, wordIndex, removeTileIndex)
            
        }else if (tileIndex !== -1 && this.isValid(value)) {
            this.updateValue(value.toLowerCase(), wordIndex, tileIndex)
        }
    }

    handleKeyDown(event) {
        this.handleEvent(event.key);
    }

    handleClick(key) {
        this.handleEvent(key.value);
    }

    handleNewGame() {
        this.setState(this.initState());
        this.timeout = null;
        this.waitingForReq = true;
        api.startNewGame();
        this.waitingForReq = false;
    }

    render() {
        return (
            <div className='game'>
                <div>
                    <Board words={this.state.words}/>
                </div>
                <div>
                    <Keyboard keys={this.state.keys} onClick={(key) => this.handleClick(key)}/>
                </div>
                <div className='message'>
                    {this.state.message}
                </div>
                {(this.state.message === 'You Won!' || this.state.message === 'You Lost!') && <div>
                <button className='rectangle' onClick={() => this.handleNewGame()}>
                    New Game
                </button>
                </div>}
            </div>
        );
    }
}
