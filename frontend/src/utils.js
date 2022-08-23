export function getStateColor(state) {
    if (state === 'not present') {
        return 'not-present';
    } else if (state === 'wrong placement') {
        return 'incorrect';
    } else if (state === 'correct placement'){
        return 'correct';
    }
    return 'empty';
}
