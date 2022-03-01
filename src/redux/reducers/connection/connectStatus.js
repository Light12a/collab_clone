import { createSlice } from '@reduxjs/toolkit'

const connectStatusSlice = createSlice({
    name: 'connectStatus',
    initialState: { currentState: 'connecting' },
    reducers: {
        setConnect(state, action) {
            state.currentState = action.payload
        }
    }
})

export const { setConnect } = connectStatusSlice.actions

export default connectStatusSlice.reducer