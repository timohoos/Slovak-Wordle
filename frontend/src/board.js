import React from 'react';

import { getStateColor } from './utils';

class Tile extends React.Component {
    render() {
        return (
            <div className={`p-2 text-4xl font-semibold text-center leading-none basis-1/5 tile ${getStateColor(this.props.state, this.props.value)}`}>
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
            <div className='w-full h-[3.5rem] flex flex-row space-x-2'>
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
            <div className='w-[20rem] flex flex-col space-y-2 mx-auto'>
                {board}
            </div>
        )
    }
}
