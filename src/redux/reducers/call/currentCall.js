import { createSlice } from '@reduxjs/toolkit'
import { callConstant } from '../../../util/constant'
const callStates = [
    callConstant.ANSWER,
    callConstant.INCALL,
    callConstant.HOLD,
    callConstant.UN_HOLD,
    callConstant.END,
    callConstant.HANG_UP,
    callConstant.MAKE_CALL,
    callConstant.TRANSFER
]

const currentCallSlice = createSlice({
    name: 'currentCall',
    initialState: { hasCurrentCall: false, activeCall: { sessionId: null, state: null, displayName: null, ext: null }, holdCall: { sessionId: null, state: null }, transferTo: null},
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
            if (callConstant.END === action.payload) {
                state.activeCall.ext = null
            }
            state.activeCall.state = action.payload
        },
        removeAtiveCall(state, action) {
            state.hasCurrentCall = false
            state.activeCall.sessionId = null
            state.activeCall.state = null
            state.activeCall.displayName = null
        },
        setActiveCallExtNumber(state, action) {
            state.activeCall.ext = action.payload
        },
        setTransferToExtNumber(state, action){
            state.transferTo = action.payload
        }
    }
})

export const { setCurrentCall, changeCurrentCallState, removeAtiveCall, setActiveCallExtNumber, setTransferToExtNumber } = currentCallSlice.actions

export default currentCallSlice.reducer