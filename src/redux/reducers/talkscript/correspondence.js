import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import {getCorrespondenceAPI} from '../../../api'

export const getCorrespondence = createAsyncThunk('correspondence/getCorrespondence', async (token) => {
    try {
        let { data } = await getCorrespondenceAPI(token)
        return data
    } catch (error) {
        console.log(error)
        return Promise.reject(error)
    }

})

const correspondenceSlice = createSlice({
    name: 'correspondence',
    initialState: { correspondenceMemo:{}},
    extraReducers: {
        [getCorrespondence.fulfilled]: (state, action) => {
            state.correspondenceMemo = action.payload
        },
    }
})


export default correspondenceSlice.reducer