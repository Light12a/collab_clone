import React, { createContext, useEffect, useRef, useState } from 'react';
import Sip from 'jssip'
import { useSelector, useDispatch } from 'react-redux';



import { setConnect } from '../redux/reducers/connection/connectStatus';
import { removeAtiveCall, setCurrentCall, changeCurrentCallState, setTransferToExtNumber } from '../redux/reducers/call/currentCall';
import { pushACall, removeACall } from '../redux/reducers/waitingList/waitingCallList'
import { callConstant } from '../util/constant';

import ringtone from '../service/sounds/ringtone.wav'
import ringBackTone from '../service/sounds/ringbacktone.wav'
import { setIsWaitingListOpen } from '../redux/reducers/waitingList/waitingListStatus';

if (process.env.REACT_APP_PLATFORM === 'app') {
    var electron = window.require("electron");
}

export const SipContext = createContext(null)

const registerExpire = 120
const reRegisterTime = 5

var callOptions = {
    mediaConstraints: {
        audio: true, // only audio calls
        video: false
    }
};

const incomingCallAudio = new window.Audio(ringtone);
incomingCallAudio.loop = true;
incomingCallAudio.crossOrigin = "anonymous";

const ringBackAudio = new window.Audio(ringBackTone);
ringBackAudio.loop = true;
ringBackAudio.crossOrigin = "anonymous";

var remoteAudio = new window.Audio();
remoteAudio.autoplay = true;
remoteAudio.crossOrigin = "anonymous";

const SipProvider = ({ children }) => {
    const [ua, setUa] = useState(null)
    const { user, userConfig } = useSelector(state => state.auth)
    const { isConnected } = useSelector(state => state.networkStatus)
    const { currentState } = useSelector(state => state.connectStatus)
    const { activeCall, transferTo } = useSelector(state => state.currentCall)
    const waitingCallList = useSelector(state => state.waiting)
    const dispatch = useDispatch()
    const sessionRef = useRef([])
    const previousLengthRef = useRef()
    const [isIncomingAudioPlaying, setIsIncomingAudioPlaying] = useState(false);
    const [isRingBackAudioPlaying, setIsRingBackAudioPlaying] = useState(false);
    const { keypadNumber } = useSelector(state => state.keypadStatus)

    useEffect(() => {
        if (waitingCallList.length > 0 && !isIncomingAudioPlaying &&
            activeCall.state !== (callConstant.ANSWER && callConstant.MAKE_CALL && callConstant.HOLD && callConstant.UN_HOLD && callConstant.INCALL)) {
            incomingCallAudio.play();
            setIsIncomingAudioPlaying(true);
        }
        else {
            incomingCallAudio.pause();
            setIsIncomingAudioPlaying(false);
        }
    }, [waitingCallList])

    useEffect(() => {
        if (!ua) {
            Sip.debug.enable('JsSIP:*');
            // let socket = new Sip.WebSocketInterface(userConfig.config.pbx_domain_ws)
            let socket = new Sip.WebSocketInterface('wss://35.75.95.117:8090/ws')

            // FIXME apply config with real user
            const config = {
                uri: `sip:${userConfig.config.username}@${userConfig.config.pbx_domain}`,
                ha1: JSON.parse(localStorage.getItem('user')).ha1,
                sockets: [socket],
                register_expires: registerExpire,
                realm: 'asterisk'
            }

            console.log(config)
            setUa(new Sip.UA(config))
        }
    }, [ua, user, userConfig.config])

    // listen connect/register envent 
    useEffect(() => {
        let registerTimeOutID
        let regiserIntervalId
        if (ua && isConnected) {
            ua.start()
            ua.on('connecting', () => {
                setConnectionState('connecting')
            })
            ua.on('connected', function (e) {
                console.log('connected')
            });
            ua.on('disconnected', function (e) {
                console.log('disconected')
                setConnectionState('disconnected')
            });
            ua.on('registered', function (e) {
                console.log('registered')
                setConnectionState('connected')
                regiserIntervalId = setInterval(() => {
                    ua.register()
                }, registerExpire * 1000 / 2)
            });
            ua.on('unregistered', function (e) {
                console.log('unregistered')
                setConnectionState('disconnected')
                clearInterval(regiserIntervalId)
            });
            ua.on('registrationFailed', function (e) {
                console.log('registrationFailed')
                registerTimeOutID = setTimeout(() => {
                    ua.register()
                }, reRegisterTime * 1000)
                setConnectionState('registrationFailed')
            });
        }
        window.addEventListener('beforeunload', cleanup)
        function cleanup() {
            clearTimeout(registerTimeOutID)
            clearInterval(regiserIntervalId)
            if (ua) {
                ua.unregister()
                ua.stop()
            }
        }
        return () => {
            window.removeEventListener('beforeunload', cleanup)
            cleanup()
        }
    }, [ua, dispatch, isConnected])

    useEffect(() => {
        if (ua) {
            ua.on("newRTCSession", function (data) {
                var session = data.session;
                let intervalLogJBId = null
                console.log(session)

                sessionRef.current.push(session)


                const completeSession = () => {
                }
                session.on('progress', function () {

                    console.log('call is in progress');
                })

                session.on('sending', () => {
                    console.log('sending', session);
                    dispatch(setCurrentCall({ sessionId: session.id, state: callConstant.MAKE_CALL }))
                    if (!isRingBackAudioPlaying) {
                        ringBackAudio.play().catch(error => {
                            console.log(error)
                            //  when an exception is played, the exception flow is followed 
                        })
                        setIsRingBackAudioPlaying(true);
                    }
                })
                // incoming call here
                session.on("accepted", function () {
                    dispatch(changeCurrentCallState(callConstant.INCALL))
                    incomingCallAudio.pause();
                    setIsIncomingAudioPlaying(false);
                    // the call has answered
                });
                session.on("confirmed", function () {
                    // this handler will be called for incoming calls too
                    console.log('call confirmed');

                    ringBackAudio.pause()
                    setIsRingBackAudioPlaying(false);

                    // var localStream = session.connection.getLocalStreams()[0];
                    // var dtmfSender = session.connection.createDTMFSender(localStream.getAudioTracks()[0])
                    // session.sendDTMF = function (tone) {
                    //     dtmfSender.insertDTMF(tone);
                    // };
                    session.sendDTMF(1)



                    let rtt = 0, pcl = 0, callQuality = 0, callQualityConstrain = { 0: 'Normal', 1: 'Warning', 2: 'Abnormal' }
                    intervalLogJBId = setInterval(() => {
                        session.connection.getStats().then(data => {
                            let packetsSend = 0
                            data.forEach(item => {
                                // if (item.type.includes('inbound') || item.type.includes('outbound')) {

                                // }
                                if (item.type === 'outbound-rtp') {
                                    packetsSend = item.packetsSent
                                }
                                if (item.type === 'remote-inbound-rtp') {
                                    let rttValue = item.roundTripTime, packetLostRate = 0
                                    packetLostRate = item.packetsLost / packetsSend

                                    if (packetLostRate <= 0.05) {
                                        pcl = 0
                                    }
                                    else if (packetLostRate <= 0.1) {
                                        pcl = 1
                                    }
                                    else {
                                        pcl = 2
                                    }

                                    if (rttValue < 0.1) {
                                        rtt = 0
                                    }
                                    else if (rttValue <= 0.2) {
                                        rtt = 1
                                    }
                                    else {
                                        rtt = 2
                                    }
                                    if (pcl >= rtt) {
                                        callQuality = pcl
                                    } else {
                                        callQuality = rtt
                                    }
                                    console.log(`%ccall quality: ${callQualityConstrain[callQuality]}`, 'font-size:32px; background: #222; color: #bada55',)
                                }
                            })
                        })
                    }, 1000)
                });
                session.on("ended", function (e) {
                    // the call has ended
                    dispatch(changeCurrentCallState(callConstant.END))
                    console.log("session ended: ", session);
                    dispatch(removeACall(session.id))
                    dispatch(removeAtiveCall())
                    if (intervalLogJBId) {
                        clearInterval(intervalLogJBId)
                    }
                    // console.log('call ended with cause: ' + e.message.reason_phrase);
                    completeSession()
                });
                session.on("failed", function (e) {

                    // unable to establish the call
                    console.log("session failed: ", session);
                    dispatch(changeCurrentCallState(callConstant.END))
                    dispatch(removeAtiveCall())
                    dispatch(removeACall(session.id))
                    // console.log('call failed with cause: ' + e.message.reason_phrase);
                    completeSession()

                    ringBackAudio.pause()
                    setIsRingBackAudioPlaying(false);
                    if (waitingCallList.length === 0) {
                        incomingCallAudio.pause()
                        setIsIncomingAudioPlaying(false);
                    }
                    else if (!isIncomingAudioPlaying) {
                        incomingCallAudio.play();
                        setIsIncomingAudioPlaying(true);
                    }
                });
                // session.on('icecandidate', (data) => {
                //     console.log('candidate:', data)
                // })

                // ANCHOR force run ready to complete gather icecandidate after last candidate if this has stun candidate
                let endGatherIceId = null
                let hasStunCandidate = false
                session.on('icecandidate', ({ candidate, ready }) => {
                    if (endGatherIceId) {
                        clearTimeout(endGatherIceId)
                    }
                    if (candidate.type === 'srflx') {
                        hasStunCandidate = true
                    }
                    if (hasStunCandidate) {
                        endGatherIceId = setTimeout(() => {

                            ready()
                        }, 500)
                    }
                })

                session.on('peerconnection', (e) => {
                    console.log('peerconnection', e);
                    const peerconnection = e.peerconnection;

                    peerconnection.onicegatheringstatechange = function (e) {
                        console.log('state change')
                        console.log(peerconnection.iceGatheringState)
                    }

                    peerconnection.onicecandidateerror = function (e) {
                        console.log('candidate error')
                    }

                    peerconnection.onaddstream = function (e) {
                        console.log('addstream', e);
                        // set remote audio stream (to listen to remote audio)
                        remoteAudio.srcObject = e.stream;
                        remoteAudio.play();
                    };

                    var remoteStream = new MediaStream();
                    console.log(peerconnection.getReceivers());
                    peerconnection.getReceivers().forEach(function (receiver) {
                        console.log(receiver);
                        remoteStream.addTrack(receiver.track);
                    });
                });

                session.on("refer", function () {
                    console.log("refer: ", session);
                });

                if (session.direction === 'incoming') {
                    console.log('incoming: ', session)
                    var callInfo = {
                        ssId: session.id,
                        group_id: Math.floor(Math.random() * (12 - 9 + 1) + 9),
                        sipAddress: session._request.from._uri._scheme + ":" + session._request.from._uri._user + "@" + session._request.from._uri._host,
                        arrivedTime: new Date().toString(),
                        userName: session._request.from._uri._user,
                    };
                    dispatch(pushACall(callInfo))

                }
                else {
                    console.log('con', session.connection)
                    dispatch(setCurrentCall({ sessionId: session.id, state: callConstant.INCALL }))
                    session.connection.addEventListener('addstream', function (e) {
                        remoteAudio.srcObject = e.stream;
                    });
                }
            });
        }
    }, [ua, dispatch])

    const blindTransfer = (number, session) => {
        let eventHandlers = {
            requestSucceeded: function (e) {
                console.log("Blind transfer requestSucceeded");
            },
            requestFailed: function (e) {
                console.log("Blind transfer requestFailed");
            },
            trying: function (e) {
                console.log("Blind transfer trying");
            },
            progress: function (e) {
                console.log("Blind transfer progress");
            },
            accepted: function (e) {
                console.log("Blind transfer accepted");
                session.terminate()
                dispatch(removeAtiveCall())
            },
            failed: function (e) {
                console.log("Blind transfer failed");
            },
        };
        try {
            session.refer(number, {
                eventHandlers
            });
        } catch (err) {
            console.log("Blind transfer failed");
        }
        dispatch(setTransferToExtNumber(null));
    }

    // notification for app
    useEffect(() => {
        if (process.env.REACT_APP_PLATFORM === 'app' && previousLengthRef.current < waitingCallList.length) {
            if (waitingCallList.length === 1) {
                const NOTIFICATION_TITLE = 'INCOMMING CALL'
                const NOTIFICATION_BODY = ` Have a call from ${waitingCallList[0].skillName}. Click to answer call`
                new Notification(NOTIFICATION_TITLE, { body: NOTIFICATION_BODY })
                    .onclick = () => {
                        dispatch(setCurrentCall({ sessionId: waitingCallList[0].ssId, state: callConstant.ANSWER, displayName: waitingCallList[0].skillName }))
                        electron.ipcRenderer.send('open-app')
                    }
            }
            else if (waitingCallList.length > 1) {
                const NOTIFICATION_TITLE = 'INCOMMING CALL'
                const NOTIFICATION_BODY = `Have many calls, click to open waiting call list`
                new Notification(NOTIFICATION_TITLE, { body: NOTIFICATION_BODY })
                    .onclick = () => {
                        dispatch(setIsWaitingListOpen(true))
                        electron.ipcRenderer.send('open-app')
                    }
            }
        }
    }, [waitingCallList.length, dispatch])


    // get previoust waitingCallList length to use above
    useEffect(() => {
        previousLengthRef.current = waitingCallList.length
    }, [waitingCallList.length])

    // handle session
    useEffect(() => {

        const session = sessionRef.current.find(ss => ss.id === activeCall.sessionId)
        // if (activeCall.state === callConstant.CALL) {
        //     ua.call(keypadNumber, callOptions)

        // }
        if (!session) return
        var holdStatus = session.isOnHold();
        switch (activeCall.state) {
            case callConstant.ANSWER:
                dispatch(removeACall(activeCall.sessionId))
                session.answer(callOptions)
                break
            case callConstant.HOLD:
                if (!holdStatus.local) {
                    session.hold();
                }

                break
            case callConstant.UN_HOLD:
                if (holdStatus.local) {
                    session.unhold();
                    dispatch(changeCurrentCallState(callConstant.INCALL))
                }
                break
            case callConstant.END:
                break
            case callConstant.HANG_UP:
                session.terminate()
                dispatch(removeAtiveCall())
                break
            case callConstant.INCALL:

                break
            case callConstant.MAKE_CALL:

                break
            case callConstant.TRANSFER:
                //session.refer(keypadNumber);
                blindTransfer(transferTo, session);
                break
            default:
                return
        }
    }, [activeCall, dispatch,])

    const setConnectionState = state => {
        if (currentState === state) {
            return
        }
        dispatch(setConnect(state))
    }

    return (
        <SipContext.Provider value={ua}>

            {children}
        </SipContext.Provider>
    );
};

export default React.memo(SipProvider);