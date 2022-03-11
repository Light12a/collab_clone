import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'

import { getUserConfigAPI, loginAPI, reLoginAPI, getUserStateAPI, applyStateAPI, getAwayReasonsAPI, callAPI } from '../../../api'

export const signin = createAsyncThunk('auth/login', async (info) => {
    try {
        let { data } = await loginAPI(info.body)
        localStorage.setItem('token', data.token)
        localStorage.setItem('expire', data.token_expired)
        localStorage.setItem('user', JSON.stringify({
            ...info.body,
            password: null,
            ha1: info.ha1
        }))
        return data
    } catch (error) {
        info.setLoginError(error.response ? error.response.data.errorMessage : error.message)
        return Promise.reject(error)
    }
})

export const reLogin = createAsyncThunk('auth/reLogin', async (body, thunkAPI) => {
    try {
        let { data } = await reLoginAPI(body)
        return data
    } catch (error) {
        console.log(error)
        return thunkAPI.rejectWithValue(error)
    }
})

export const getUserConfig = createAsyncThunk('auth/getUserConfig', async (token, thunkAPI) => {
    try {
        let { data } = await getUserConfigAPI(token)
        // thunkAPI.dispatch(setAuthFinish())
        return data
    } catch (error) {
        console.log(error)
        return thunkAPI.rejectWithValue(error)

    }

})

export const getUserState = createAsyncThunk('auth/getUserState', async (token, thunkAPI) => {
    try {
        let { data } = await getUserStateAPI(token)
        return data
    } catch (error) {
        console.log(error)
        return thunkAPI.rejectWithValue(error)
    }

})

export const applyState = createAsyncThunk('auth/applyState', async (body, thunkAPI) => {
    try {
        let { data } = await applyStateAPI(body)
        return data
    } catch (error) {
        console.dir(error)
        return thunkAPI.rejectWithValue(error)
        // return Promise.reject(error)
    }
})

export const getAwayReasons = createAsyncThunk('auth/getAwayReasons', async (body, thunkAPI) => {
    try {
        let { data } = await getAwayReasonsAPI(body)
        return data
    } catch (error) {
        console.dir(error)
        return thunkAPI.rejectWithValue(error)
    }
})
export const refreshToken = createAsyncThunk('auth/refreshToken', async (oldToken, thunkAPI) => {
    try {
        let { data } = await callAPI({ method: 'post', path: '/refresh_token', body: { token: oldToken } })
        localStorage.setItem('token', data.token)
        localStorage.setItem('expire', data.token_expired)
        return data
    } catch (error) {
        alert('token refresh fail')
        return thunkAPI.rejectWithValue(error)

    }
})


const authSlice = createSlice({
    name: 'auth',
    initialState: {
        error: null, isLoading: true, isAuth: false, user: {}, userConfig: { isLoading: true, config: null }, token: {
            isHaveToken: false, token: null, isSettingToken: true
        }, userState: {}, awayReasons: {}
    },
    reducers: {
        setLoginLoadState(state, action) {
            state.isLoading = false
            state.isAuth = action.payload
        },
        setMe(state, action) {
            state.isLoading = false
            state.isAuth = false
            state.user = action.payload
        },
        setToken(state, action) {
            state.token.isHaveToken = true
            state.token.token = action.payload
            state.token.isSettingToken = false
        },
        setInitTokenSuccess(state, action) {
            state.token.isSettingToken = false
        },
        setAuthFinish(state, action) {
            state.isAuth = true
            state.isLoading = false
        }
    },
    extraReducers: {
        [signin.fulfilled]: (state, action) => {
            state.isAuth = true
            state.isLoading = false
            state.token.token = action.payload?.token
            state.token.isSettingToken = false
            state.token.isHaveToken = true

        },
        [getUserConfig.fulfilled]: (state, action) => {
            state.userConfig.config = action.payload
            state.userConfig.isLoading = false
        },
        [getUserState.fulfilled]: (state, action) => {
            state.userState = action.payload
        },
        [applyState.fulfilled]: (state, action) => {
            if(action.payload.state !== -1){
                state.userState = action.payload
            }
            
        },
        [getAwayReasons.fulfilled]: (state, action) => {
            state.awayReasons = action.payload
        },
        [reLogin.fulfilled]: (state, action) => {
            state.isAuth = true
            state.isLoading = false
        },
        [refreshToken.fulfilled]: (state, action) => {
            state.token.token = action.payload.token
            state.token.isHaveToken = true
            state.token.isSettingToken = false
        }
    }
})

export const { setLoginLoadState, setMe, setToken, setInitTokenSuccess, setUserState, setAuthFinish } = authSlice.actions

export default authSlice.reducer