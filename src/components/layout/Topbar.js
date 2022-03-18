import axios from 'axios';
import React, { useRef, useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import styled from 'styled-components';
import logo from '../../asset/logo-clb.svg';
// import wifi from '../../asset/wifi.svg';
import disconnected from '../../asset/disconnected.svg';
import connected from '../../asset/connected.svg';
import connecting from '../../asset/connecting.svg';
import arrow from '../../asset/arrow.svg';
import logoutImg from "../../asset/logout.svg"
import { applyState, getAwayReasons, getUserState } from '../../redux/reducers/authen/auth'
import {Modal} from 'antd';

const Topbar = ({ t }) => {
    const dropdownActive = useRef()
    const toggleRef = useRef()
    const [ws, setWs] = useState(null);

    const { token: { token } } = useSelector(state => state.auth)
    const { user } = useSelector(state => state.auth)

    const [isModalVisible, setIsModalVisible] = useState(false);
    const { userState } = useSelector(state => state.auth)

    const [reasonID, setReasonID] = useState(null)


    const { awayReasons } = useSelector(state => state.auth)

    const CheckState = (item) => {
        switch (item) {
            case 101:
                return { state: t('acceptable'), bg: "78,107,218" }
            case 102:
                return { state: t('afterTreatment'), bg: "242, 201, 76" }
            case 100:
                return { state: t('away'), bg: "235, 87, 87" }
            default:
                return { state: t('offline'), bg: "235, 87, 87" }
        }
    }

    useEffect(() => {
        dispatch(getUserState(token))
        dispatch(getAwayReasons(token))
    }, [])
    
    useEffect(() => {
        setReasonID(userState.sub_state)
    },[userState])
    

    // useEffect(() => {
    //     const wsClient = new WebSocket('wss://18.179.96.129:8888/collabos');
    //     wsClient.onopen = () => {
    //         console.log('ws opened');
    //         setWs(wsClient);
    //       };
    //     wsClient.onclose = () => console.log('ws closed');
       
    //       return () => {
    //         wsClient.close();
    //       }
    // }, [])
    

    const { userConfig } = useSelector(state => state.auth)

    const [logOutModalVisible, setLogOutModalVisible] = useState(false)


    const userStates = [
        {
            code: 101,
            state: t('acceptable'),
            bg: "78,107,218"
        },
        {
            code: 102,
            state: t('afterTreatment'),
            bg: "242, 201, 76"
        },
        {
            code: 100,
            state: t('away'),
            bg: "235, 87, 87"
        }
    ]

    const clickOutsideRef = (contentRef, toggleRef) => {
        document.addEventListener("mousedown", (e) => {
          // user click toggle
          if (toggleRef.current && toggleRef.current.contains(e.target)) {
            contentRef.current.classList.toggle("active");
          } else {
            // user click outside toggle and content
            if (contentRef.current && !contentRef.current.contains(e.target)) {
              contentRef.current.classList.remove("active");
            }
          }
        });
    };

    useEffect(() => {
        clickOutsideRef(dropdownActive, toggleRef)
    }, [])
    

    const strConnected = t('connected');
    const strConnecting = t('connecting');
    const strDisconnected = t('disconnected');
    const states = {
        connecting: {
            text: strConnecting,
            img: connecting,
        },
        connected: {
            text: strConnected,
            img: connected
        },
        disconnected: {
            text: strDisconnected,
            img: disconnected,
        },
    }
    const { currentState } = useSelector(state => state.connectStatus)
    // const { userConfig: { config: { displayname } } } = useSelector(state => state.auth)
    const dispatch = useDispatch()
    const handleLogout = () => {
        dispatch({ type: 'LOGOUT' })
    }

    const handleSetUser = (item) => {
        dispatch(applyState({
            username: user.username,
            token: token,
            state: item.code,
            sub_state: 0
        }))

        dropdownActive.current.classList.remove('active')
    }

    const chooseAwayReason = () => {
        setIsModalVisible(true)
        dropdownActive.current.classList.remove('active')
    }

    const handleAway = () =>{

        if(!reasonID){
            return
        }

        dispatch(applyState({
            username: user.username,
            token: token,
            state: 100,
            sub_state: reasonID
        }))
        setIsModalVisible(false)
    }

    const handleCancleModal = () => {
        setIsModalVisible(false)
        setReasonID(userState.sub_state)
    }

    return (
        <Wrapper>
            <div className='topbar__group'>
                <img src={logo} className="topbar__group__logo" />
                <span>|</span>
                <div className='topbar__group__state'>
                    <img src={states[currentState].img} alt='' />
                    <span>{t('server')} {states[currentState].text}</span>
                </div>

            </div>
            <div className='topbar__group'>
                <div className='topbar__group__account'>
                    <div className='topbar__group__account__content' ref={toggleRef} 
                    >
                        <Dot bg={CheckState(userState.state).bg} />
                        <span className='name'>{userConfig.config?.displayname}</span>
                        <Text color={CheckState(userState.state).bg}>(<b>{CheckState(userState.state).state} {userState.state === 100 && ` - ${awayReasons.away_reasons?.filter(away => away.id === userState.sub_state).map(e => e.text)}`}</b>)</Text>
                        <img src={arrow} />
                    </div>

                    <div className='drop-down' ref={dropdownActive}>
                        {
                            userStates.map((item) => (
                                <div className={`drop-down-item ${userState.state === item.code && 'active'}`} onClick={() => { item.code === 100 ? chooseAwayReason() : handleSetUser(item) }}>
                                    <input type="radio" checked={userState.state === item.code ? true : false} />
                                    <span>{item.state}</span>
                                </div>
                            ))
                        }
                    </div>
                </div>
                <span>|</span>
                <div className='topbar__group__logout' onClick={() => setLogOutModalVisible(true)}>
                    <span>{t('logout')}</span>
                    <img src={logoutImg} />
                </div>

            </div>

            <Modal title="away reason" onCancel={handleCancleModal} visible={isModalVisible} onOk={handleAway} cancelButtonProps={{ style: { display: 'none' } }} okButtonProps={{ style: { borderRadius: "8px" } }}>
                <h3>Choose one reason:</h3>
                <div className='reason-body'>
                    {
                        awayReasons.away_reasons?.map((item) => (
                            <div className={`ant-modal-item ${reasonID === item.id && 'active'}`}  onClick={() => setReasonID(item.id)} >
                                <input type="radio" name='rdReason' id={item.id} checked={reasonID === item.id ? true : false }/>
                                <label for={item.id}>{item.text}</label>
                            </div>
                        ))
                    }
                </div>
            </Modal>
            <Modal
                visible={logOutModalVisible}
                title={t('logout')}
                onOk={handleLogout}
                onCancel={() => setLogOutModalVisible(false)}
                okText={t('OK')}
                cancelText={t('Cancel')}
                className="modal-logout"
            >
                {t('logOutQuestion')}
            </Modal>
        </Wrapper >
    );
};

const Wrapper = styled.div`
    height: 52px;
    padding: 0 20px;
    background-color: #FFFFFF;
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .topbar__group{
        display:flex;
        gap:1.5rem;
        align-items: center;

        &__logo{
            width:127px;
        }

        &__account{
            position: relative;

            &__content{
                display: flex;
                gap:0.5rem;
                cursor: pointer;
                align-items: center;

            }
            
            .name{
                font-weight: 700;
            }
            .drop-down{
                position: absolute;
                top:150%;
                left: 0;
                width: 100%;
                background-color: #fff;
                box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.12);
                border: 1px solid #CDCDCD;
                border-radius: 4px;
                display: none;
                cursor: pointer;
                z-index: 10;

                &-item{
                    display: flex;
                    padding: 15px 10px;
                    align-items: center;
                    gap:0.5rem;

                    &.active{
                        background-color: #F7FFE1 !important;
                        
                    }

                    &:hover{
                        background-color: #f5f5f5;
                    }

                }
            }
            .drop-down.active{
                display: initial;
            }
            
        }

        &__state{
            display: flex;
            align-items: center;
            gap:0.5rem;

            span{
                @media screen and (max-width: 768px){
                    display: none;
                }
            }
        }
        
        &__logout{
            color: #DD0000;
            font-weight: 500;
            cursor: pointer;

            span{
                margin-right: 0.5rem;
            }
        }
    }

    input[type='radio']{
        accent-color: #769d03;
    }
    
`

const Text = styled.span`
    color: ${props => `rgb(${props.color})`};
    b{
        text-transform: capitalize;
    }
`
const Dot = styled.div`
        background-color: ${props => `rgb(${props.bg})`};
        width: 10px;
        height: 10px;
        border-radius: 50%;
        box-shadow: 0 0 0 3px ${props => `rgb(${props.bg}, 0.3)`};
`

export default React.memo(Topbar);

