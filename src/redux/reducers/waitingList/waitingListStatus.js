import { createSlice } from '@reduxjs/toolkit'

const waitingListStatusSlice = createSlice({
    name: 'waitingListStatus',
    initialState: { isWaitingListOpen: false },
    reducers: {
        setIsWaitingListOpen(state, action) {
            state.isWaitingListOpen = action.payload
        }
    }
})

export const { setIsWaitingListOpen } = waitingListStatusSlice.actions

export default waitingListStatusSlice.reducer