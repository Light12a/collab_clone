import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { getSkillGroupAPI } from '../../../api'

export const getSkillGroups = createAsyncThunk('waiting/getSkillGroupAPI', async (token) => {
    try {
        let { data } = await getSkillGroupAPI(token)
        return data.groups
    } catch (error) {
        return Promise.reject(error)
    }

})

const waitingSlice = createSlice({
    name: 'waiting',
    initialState: {waitingList: [], skillGroupList: [], newestCall: {}, removedCall: null},
    reducers: {
        pushACall(state, action) {
            state.waitingList.push(action.payload)
            state.newestCall = action.payload;
        },
        removeACall(state, action) {
            state.removedCall = action.payload;
            if(state.waitingList){
                state.waitingList = state.waitingList.filter(item => item.ssId !== action.payload)
            }
        }
    },
    extraReducers: {
        [getSkillGroups.fulfilled]: (state, action) => {
            state.skillGroupList = action.payload
        }
    }
})

export const { pushACall, removeACall } = waitingSlice.actions

export default waitingSlice.reducer