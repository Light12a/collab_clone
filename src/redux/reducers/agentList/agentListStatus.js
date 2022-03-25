import { createSlice } from '@reduxjs/toolkit'

const agentListStatusSlice = createSlice({
    name: 'agentListStatus',
    initialState: { isAgentListOpen: false, zIndexAgentList: 0, agentListType: 'CALL'},
    reducers: {
        setAgentListOpen(state, action) {
            state.isAgentListOpen = action.payload
        },
        setZIndexAgentList(state, action) {
            state.zIndexAgentList += 1
        },
        setAgentListType(state, action) {
            state.agentListType = action.payload;
        }
    }
})

export const { setAgentListOpen, setZIndexAgentList, setAgentListType } = agentListStatusSlice.actions

export default agentListStatusSlice.reducer