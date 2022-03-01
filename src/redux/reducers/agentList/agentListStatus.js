import { createSlice } from '@reduxjs/toolkit'

const agentListStatusSlice = createSlice({
    name: 'agentListStatus',
    initialState: { isAgentListOpen: false },
    reducers: {
        setAgentListOpen(state, action) {
            state.isAgentListOpen = action.payload
        }
    }
})

export const { setAgentListOpen } = agentListStatusSlice.actions

export default agentListStatusSlice.reducer