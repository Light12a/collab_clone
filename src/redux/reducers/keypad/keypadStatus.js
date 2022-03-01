import { createSlice } from '@reduxjs/toolkit'

const keypadStatusSlice = createSlice({
    name: 'keypadStatus',
    initialState: { isKeypadOpen: false, keypadNumber: ''},
    reducers: {
        setIsKeypadOpen(state, action) {
            state.isKeypadOpen = action.payload
        },
        setKeypadInput(state, action) {
            state.keypadNumber = action.payload
        },
        resetKeypad(state, action) {
            state.keypadNumber = ''
        },
    }
})

export const { setIsKeypadOpen, setKeypadInput, resetKeypad } = keypadStatusSlice.actions

export default keypadStatusSlice.reducer