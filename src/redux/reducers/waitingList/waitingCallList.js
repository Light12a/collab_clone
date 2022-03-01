import { createSlice } from '@reduxjs/toolkit'

const waitingSlice = createSlice({
    name: 'waiting',
    initialState: [],
    reducers: {
        pushACall(state, action) {
            // let has = false
            // state.forEach(group => {
            //     if (group.id === action.payload.groupId) {
            //         has = true
            //         group.sessionIds.push(action.payload.sessionId)
            //     }
            // })
            // if (has === false) {
            //     state.push({ name: action.payload.groupName, id: action.payload.groupId, sessionIds: [action.payload.sessionId] })
            // }
            state.push(action.payload)
        },
        removeACall(state, action) {
            // state.forEach(group => {
            //     group = group.sessionIds.filter(sessionId => {
            //         console.log('compare ', sessionId, action.payload)
            //         return sessionId !== action.payload
            //     })
            // })
            return state.filter(item => item.ssId !== action.payload)
        }
    }
})

export const { pushACall, removeACall } = waitingSlice.actions

export default waitingSlice.reducer