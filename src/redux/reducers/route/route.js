import { createSlice } from '@reduxjs/toolkit'

const routeSlice = createSlice({
    name: 'route',
    initialState: { currentRoute: 'main' },
    reducers: {
        setCurentRoute(state, action) {
            state.currentRoute = action.payload
        }
    }
})

export const { setCurentRoute } = routeSlice.actions

export default routeSlice.reducer