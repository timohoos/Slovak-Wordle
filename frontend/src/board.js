import React from 'react';

import { getStateColor } from './utils';

class Tile extends React.Component {
    render() {
        return (
            <div className={`square ${getStateColor(this.props.state)}`}>
                {this.props.value?.toUpperCase()}
            </div>
        )
    }
}


class Word extends React.Component {
    render() {
        const word = this.props.tiles.map((tile, index) => <Tile key={index.toString()}
                                                  value={tile.value}
                                                  state={tile.state}/>);
        return (
            <div className='board-row'>
                {word}
            </div>
        )
    }
}


export class Board extends React.Component {
    render() {
        const board = this.props.words.map((word, index) => <Word key={index.toString()}
                                                                  tiles={word.tiles}/>);
        return (
            <div>
                {board}
            </div>
        )
    }
}
