import React, { useEffect, useRef, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Badge, Select, message } from 'antd';
import styled from 'styled-components';
import { setAgentListOpen } from "../../redux/reducers/agentList/agentListStatus";
import { callStatsContraint, removeAtiveCall, setCurrentCall, changeCurrentCallState } from '../../redux/reducers/call/currentCall';
import useSip from '../../hooks/useSip';
import { useTranslation } from 'react-i18next';
import { setIsWaitingListOpen } from '../../redux/reducers/waitingList/waitingListStatus';
import bgImage from '../../asset/background.svg'
import arrowIcon from '../../asset/ic.svg'
import dialpad from '../../asset/dialpad.svg'
import { setIsKeypadOpen } from '../../redux/reducers/keypad/keypadStatus';
import imgCopy from '../../asset/copy.svg'
import imgDot from '../../asset/dot.svg'
import endCallImg from '../../asset/end_call.svg'
import checkImg from '../../asset/check.svg'
import transferImg from '../../asset/transfer.svg'
import pauseImg from '../../asset/pause.svg'
import copyImg from '../../asset/copy.svg'
import playImg from '../../asset/play.svg'

const log = require('electron-log');

const HomePage = () => {
    const ua = useSip()
    const dispatch = useDispatch();
    const { currentState } = useSelector(state => state.connectStatus)
    const { isWaitingListOpen } = useSelector(state => state.waitingListStatus)
    const { activeCall, hasCurrentCall } = useSelector(state => state.currentCall);
    const { keypadNumber } = useSelector(state => state.keypadStatus)
    const { isFullScreen } = useSelector(state => state.homePageSlice)
    const currentRoute = useSelector(state => state.route.currentRoute)
    const { Option } = Select;
    const { t } = useTranslation();
    const [callStatus, setCallStatus] = useState({
        color: '',
        text: ''
    });

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
    log.info("HomePage.js callStatus: " + JSON.stringify(callStatus));

    useEffect(() => {
        switch (activeCall.state) {
            case callStatsContraint.ANSWER:
                setCallStatus({
                    color: 'blue',
                    text: 'In call'
                })
                break
            case callStatsContraint.HOLD:
                setCallStatus({
                    color: 'yellow',
                    text: 'On hold'
                })
                break
            case callStatsContraint.UN_HOLD:
                setCallStatus({
                    color: 'blue',
                    text: 'In call'
                })
                break
            case callStatsContraint.END:
                setCallStatus({
                    color: '',
                    text: ''
                })
                break
            case callStatsContraint.HANG_UP:
                setCallStatus({
                    color: '',
                    text: ''
                })
                break
            case callStatsContraint.INCALL:
                setCallStatus({
                    color: 'blue',
                    text: 'In call'
                })
                break
            case callStatsContraint.CALL:
                setCallStatus({
                    color: 'green',
                    text: 'Calling...'
                })
                break
            default:
                return
        }
    }, [activeCall]);

    const endCall = () => {
        dispatch(changeCurrentCallState(callStatsContraint.HANG_UP))
    }

    const call = () => {
        if (keypadNumber.trim() === '') return
        dispatch(changeCurrentCallState(callStatsContraint.CALL))
        ua.call(keypadNumber, callOptions)
    }

    const hold = () => {
        if (activeCall.state === callStatsContraint.HOLD) {
            dispatch(changeCurrentCallState(callStatsContraint.UN_HOLD))
        }
        else {
            dispatch(changeCurrentCallState(callStatsContraint.HOLD))
        }
    }

    const forward = () => {
        dispatch(changeCurrentCallState(callStatsContraint.TRANSFER))
    }

    const location = window.location.href.split('?');
    useEffect(() => {
        if (location[1]) {
            //  keypadNumber = location[1].split("=")[1]

            const timer = setTimeout(() => {
                message.error("Can't make call because lost register!");
            }, 5000);

            // alert(location[1].split("=")[1])
            if (currentState == 'connected') {

                // console.log('Timeout clear!');
                dispatch(changeCurrentCallState(callStatsContraint.CALL))
                // ua.call(location[1].split("=")[1], callOptions)
                clearTimeout(timer)
                return () => clearTimeout(timer);
            }
            return () => clearTimeout(timer);
            // console.log(currentState + ";;;;hien thi")
        }
    }, [currentState])

    const copyToClipboard = (text) => {
        navigator.clipboard.writeText(text)
        message.success('copy to clipboard')
    }

    return (
        <Wrapper>
            <div className={(isWaitingListOpen && !isFullScreen) ? 'haflHomepage' : 'homepage'}>
                <div className='homepage__top'>
                    <p>{t('yourNotiNumber')}<span>*</span></p>
                    <div className='homepage__top__group'>
                        <Select style={{ width: '376px' }} defaultValue={'123-444-444'} suffixIcon={<img src={arrowIcon} />}>
                            <Option value="123-444-444">123-444-444</Option>
                            <Option value="123-555-555">123-555-555</Option>
                        </Select>
                        <button onClick={e => { dispatch(setIsKeypadOpen(true)) }}><img src={dialpad} alt="" />{t("dialPad")}</button>
                    </div>

                </div>
                <div className={`homepage__monitor ${currentRoute !== 'main' ? 'half' : ''}`} style={{ backgroundImage: `url(${bgImage})`, backgroundRepeat: 'no-repeat', backgroundSize: 'cover' }}>
                    <Badge color={callStatus.color} dot text={callStatus.text} />
                    <span style={{ fontSize: '36px' }}>{(activeCall.displayName && activeCall.displayName.length) > 0 ? activeCall.displayName : ''} {/*<span style={{ fontSize: '16px' }}>Copy</span>*/}</span>

                    {/* UI Coaching active */}

                    {/* <div className='coaching'>
                        <div className='coaching__item'>
                            <h1>Charlie Press</h1>
                            <div className='coaching__item__number'>
                                <span>123-345-668</span>
                                <button><img src={imgCopy} /></button>
                            </div>
                        </div>
                        <div className='coaching__descript'>
                            <img src={imgDot} />
                            <p>In a call</p>
                        </div>
                        <div className='coaching__item'>
                            <h1>Unknown</h1>
                            <div className='coaching__item__number'>
                                <span>123-345-668</span>
                                <button><img src={imgCopy} /></button>
                            </div>
                        </div>
                    </div> */}



                    {/* UI coaching passive */}
                    {/* <div className='coaching-passive'>
                        <div className='coaching-passive__item'>
                            <div className='coaching-passive__item__header'>
                                <Dot bg="#21F777" />
                                <span>Coaching</span>
                            </div>
                            <div className='coaching-passive__item__body'>
                                <h1>Charlie Press</h1>
                                <p>123-345-669</p>
                            </div>
                        </div>
                        <div className='coaching-passive__item'>
                            <div className='coaching-passive__item__header'>
                                <Dot bg="#FF9900" />
                                <span>On hold</span>
                            </div>
                            <div className='coaching-passive__item__body'>
                                <h1>Unknown</h1>
                                <p>123-345-669</p>
                            </div>
                        </div>
                    </div> */}
                    <div>

                    </div>
                    {hasCurrentCall &&
                        <> <div className='homepage__monitor__info'>
                            <Badge color={callStatus.color} dot text={callStatus.text} style={{ color: 'white' }} />
                            <span className='display__name'>{(activeCall.displayName && activeCall.displayName.length) > 0 ? activeCall.displayName : ''} {/*<span style={{ fontSize: '16px' }}>Copy</span>*/}</span>

                            <span className='display__name'>{'UNKNOW'}</span>
                            <div className='extension__number'>
                                <span>123-123-113</span>
                                <div className='copy__btn' onClick={() => copyToClipboard('123')}>
                                    <img src={copyImg} alt='copy' />
                                </div>
                            </div>
                        </div>
                            <div className='homepage__monitor__action'>
                                {activeCall.state === callStatsContraint.HOLD
                                    ? <HomePageIcon icon={playImg} color='white' text={t('realeseHold')} size={48} onClick={hold} />
                                    : <HomePageIcon icon={pauseImg} color='white' text={t('holdOn')} size={48} onClick={hold} />}
                                <HomePageIcon icon={endCallImg} color='#FF223C' text={t('disconect')} onClick={endCall} />
                                <HomePageIcon icon={transferImg} color='white' text={t('transfer')} size={48} onClick={forward} />

                            </div>
                        </>}
                </div>


                <div className='homepage__btn-group'>
                    {/* <button onClick={e => { hasCurrentCall ? endCall() : call() }} className='btn'>{hasCurrentCall ? t('disconnect') : t('call')}</button> */}
                    {/* <button className='btn' onClick={e => hold()}>{activeCall.state === callStatsContraint.HOLD ? t('unHold') : t('holdOn')}</button>
                    <button className='btn' onClick={e => forward()}>{t('forward')}</button> */}
                    <button className='btn' onClick={e => { dispatch(setAgentListOpen(true)) }}>{t('call')}</button>
                    <button className='btn'>{t('pickUp')}</button>
                    <button className='btn'>{t('conference')}</button>
                    <button className='btn'>{t('coach')}</button>
                    <button className='btn'>{t('monitor')}</button>
                </div>
            </div>
        </Wrapper>

    );
};

const HomePageIcon = ({ icon, color, size, attachIcon, text, ...rest }) => {
    return <HomepageIconWrapper color={color} size={size} {...rest}>
        <div className='homepage__icon__top'>
            <img src={icon} alt='logo' />
            {attachIcon &&
                <div className='attach__icon'>
                    <img src={attachIcon} alt='attach icon' />
                </div>}
        </div>
        <div className='homepage__icon__bottom'>
            <span>{text}</span>

        </div>
    </HomepageIconWrapper>
}
const HomepageIconWrapper = styled.div`
    height: ${props => props.size === 64 || !props.size ? '120%' : '100%'};
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-direction: column;
    width:${props => props.size ? props.size : 64}px;
    user-select: none;
    .homepage__icon__top {
        cursor: pointer;
        width:100%;
        height:${props => props.size ? props.size : 64}px;
        border-radius: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color:${props => props.color};
        position: relative;
    }
    .homepage__icon__top:active {
        opacity: .6;
    }
    .homepage__icon__bottom {
        width: max-content;
    }
    .attach__icon {
        position: absolute;
        width: 21px;
        height: 21px;
        bottom: 0;
        right: 0;
        background: #99CC00;
        border-radius: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
`

const Wrapper = styled.div`
    width:50%;
    font-size: 14px;
    padding: 20px;
    height: calc(100vh - 52px);
    flex: 1;
    

    .homepage{
        height: 100%;
        background: #FFFFFF;
        padding: 16px;
        border-radius: 4px;
        display: flex;
        flex-direction: column;
        gap:16px;
        

        &__top{
            p{
                font-weight: 500;
                color: #555555;
                span{
                    color: #EE0000;
                }
            }
            &__group{
                display: flex;
                justify-content: space-between;

                button{
                    background-color: #99CC00;
                    width: 140px;
                    border: none;
                    border-radius: 8px;
                    font-weight: 700;
                    color: #FFFFFF;
                    cursor: pointer;

                    img{
                        margin-right: 0.5rem;
                    }

                    &:active{
                        background-color: #bae145;
                    }

                }
            }

        }
        

        &__monitor{
            /* background-color: #808080; */
            padding: 24px;
            width: 100%;
            height: 100%;
            border-radius: 4px;
            background: linear-gradient(360deg, rgba(43, 43, 43, 0.1) 0%, rgba(43, 43, 43, 0) 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
            justify-content: space-between;
            &__info {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                color: #FFFFFF;
                .ant-badge-status-dot {
                    width: 16px;
                    height: 16px;
                }
                .display__name {
                    font-weight: 500;
                    font-size: 48px;
                }
                .extension__number{
                    font-size: 24px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    gap: 16px;
                    font-weight: 400;
                }
                .copy__btn {
                    cursor: pointer;
                    width: 36px;
                    height: 36px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background: rgba(255, 255, 255, 0.14);
                    backdrop-filter: blur(12px);
                    /* Note: backdrop-filter has minimal browser support */

                    border-radius: 8px;
                }
            }
            &__action {
                display: flex;
                justify-content: center;
                align-items: flex-end;
                gap: 48px;
            }
        }

        &__btn-group{
            display: flex;
            justify-content: center;
            align-items: center;
            gap:1rem;
        }
    }

    .haflHomepage {
        height: 100%;
        background: #FFFFFF;
        padding: 16px;
        border-radius: 4px;
        display: flex;
        flex-direction: column;
        gap:16px;
        min-width: 470px;
        width: 45vw;
    }
    .btn {
        background-color: #99CC00;
        color: #FFFFFF;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 10px;
        width: 160px;
        cursor: pointer;

        &:active{
            background-color: #bae145;
        }
    }



    .coaching{
        display: flex;
        align-items: center;
        gap:1.5vw;

        &__item{
            padding: 2.5vw;
            width: 20vw;
            background: rgba(255, 255, 255, 0.14);
            box-shadow: 0px 6px 60px rgba(5, 13, 7, 0.2);
            border-radius: 40px;
            backdrop-filter: blur(30px);
            text-align: center;
            min-width: 15rem;
            
            h1, span{
                color: #FFFFFF;
                white-space: nowrap;
            }
            h1{
                font-weight: 700;
                font-size: 32px;
                margin-bottom: 1rem;
               
            }
            span{
                font-size: 24px;
                font-weight: 400;
                
            }

            &__number{
                display: flex;
                align-items: center;
                justify-content: center;
                gap:1rem;

                button{
                    width: 36px;
                    height: 36px;
                    background: rgba(255, 255, 255, 0.2);
                    backdrop-filter: blur(16px);
                    border-radius: 8px;
                    border: none;
                    cursor: pointer;

                    &:active{
                        background-color: #bae145;
                    }
                }
            }
        }
        &__descript{
                p{
                    color: #0084FF;
                }
        }
    }

    .half{
        .coaching__item{
            width: 15vw;
            padding: 1vw;
        }
    }

    .coaching-passive{
        position: absolute;
        right: 0;
        top: 0;
        padding: 1rem;

        &__item{
            background: rgba(255, 255, 255, 0.3);
            border: 2px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0px 4px 30px rgba(5, 13, 7, 0.16);
            box-shadow: 0px 4px 30px rgba(5, 13, 7, 0.16);
            border-radius: 24px;
            margin-bottom: 1rem;

            &__header{
                display: flex;
                justify-content: center;
                align-items: center;
                gap:0.5rem;
                color:#FFFFFF;
                padding: 10px;
                background: rgba(0, 0, 0, 0.25);
                border-radius: 24px 24px 0 0;
                width: 197px;
            }

            &__body{
                text-align: center;

                h1, p{
                    color: #FFFFFF;
                }
                h1{
                    margin-bottom: 2px;
                }
                p{
                    margin-bottom: 10px;
                }
            }
        }
    }
`



const Dot = styled.div`
    width: 16px;
    height: 16px;
    background-color: ${props => props.bg};
    border-radius: 50%;
`

export default React.memo(HomePage);