import { createSlice } from '@reduxjs/toolkit'
import { appString } from '../../../../value/string'

const languageSlice = createSlice({
    name: 'language',
    initialState: { language: localStorage.getItem(appString.languageKey) },
    reducers: {
        setLanguage(state, action) {
            state.language = action.payload
        }
    }
})

export const { setLanguage } = languageSlice.actions

export default languageSlice.reducer