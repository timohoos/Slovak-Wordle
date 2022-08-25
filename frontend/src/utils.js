export function getStateColor(state, value) {
    if (state === 'not present') {
        return 'not-present';
    } else if (state === 'wrong placement') {
        return 'incorrect';
    } else if (state === 'correct placement'){
        return 'correct';
    } else if (value && value !== null) {
        return 'not-empty';
    }
    return 'empty';
}
