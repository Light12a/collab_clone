import { createSlice } from "@reduxjs/toolkit";


const homePageSlice = createSlice({
    name: 'homePageSlice',
    initialState: { isFullScreen: false },
    reducers: {
        setIsFullScreen(state, action) {
            state.isFullScreen = action.payload
        },
    }
})

export const { setIsFullScreen } = homePageSlice.actions

export default homePageSlice.reducer