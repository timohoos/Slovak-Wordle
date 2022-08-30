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
            status: 'ongoing',
            message: '',
            keys: 'aáäbcčdďeéfghiíjklĺľmnňoóôpqrŕsštťuúvwxyýzž'.split('').map((value) => this.makeKey(value))
        };
    }

    componentDidUpdate() {
        clearTimeout(this.timeout);
        if (this.state.status === 'not enough letters' || this.state.status === 'invalid word') {
            this.timeout = setTimeout(() => this.setState({status:'ongoing'}), 3000);
        }
    }

    async componentDidMount() {
        this.waitingForReq = true;
        const data = await api.getGame();
        this.waitingForReq = false;
        this.loadGame(data.game.guesses, data.game.overall_state, data.status);
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


    async getMessage(status) {
        if (status === 'won') {
            return 'Vyhral si';
        } else if (status === 'lost') {
            this.waitingForReq = true;
            const data = await api.getWord();
            this.waitingForReq = false;
            return `Prehral si, tvoje slovo bolo: ${data.word}`;
        }
        return '';
    }


    async loadGame(guesses, overallState, status) {
        let stateCopy = cloneDeep(this.state);
        guesses.forEach((guess, wordIdx) => {
            guess.guess_state.forEach((valueState, tileIdx) => {
                stateCopy.words[wordIdx].tiles[tileIdx].state = valueState
            });
            stateCopy.keys.forEach((key) => {
                key.state = overallState[key.value]
            });

            stateCopy.words[wordIdx].submitted = true;
            guess.guess.split('').forEach((value, valueIdx) => {
                stateCopy.words[wordIdx].tiles[valueIdx].value = value;
            });
        });
        stateCopy.message = await this.getMessage(status);
        stateCopy.status = status;
        this.setState(stateCopy);
    }

    updateState(guess, wordIndex, overallState, message, status) {
        let stateCopy = cloneDeep(this.state);

        guess.guess_state.forEach((valueState, tileIdx) => {
            stateCopy.words[wordIndex].tiles[tileIdx].state = valueState
        });

        stateCopy.keys.forEach((key) => {
            key.state = overallState[key.value]
        });

        stateCopy.words[wordIndex].submitted = true;

        if (message) {
            stateCopy.message = message;
        }

        if (status) {
            stateCopy.status = status;
        }

        this.setState(stateCopy);
    }

    updateMessage(message, status) {
        let stateCopy = cloneDeep(this.state);
        stateCopy.status = status;
        stateCopy.message = message;
        this.setState(stateCopy);
    }

    updateValue(value, wordIndex, tileIndex) {
        let stateCopy = cloneDeep(this.state);
        stateCopy.words[wordIndex].tiles[tileIndex].value = value;
        this.setState(stateCopy);
    }

    async handleEvent(value) {
        if (this.state.status === 'won' || this.state.status === 'lost' || this.waitingForReq) {
            return;
        }


        const wordIndex = this.state.words.findIndex((word) => !word.submitted);
        const tileIndex = this.state.words[wordIndex].tiles.findIndex((value) => value.value === null);

        if (value === 'Enter') {
            if (this.state.words[wordIndex].tiles[4].value === null) {
                this.updateMessage('Nedostatok písmen', 'not enough letters');
                return;
            }
            const guess = this.state.words[wordIndex].tiles.map((tile) => tile.value).join('');
            this.waitingForReq = true;
            const data = await api.guessWord(guess)
            console.log(data);
            this.waitingForReq = false;
            if (data.status !== 'invalid word') {
                const message = await this.getMessage(data.status);
                this.updateState(data.game.guesses[wordIndex], wordIndex, data.game.overall_state, message, data.status);
            } else {
                this.updateMessage('Neplatné slovo', data.status);
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
            <div className='flex flex-col justify-between h-screen'>
                <div className='w-full text-center py-3 border-b-2 border-gray-300'>
                    <h1 className='text-3xl font-bold'>Slovo dňa</h1>
                    {this.state.status !== 'ongoing' &&
                    <div className='absolute top-[4.5rem] left-1/2 transform -translate-x-1/2 z-10'>
                        <p className='text-white text-xl bg-gray-700 text-center px-2 py-2 rounded-md'>
                            {this.state.message}
                        </p>
                    </div>}
                </div>
                <div className='relative z-0'>
                    <Board words={this.state.words}/>
                    {(this.state.status === 'won' || this.state.status === 'lost') &&
                    <div className='absolute bottom-[-6rem] left-1/2 transform -translate-x-1/2'>
                        <button className='text-2xl text-center text-white bg-gray-700 w-36 h-16 rounded' onClick={() => this.handleNewGame()}>
                            Nová hra
                        </button>
                    </div>}
                </div>
                <div>
                    <Keyboard keys={this.state.keys} onClick={(key) => this.handleClick(key)}/>
                </div>
            </div>
        );
    }
}
