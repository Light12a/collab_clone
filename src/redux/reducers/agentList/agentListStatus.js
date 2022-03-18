import { createSlice } from '@reduxjs/toolkit'

const agentListStatusSlice = createSlice({
    name: 'agentListStatus',
    initialState: { isAgentListOpen: false, zIndexAgentList: 0},
    reducers: {
        setAgentListOpen(state, action) {
            state.isAgentListOpen = action.payload
        },
        setZIndexAgentList(state, action) {
            state.zIndexAgentList += 1
        }
    }
})

export const { setAgentListOpen, setZIndexAgentList } = agentListStatusSlice.actions

export default agentListStatusSlice.reducer