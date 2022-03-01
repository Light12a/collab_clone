import { combineReducers } from '@reduxjs/toolkit'

import auth from './authen/auth'
import connectStatus from './connection/connectStatus'
import networkStatus from './connection/networkStatus'
import route from './route/route'
import currentCall from './call/currentCall'
import waiting from './waitingList/waitingCallList'
import waitingListStatus from './waitingList/waitingListStatus'
import keypadStatus from './keypad/keypadStatus'
import agentListStatus from './agentList/agentListStatus'
import AgentList from './agentList/AgentList'
import homePageSlice from './homePage/homePageSlice'
import { logoutAPI } from '../../api'

const appReducer = combineReducers({
    auth,
    connectStatus,
    networkStatus,
    route,
    currentCall,
    waiting,
    waitingListStatus,
    keypadStatus,
    agentListStatus,
    homePageSlice,
    AgentList
})

const rootReducer = (state, action) => {
    if (action.type === 'LOGOUT') {
        logoutAPI({ token: state.auth.token.token })
        var remember = localStorage.getItem('userRemember');
        localStorage.clear()
        if(remember) {
            localStorage.setItem('userRemember',remember);
        }
        state = undefined
    }
    return appReducer(state, action)
}

export default rootReducer