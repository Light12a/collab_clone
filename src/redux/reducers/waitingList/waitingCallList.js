import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { getSkillGroupAPI } from '../../../api'

export const getSkillGroups = createAsyncThunk('waiting/getSkillGroupAPI', async (token) => {
    try {
        let { data } = await getSkillGroupAPI(token)
        if(data.groups){
            data.groups.push({
                "group_id": 98,
                "group_name": "Conference"
            },
                {
                    "group_id": 99,
                    "group_name": "Other"
                });
                data.groups.forEach(group => {
                group.calls = [];
            });
    
            for (let i = 0; i < 9; i++) {
                data.groups.push({
                    "group_id": 100 + i,
                    "group_name": "group " + 100 + i,
                    "calls": []
                })
            }
        }
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