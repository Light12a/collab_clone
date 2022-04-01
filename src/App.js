import React, { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';

import './App.less';
import './App.css'
import styled from 'styled-components';
import Signin from './features/login/Signin';
import { useDispatch, useSelector } from 'react-redux';
import MainApp from './features/MainApp';
import SipProvider from './contexts/SipProvider';
import { getUserConfig, reLogin, setLoginLoadState, setMe, signin, getUserState, setAuthFinish } from './redux/reducers/authen/auth';
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

function App() {
  const { isLoading, isAuth, token: { isHaveToken, token, isSettingToken }, userConfig: { isLoading: userConfigLoading, config } } = useSelector(state => state.auth)
  const { isWaitingListOpen } = useSelector(state => state.waitingListStatus)
  const { isAgentListOpen } = useSelector(state => state.agentListStatus)
  const { isKeypadOpen } = useSelector(state => state.keypadStatus)
  // const { isFullScreen } = useSelector(state => state.isFullScreen)
  const [newWaitingWindow, setNewWaitingWindow] = useState(null)
  const [newAgentWindow, setNewAgentWindow] = useState(null)

  // const zIndexKeyPad = useSelector(state => state.keypadStatus);
  // const zIndexWaitingList = useSelector(state => state.waitingListStatus);
  // const zIndexAgentList = useSelector(state => state.agentListStatus);

  const nwaitingRef = useCallback(node => setNewWaitingWindow(node), [])
  const nagentRef = useCallback(node => setNewAgentWindow(node), [])
  const dispatch = useDispatch()

  useLayoutEffect(() => {
    // setTimeout(function () {
      console.log('loadend')
      // your code here
      if (process.env.REACT_APP_PLATFORM === 'app') {
        require('electron').ipcRenderer.send("load-done", 'hello')

        require('electron').ipcRenderer.on('param',()=> {
          alert('sign in')
        })
      }
      
    // },3000)
  }, [])

  useEffect(() => {
    if (navigator.mediaDevices.getUserMedia !== null) {

      var options = {
        audio: true
      };
      try {

        navigator.getUserMedia(options, () => {
          console.log("Get permission for microphone and peaker success")
        }, () => {
          console.log("Get permission for microphone and peaker fail")
        })
      }
      catch (e) {
        console.log("Error: " + e)
      }
    }

  }, []);

  useEffect(() => {
    if (isSettingToken === true) {

      let tokenInStorage = localStorage.getItem('token')

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
    if (user) {
      dispatch(setMe(user))
    }
  }, [dispatch])

  useEffect(() => {
    if (isHaveToken && !isAuth && !isLoading)
      dispatch(getUserConfig(token)).then((data) => {
        if (data.meta.requestStatus === 'fulfilled') {
          dispatch(setAuthFinish())
        }
      })

  }, [isHaveToken, token, isLoading, isAuth, dispatch])

  useEffect(() => {
    if (isAuth && isHaveToken && !config)
      dispatch(getUserConfig(token))

  }, [isAuth, isHaveToken, dispatch, token, config])

  if (!isHaveToken && !isSettingToken) {
    return <Signin />
  }

  if ((isHaveToken && isLoading) || isSettingToken) return 'loading..'
  return (

    // <Wrapper>
    <div className="App">
      {isAuth && !userConfigLoading ?
        <SipProvider>
          <MainApp />
          {isWaitingListOpen && (
            process.env.REACT_APP_PLATFORM ?
              <StyleSheetManager target={newWaitingWindow}>
                <NewWindow onClose={() => {
                  dispatch(setIsWaitingListOpen(false))

                }} name='waitinglist'>
                  <WaitingList ref={nwaitingRef} />
                </NewWindow>
              </StyleSheetManager>
              :
              <Draggable positionOffset={{ x: '-50%', y: '-50%' }}>
                <div className='drag waiting-list'>
                  <WaitingList />
                </div>
              </Draggable>)
          }
          {
            isAgentListOpen && (
              process.env.REACT_APP_PLATFORM ?
                <StyleSheetManager target={newAgentWindow}>
                  <NewWindow onClose={() => {
                    dispatch(setNewAgentWindow(false))

                  }} name='agentlist'>
                    <AgentList ref={nagentRef} />
                  </NewWindow>
                </StyleSheetManager>
                :
                <Draggable positionOffset={{ x: '-50%', y: '-50%' }}>
                  <div className='drag agent-list'>
                    <AgentList />
                  </div>
                </Draggable>
            )

          }
          {isKeypadOpen &&
            <Draggable positionOffset={{ x: '-50%', y: '-50%' }}>
              <div className='drag keypad'>
                <Keypad />
              </div>
            </Draggable>
          }

        </SipProvider>
        : null}
        </div>
    // </Wrapper>
  );
}
const Wrapper = styled.div`
.drag {
    background-color: white;
    position: absolute;
    top: -50%;
    left: -50%;
    box-shadow: 0px 6px 60px rgba(0, 0, 0, 0.16);
    border-radius: 4px;
    max-height: 95vh;
    max-width: 90vw;
}

.waiting-list{
    width: 569px;
}

.agent-list{
  top: 0% !important;
    left: 10% !important;
    width: fit-content !important;   
    height: fit-content !important;
    max-height: fit-content !important;
}
.keypad{
    width: 840px;
}

.drag table{
    width: 100%;
    border-collapse: separate !important;
    border-spacing: 0;
    border-radius: 4px;
    border: 1px solid #ECECEC;
    margin-top:16px;
}
.drag .table-th{
    display: flex;
    align-items: center;
    gap:0.5rem;
}
.drag  th,td{
    /* padding: 3px; */
}
.drag th{
    background: #F6F6F6;
    border-bottom: 1px solid #ECECEC;
}
.drag tr:not(:last-child) td{
    border-bottom: 1px solid #ECECEC;
}

.drag .table-sort{
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap:1px;
    transform: translateY(1px);
    
}

.drag .table-sort img{
    cursor: pointer;
}


.formWaitingList {
    background-color: white;
    width: 45vw;
    min-width: 470px;
    position: absolute;
    top: 8.8vh;
    right: 8vw;
    box-shadow: 0px 6px 60px rgba(0, 0, 0, 0.24);
    border-radius: 4px;
}

`
export default React.memo(App);