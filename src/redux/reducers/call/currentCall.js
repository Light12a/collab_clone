import { createSlice } from '@reduxjs/toolkit'


const END = 'END'
const INCALL = 'INCALL'
const HOLD = 'HOLD'
const UN_HOLD = 'UN_HOLD'
const ANSWER = 'ANSWER'
const CALL = 'MAKE_CALL'
const HANG_UP = 'HANG_UP'
const TRANSFER = 'TRANSFER'
const callStates = [
    ANSWER,
    INCALL,
    HOLD,
    UN_HOLD,
    END,
    HANG_UP,
    CALL,
    TRANSFER
]

export const callStatsContraint = {
    ANSWER,
    INCALL,
    HOLD,
    UN_HOLD,
    END,
    HANG_UP,
    CALL,
    TRANSFER
}

const currentCallSlice = createSlice({
    name: 'currentCall',
    initialState: { hasCurrentCall: false, activeCall: { sessionId: null, state: null, displayName: null }, holdCall: { sessionId: null, state: null } },
    reducers: {
        setCurrentCall(state, action) {

            if (!action.payload.sessionId || !callStates.includes(action.payload.state)) {
                return
            }
            state.hasCurrentCall = true
            state.activeCall.sessionId = action.payload.sessionId
            state.activeCall.displayName = action.payload.displayName
            state.activeCall.state = action.payload.state
        },
        changeCurrentCallState(state, action) {
            if (!callStates.includes(action.payload)) {
                return
            }

            state.activeCall.state = action.payload
        },
        removeAtiveCall(state, action) {
            state.hasCurrentCall = false
            state.activeCall.sessionId = null
            state.activeCall.state = null
            state.activeCall.displayName = null
        }
    }
})

export const { setCurrentCall, changeCurrentCallState, removeAtiveCall } = currentCallSlice.actions

export default currentCallSlice.reducer