import { createSlice } from '@reduxjs/toolkit'

const volumeSlice = createSlice({
    name: 'volumeSlice',
    initialState: { volume: 50 },
    reducers: {
        setVolumn(state, action) {
            state.currentState = action.payload
        }
    }
})

export const { setVolumn } = volumeSlice.actions

export default volumeSlice.reducer