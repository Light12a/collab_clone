import React, { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import styled, { css, StyleSheetManager } from 'styled-components';
import { changeCurrentCallState, setActiveCallExtNumber, setExtNumber } from '../../redux/reducers/call/currentCall';
import { callConstant } from '../../util/constant';
import closeIcon from '../../asset/Close.svg'
import callIcon from '../../asset/call.svg'
import imgCopy from '../../asset/copy.svg'

import useSip from '../../hooks/useSip';
import { setIsKeypadOpen, setKeypadInput, resetKeypad } from '../../redux/reducers/keypad/keypadStatus';

import deleteIcon from '../../asset/delete.svg'
import { message } from 'antd';
import { t } from 'i18next';
import PresenceState from '../../components/PresenceState';
const defaulKeypad = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#',]


const Keypad = (props) => {
    const ua = useSip()
    const [callNumber, setCallNumber] = useState('')
    const { userConfig } = useSelector(state => state.auth)
    const { currentState } = useSelector(state => state.connectStatus)
    const dispatch = useDispatch()
    const { agentList } = useSelector(state => state.AgentList)
    const ListAgent = agentList.agentList.users;
    const [filterNumberList, setFilterNumberList] = useState([])

    useLayoutEffect(() => {
        if (callNumber)
            setFilterNumberList(() => {
                return ListAgent.filter(item => item.ext_number.includes(callNumber))
            })
        else setFilterNumberList([])
    }, [callNumber])

    const call = () => {
        if (currentState !== 'connected') {
            message.error('not connect to PBX')
            return
        }
        if (callNumber.trim() === '') return
        dispatch(changeCurrentCallState(callConstant.MAKE_CALL))
        dispatch(setActiveCallExtNumber(callNumber))
        ua.call(callNumber, callOptions)
    }
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
        },
        // fromUserName:'sasuketamin',
        fromDisplayName: 'haizaaa',
        extraHeaders: ['uchihahaha:helo;']
    };

    useEffect(() => {
        dispatch(setKeypadInput(callNumber));
    }, [callNumber]);

    useEffect(() => {
        return () => setKeypadInput('')
    }, [])

    const handleDelete = () => {
        // setCallNumber('')
        // dispatch(resetKeypad());
        setCallNumber(currentNumber => {
            return currentNumber.slice(0, -1)
        })
    }

    const onKeypadValueChange = (number) => {
        setCallNumber(number)
    }

    const handleCall = () => {
        if (callNumber) {
            call();
            setTimeout(() => {
                dispatch(setIsKeypadOpen(false))
            }, [500])
        }
        return
    }

    const handleCopy = () => {
        navigator.clipboard.writeText(callNumber)
        message.success('coppy success')
    }

    return (
        <Wrapper>
            <div className='call-number'>
                <div className='call-number__close'>
                    <img src={closeIcon} onClick={e => { dispatch(setIsKeypadOpen(false)) }} />
                </div>
                {/* <h1 className={callNumber === '' ? 'white-blur' : 'white'} onChange={e => { onKeypadValueChange(e.target.value) }} >{callNumber === '' ? 'Phone number' : callNumber}</h1> */}
                <div className='phone-number-main'>
                    <input placeholder={t('phoneNumber')} onChange={e => { onKeypadValueChange(e.target.value) }} value={callNumber} onKeyDown={e => e.preventDefault()} />
                    {
                        callNumber && <button onClick={handleCopy}><img src={imgCopy} /></button>
                    }
                </div>

                {
                    filterNumberList.length !== 0 &&
                    <div className='filter-wrap'>
                        <div className='phone-number-filter'>
                            {
                                filterNumberList.map((item) => {
                                    let firstMatchPoint = item.ext_number.indexOf(callNumber)
                                    let lastMatchPoint = callNumber.length + firstMatchPoint
                                    console.log('f, l:', firstMatchPoint, lastMatchPoint)
                                    return <div className='filter-item' key={item.username} onClick={() => { setCallNumber(item.ext_number) }}>
                                        <span>{item.displayname}</span>
                                        <div>
                                            <span>
                                                {item.ext_number.slice(0, firstMatchPoint)}
                                            </span>
                                            <span className='highlight__ext'>
                                                {item.ext_number.slice(firstMatchPoint, lastMatchPoint)}
                                            </span>
                                            <span>
                                                {item.ext_number.slice(lastMatchPoint)}
                                            </span>
                                        </div>
                                        <div className='filter-state'>
                                            <PresenceState state={item.state} />
                                        </div>
                                    </div>
                                })
                            }
                        </div>
                    </div>
                }




            </div>

            <div className='key__number'>
                {defaulKeypad.map((item, index) =>
                    <KeyNumber content={item} key={index} number={typeof item === 'number'} setCallNumber={setCallNumber} />
                )}
                <CallButton onClick={handleCall} />
                <DeleteButton onClick={handleDelete} />

            </div>

        </Wrapper>
    );
};

const KeyNumber = ({ number, content, setCallNumber, ...rest }) => {
    const handleAddCallNumber = () => {
        setCallNumber(pre => pre.toString() + content.toString())
    }
    return <KeyNumberWrapper {...rest} onClick={handleAddCallNumber}>
        {content}
    </KeyNumberWrapper>
}
const CallButton = ({ ...rest }) => {
    return <KeyNumberWrapper {...rest} center>
        <img src={callIcon} alt='call' />
    </KeyNumberWrapper>
}

const DeleteButton = ({ ...rest }) => {

    return <KeyNumberWrapper {...rest} right>
        <img src={deleteIcon} alt='delete' />
    </KeyNumberWrapper>
}

const KeyNumberWrapper = styled.button`
    background-color: #F0F0F0;
    font-weight: 500;
    border-radius: 8px;
    outline: none;
    border: none;
    height: 48px;
    font-size: 28px;
    cursor: pointer;

    ${props => props.center ? css` 
        grid-column: 2/3;
        background-color: #99CC00;
        width: 64px;
        height: 64px;
        justify-self: center;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;

        &:active{
            background-color: #bae145;
        }

        img{
            filter: brightness(0) saturate(100%) invert(100%) sepia(54%) saturate(52%) hue-rotate(111deg) brightness(108%) contrast(101%);
            width: 27.43px;
            height: 27.43px;
        }
    `: null}

    ${props => props.right ? css` 
        grid-column: 3;
        background-color: #fff;
    `: null}
`

const Wrapper = styled.div`
    /* padding: 22px; */

    .call-number{
        background: #99CC00 linear-gradient(360deg, rgba(43, 43, 43, 0.1) 0%, rgba(43, 43, 43, 0) 100%);
        border-radius: 4px 4px 0 0;
        height: 33vh;
        display:flex ;
        flex-direction: column ;

        &__close{
            display: flex;
            flex-direction: row-reverse;
            filter: brightness(0) saturate(100%) invert(100%) sepia(54%) saturate(52%) hue-rotate(111deg) brightness(108%) contrast(101%);
            padding: 22px;

            img{
                cursor: pointer;
            }
        }

            .phone-number-main{
                display: flex;
                align-items: center;
                max-width: 400px;
                margin: 0 auto;

                input{
                    background-color: transparent;
                    border: none;
                    font-size: 48px;   
                    color: #fff;
                    outline: none;
                    width: 100%;
                    font-weight: 500;

                    &::placeholder{
                        color: rgba(255, 255, 255, 0.5);
                        font-weight: 500;
                    }
                }

                button{
                    width: 36px;
                    height: 36px;
                    border-radius: 8px;
                    background: rgba(255, 255, 255, 0.2);
                    backdrop-filter: blur(16px);
                    border: none;
                    cursor: pointer;
                    
                    img{
                        filter: brightness(0) saturate(100%) invert(100%) sepia(100%) saturate(2%) hue-rotate(234deg) brightness(106%) contrast(101%);
                    }
            }


            /* h1{
                font-size: 48px;                
            }
            .white{
                color: #ffffff;
            }
            .white-blur{
                color: rgba(255, 255, 255, 0.5);
            } */
        }
        .filter-wrap{
            background: #FBFBFB;
            overflow-y: scroll;
            height: 15vh;
            flex-grow:2 ;
            border-bottom:1px solid #ECECEC ;
            &::-webkit-scrollbar{
                width: 6px;
            }
            &::-webkit-scrollbar-track {
                background: #FBFBFB;
            }

            &::-webkit-scrollbar-thumb {
                background: #C4C4C4;
                border-radius: 100px;
            }

            /* Handle on hover */
            &::-webkit-scrollbar-thumb:hover {
                background: #555;
            }
        }
        .phone-number-filter{
           max-width: 400px;
           margin: 0 auto;
           transform: translateX(5px);
           background-color:#FBFBFB ;
            .filter-item{
                cursor: pointer;
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                padding: 12px 0;
                border-bottom: 1px solid #ECECEC;
                font-weight: 400;
                .highlight__ext {
                    color:#99CC00 ;
                }
            }
            .filter-item:hover {
                background-color: #efefef ;
            }

        }

    }

    .input__number {
        display: none;
        justify-content: center;
    }
    .key__number {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        /* grid-template-rows: repeat(5,1fr); */
        gap:16px;
        margin: 3rem auto 5rem;
        max-width: 400px;
    }
    .statusOnHoding {
    font-size: calc(0.5vw + 0.6vh);
    color: #FFB800;
    background-color: #FFF7E1;
    border: 1px solid #FFB800;
    padding: 3px 10px 3px 10px;
    border-radius: 100px;
}
.statusOnHodingInTransferredCall {
    font-size: calc(0.6vh + 0.5vw);
    color: #FFB800;
    background-color: #FFF7E1;
    border: 1px solid #FFB800;
    padding: 3px 10px 3px 10px;
    border-radius: 50px;
}
.statusAcceptable {
    font-size: calc(0.5vw + 0.6vh);
    color: #056FED;
    background-color: #E2EFFF;
    border: 1px solid #056FED;
    padding: 3px 10px 3px 10px;
    border-radius: 50px;
}

.statusIncomingCall {
    font-size: calc(0.5vw + 0.6vh);
    color: #009944;
    background-color: #E7FFF2;
    border: 1px solid #009944;
    padding: 3px 10px 3px 10px;
    border-radius: 50px;
}
.statusInACall {
    font-size: calc(0.5vw + 0.6vh);
    color: #E30000;
    background-color: #FFE1E1;
    border: 1px solid #E30000;
    padding: 3px 10px 3px 10px;
    border-radius: 50px;
}
`
export default React.memo(Keypad);