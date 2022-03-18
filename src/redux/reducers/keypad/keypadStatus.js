import { createSlice } from '@reduxjs/toolkit'

const keypadStatusSlice = createSlice({
    name: 'keypadStatus',
    initialState: { isKeypadOpen: false, keypadNumber: '', zIndexKeyPad: 0},
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
        setZIndexKeyPad(state, action) {
            state.zIndexKeyPad += 1
        }
    }
})

export const { setIsKeypadOpen, setKeypadInput, resetKeypad, setZIndexKeyPad } = keypadStatusSlice.actions

export default keypadStatusSlice.reducer