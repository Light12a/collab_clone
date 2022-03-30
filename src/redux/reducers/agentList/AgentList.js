import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { getUsersAPI }  from '../../../api'

export const GetAgentList = createAsyncThunk('agentList/AgentList', async (token) => {
    try {
        console.log("Token: " + token)
        let body = {
            "token": token,
            "search": "",
            "from": 0,
            "to": 20,
        }
        let { data } = await getUsersAPI(body)
        return data
    } catch (error) {
       
        return Promise.reject(error)
    }

})


const agentListSlice = createSlice({
    name: 'agentList',
    initialState: { agentList: {} },
    reducers: {
        setAgentList(state, action) {
            state.agentList = action.payload
        }
    },
    extraReducers: {
        [GetAgentList.fulfilled]: (state, action) => {
            state.agentList.agentList = action.payload
        },
    }
})

export const { setAgentList } = agentListSlice.actions

export default agentListSlice.reducer