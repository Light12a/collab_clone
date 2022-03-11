import React, { useCallback, useEffect, useRef, useState } from 'react';

// import './App.less';
import './App.css'
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

  const nwaitingRef = useCallback(node => setNewWaitingWindow(node), [])
  const dispatch = useDispatch()

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
            isAgentListOpen &&
            <Draggable positionOffset={{ x: '-50%', y: '-50%' }}>
              <div className='drag agent-list'>
                <AgentList />
              </div>
            </Draggable>
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
  );
}

export default React.memo(App);