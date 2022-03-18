import { createSlice } from '@reduxjs/toolkit'

const waitingListStatusSlice = createSlice({
    name: 'waitingListStatus',
    initialState: { isWaitingListOpen: false, zIndexWaitingList: 0 },
    reducers: {
        setIsWaitingListOpen(state, action) {
            state.isWaitingListOpen = action.payload
        },
        setZIndexWaitingList(state, action) {
            state.zIndexWaitingList += 1
        }
    }
})

export const { setIsWaitingListOpen, setZIndexWaitingList } = waitingListStatusSlice.actions

export default waitingListStatusSlice.reducer