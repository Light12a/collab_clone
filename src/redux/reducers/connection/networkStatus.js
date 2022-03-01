import { createSlice } from '@reduxjs/toolkit'

const networkStatusSlice = createSlice({
    name: 'networkStatus',
    initialState: { isConnected: true },
    reducers: {
        setNetwork(state, action) {
            state.isConnected = !!action.payload
        }
    }
})

export const { setNetwork } = networkStatusSlice.actions

export default networkStatusSlice.reducer