import React, { createContext, useEffect, useRef, useState } from 'react';
import Sip from 'jssip'
import { useSelector, useDispatch } from 'react-redux';



import { setConnect } from '../redux/reducers/connection/connectStatus';
import { callStatsContraint, removeAtiveCall, setCurrentCall, changeCurrentCallState } from '../redux/reducers/call/currentCall';
import { pushACall, removeACall } from '../redux/reducers/waitingList/waitingCallList'

import ringtone from '../service/sounds/ringtone.wav'
import ringBackTone from '../service/sounds/ringbacktone.wav'
import { setIsWaitingListOpen } from '../redux/reducers/waitingList/waitingListStatus';

if (process.env.REACT_APP_PLATFORM === 'app') {
    var electron = window.require("electron");
}
console.log(process.env.REACT_APP_PLATFORM, typeof process.env.REACT_APP_PLATFORM, process.env.REACT_APP_PLATFORM === 'app')

export const SipContext = createContext(null)

const registerExpire = 120
const reregisterTime = 5

var callOptions = {
    mediaConstraints: {
        audio: true, // only audio calls
        video: false
    },
    pcConfig: {
        iceServers: [{
            urls: ["stun:stun.l.google.com:19302"]
        }],
        // iceTransportPolicy: 'relay',
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
    const { activeCall } = useSelector(state => state.currentCall)
    const waitingCallList = useSelector(state => state.waiting)
    const dispatch = useDispatch()
    const sessionRef = useRef([])
    const previousLengthRef = useRef()
    const [isIncomingAudioPlaying, setIsIncomingAudioPlaying] = useState(false);
    const [isRingBackAudioPlaying, setIsRingBackAudioPlaying] = useState(false);
    const { keypadNumber } = useSelector(state => state.keypadStatus)

    useEffect(() => {
        if (waitingCallList.length > 0 && !isIncomingAudioPlaying &&
            activeCall.state !== (callStatsContraint.ANSWER && callStatsContraint.CALL && callStatsContraint.HOLD && callStatsContraint.UN_HOLD && callStatsContraint.INCALL)) {
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
            console.log(userConfig)
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
    }, [ua, user, userConfig])

    // listen connect/register envent 
    useEffect(() => {
        let registerTimeOutID
        let regiserIntervalId
        console.log('ua start')
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
                console.log('registered,', e)
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
                }, reregisterTime * 1000)
                setConnectionState('disconnected')
            });
        }
        return () => {
            clearTimeout(registerTimeOutID)
            clearInterval(regiserIntervalId)
            if (ua) {
                ua.stop()
            }
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
                    dispatch(setCurrentCall({ sessionId: session.id, state: callStatsContraint.CALL }))
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
                    dispatch(changeCurrentCallState(callStatsContraint.INCALL))
                    incomingCallAudio.pause();
                    setIsIncomingAudioPlaying(false);
                    // the call has answered
                });
                session.on("confirmed", function () {
                    // this handler will be called for incoming calls too
                    console.log('call confirmed');

                    ringBackAudio.pause()
                    setIsRingBackAudioPlaying(false);

                    var localStream = session.connection.getLocalStreams()[0];
                    var dtmfSender = session.connection.createDTMFSender(localStream.getAudioTracks()[0])
                    session.sendDTMF = function (tone) {
                        dtmfSender.insertDTMF(tone);
                    };

                    let rtt = 0, pcl = 0, callQuality = 0, callQualityConstrain = { 0: 'Normal', 1: 'Warning', 2: 'Abnormal' }
                    intervalLogJBId = setInterval(() => {
                        session.connection.getStats().then(data => {
                            let packetsSend = 0
                            data.forEach(item => {
                                if (item.type.includes('inbound') || item.type.includes('outbound')) {
                                    // // log local-remote jb
                                    // console.log(item)
                                }
                                if (item.type === 'outbound-rtp') {
                                    packetsSend = item.packetsSent
                                    console.log('packetsSend', packetsSend)
                                }
                                if (item.type === 'remote-inbound-rtp') {
                                    let rttValue = item.roundTripTime, packetLostRate = 0
                                    packetLostRate = item.packetsLost / packetsSend
                                    console.log('lossRate', item.packetsLost, packetsSend, item.packetsReceived)
                                    if (packetLostRate <= 0.05) {
                                        pcl = 0
                                    }
                                    else if (packetLostRate <= 0.1) {
                                        pcl = 1
                                    }
                                    else {
                                        pcl = 2
                                    }
                                    console.log('pclValue ', typeof packetLostRate, packetLostRate)

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
                    dispatch(changeCurrentCallState(callStatsContraint.END))
                    dispatch(removeACall(session.ssId))
                    dispatch(removeAtiveCall())
                    if (intervalLogJBId) {
                        clearInterval(intervalLogJBId)
                    }
                    // console.log('call ended with cause: ' + e.message.reason_phrase);
                    completeSession()
                });
                session.on("failed", function (e) {

                    // unable to establish the call
                    dispatch(changeCurrentCallState(callStatsContraint.END))
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
                session.on('icecandidate', (data) => {
                    console.log('candidate:', data)
                })

                // ANCHOR force run ready to complete gather icecandidate after last candidate if this has stun candidate
                let endGatherIceId = null
                let hasStunCandidate = false
                session.on('icecandidate', ({ candidate, ready }) => {
                    console.log('icecandidate', candidate)
                    if (endGatherIceId) {
                        clearTimeout(endGatherIceId)
                    }
                    if (candidate.type === 'srflx') {
                        hasStunCandidate = true
                    }
                    if (hasStunCandidate) {
                        endGatherIceId = setTimeout(() => {
                            console.log('timeout')
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
                        skillName: session._request.from._uri._user,
                        calls: [
                            {
                                sipAddress: session._request.from._uri._scheme + ":" + session._request.from._uri._user + "@" + session._request.from._uri._host,
                                optional: 'optional',
                                arrivedTime: new Date(),
                                ssId: session.id
                            }
                        ],
                        waitingTime: "00:00",
                        waitingCall: 0,
                        waitingTimeMilisecond: 0,
                    };
                    dispatch(pushACall(callInfo))

                }
                else {
                    console.log('con', session.connection)
                    dispatch(setCurrentCall({ sessionId: session.id, state: callStatsContraint.INCALL }))
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
    }

    // notification for app
    useEffect(() => {
        if (process.env.REACT_APP_PLATFORM === 'app' && previousLengthRef.current < waitingCallList.length) {
            if (waitingCallList.length === 1) {
                const NOTIFICATION_TITLE = 'INCOMMING CALL'
                const NOTIFICATION_BODY = ` Have a call from ${waitingCallList[0].skillName}. Click to answer call`
                new Notification(NOTIFICATION_TITLE, { body: NOTIFICATION_BODY })
                    .onclick = () => {
                        dispatch(setCurrentCall({ sessionId: waitingCallList[0].ssId, state: callStatsContraint.ANSWER, displayName: waitingCallList[0].skillName }))
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
        // if (activeCall.state === callStatsContraint.CALL) {
        //     ua.call(keypadNumber, callOptions)

        // }
        if (!session) return
        var holdStatus = session.isOnHold();
        switch (activeCall.state) {
            case callStatsContraint.ANSWER:
                dispatch(removeACall(activeCall.sessionId))
                session.answer(callOptions)
                break
            case callStatsContraint.HOLD:
                if (!holdStatus.local) {
                    session.hold();
                }

                break
            case callStatsContraint.UN_HOLD:
                if (holdStatus.local) {
                    session.unhold();
                }
                break
            case callStatsContraint.END:
                break
            case callStatsContraint.HANG_UP:
                session.terminate()
                dispatch(removeAtiveCall())
                break
            case callStatsContraint.INCALL:

                break
            case callStatsContraint.CALL:

                break
            case callStatsContraint.TRANSFER:
                //session.refer(keypadNumber);
                blindTransfer(keypadNumber, session);
                break
            default:
                return
        }
    }, [activeCall, dispatch,])

    const setConnectionState = state => {
        if (currentState === state) {
            console.log('samee')
            return
        }
        console.log('notsamee')
        dispatch(setConnect(state))
    }

    return (
        <SipContext.Provider value={ua}>

            {children}
        </SipContext.Provider>
    );
};

export default React.memo(SipProvider);