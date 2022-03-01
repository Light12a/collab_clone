import React, { useCallback, useEffect, useRef, useState } from 'react';

import './App.less';
import './App.css'
import Signin from './features/login/Signin';
import { useDispatch, useSelector } from 'react-redux';
import MainApp from './features/MainApp';
import SipProvider from './contexts/SipProvider';
import { getUserConfig, reLogin, setLoginLoadState, setMe, signin, getUserState } from './redux/reducers/authen/auth';
import { setNetwork } from './redux/reducers/connection/networkStatus';
import { setConnect } from './redux/reducers/connection/connectStatus';
import WaitingList from './features/watingList/WaitingList';
import Draggable from 'react-draggable';
import Keypad from './features/keypad/Keypad';
import AgentList from './features/agentList/AgentListScreen'
import NewWindow from './components/electron/NewWindow';
import { setIsWaitingListOpen } from './redux/reducers/waitingList/waitingListStatus';
import { setIsKeypadOpen } from './redux/reducers/keypad/keypadStatus';
import { setIsFullScreen } from './redux/reducers/homePage/homePageSlice'
import { StyleSheetManager } from 'styled-components';
import { setInitTokenSuccess, setToken } from './redux/reducers/authen/auth.js';

// const { ipcRenderer } = require('electron')
function App() {
  const { isLoading, isAuth, user, token: { isHaveToken, token, isSettingToken }, userConfig: { isLoading: userConfigLoading } } = useSelector(state => state.auth)
  const { isWaitingListOpen } = useSelector(state => state.waitingListStatus)
  const { isAgentListOpen } = useSelector(state => state.agentListStatus)
  const { isKeypadOpen } = useSelector(state => state.keypadStatus)
  // const { isFullScreen } = useSelector(state => state.isFullScreen)
  const [newWindowNode, setNewWindowNode] = useState(null)

  const nwRef = useCallback(node => setNewWindowNode(node), [])
  const dispatch = useDispatch()
  console.log('app')

  useEffect(() => {
    if (navigator.mediaDevices.getUserMedia !== null) {

      var options = {
        audio: true
      };
      try{

        navigator.getUserMedia(options, () => {
          console.log("Get permission for microphone and peaker success")
        }, () => {
          console.log("Get permission for microphone and peaker fail")
        })
      }
      catch (e){
        console.log("Error: " + e)
      }
    }

  }, []);

  console.log(isHaveToken, isSettingToken, 'hahah')

  useEffect(() => {
    if (isSettingToken === true) {

      let tokenInStorage = localStorage.getItem('token')
      console.log('hehe', typeof tokenInStorage)

      if (tokenInStorage) {
        dispatch(setToken(tokenInStorage))
      } else {
        dispatch(setInitTokenSuccess())
      }
    }
  }, [dispatch, isSettingToken])

  useEffect(() => {
    window.addEventListener('offline', () => {
      dispatch(setNetwork(false))
      dispatch(setConnect('disconnected'))
    })
    window.addEventListener('online', () => {
      dispatch(setNetwork(true))
    })
  }, [dispatch])

  useEffect(() => {
    let user = JSON.parse(localStorage.getItem('user'))
    console.log('userrrrr')
    console.log(user)
    if (user) {
      dispatch(setMe(user))
    }
  }, [dispatch])

  useEffect(() => {
    if (isHaveToken && !isAuth && !isLoading) {
      // setLoginLoadState/getMe
      dispatch(reLogin({
        tenant_id: user.tenant_id,
        username: user.username,
        token
      }))
    }
  }, [isHaveToken, token, isLoading, isAuth, dispatch])

  useEffect(() => {
    if (isAuth && isHaveToken)
      dispatch(getUserConfig(token))
      
  }, [isAuth, isHaveToken, dispatch, token])

  if (!isHaveToken && !isSettingToken) {
    console.log('!have token')
    return <Signin />
  }
  if ((isHaveToken && isLoading) || isSettingToken) return 'loading..'
  return (

    <div className="App">
      {isAuth && !userConfigLoading ?
        <SipProvider>
          <MainApp />
          {isWaitingListOpen && (
            process.env.REACT_APP_PLATFORM ?
              <NewWindow onClose={() => {
                dispatch(setIsWaitingListOpen(false))
                dispatch(setIsFullScreen(true))
                }} name='waitinglist'>
                <WaitingList />
              </NewWindow>
              :
              <Draggable onDrag={()=>{
                dispatch(setIsFullScreen(false))
                dispatch(setIsFullScreen(true))
                }}>
                <div className='drag formWaitingList'>
                  <WaitingList />
                </div>
              </Draggable>)
          }
          {
            isAgentListOpen && 
            <Draggable>
              <div className='drag agent-list'>
                <AgentList />
              </div>
            </Draggable>
          }
          {isKeypadOpen && (
            process.env.REACT_APP_PLATFORM ?
              <StyleSheetManager target={newWindowNode}>
                <NewWindow
                  onClose={() => dispatch(setIsKeypadOpen(false))}
                  name='keypad'
                >
                  <Keypad ref={nwRef} />
                </NewWindow>
              </StyleSheetManager>
              :
              <Draggable>
                <div className='drag keypad'>
                  <Keypad />
                </div>
              </Draggable>)
          }
          
        </SipProvider>
        : null}

    </div>
  );
}

export default React.memo(App);