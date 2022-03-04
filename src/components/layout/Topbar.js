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
import { Badge, Modal, Select } from 'antd';

const Topbar = ({ t }) => {
    const dropdownActive = useRef()

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
            case 103:
                return { state: "Away", bg: "235, 87, 87" }
            default:
                return { state: t('acceptable'), bg: "78, 107, 218" }
        }
    }

    useEffect(() => {
        dispatch(getUserState(token)).then(() => {console.log(userState)})
        dispatch(getAwayReasons(token))
    }, [])

    const { Option } = Select;
    const { userConfig } = useSelector(state => state.auth)

    // const [userState, setUserState] = useState(null)
    const [logOutModalVisible, setLogOutModalVisible] = useState(false)


    const userStates = [
        {
            code: 101,
            state: "Acceptable",
            bg: "78,107,218"
        },
        {
            code: 102,
            state: "After-treatment",
            bg: "242, 201, 76"
        },
        {
            code: 103,
            state: "Away",
            bg: "235, 87, 87"
        }
    ]

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
        dispatch(applyState({
            username: user.username,
            token: token,
            state: 103,
            sub_state: reasonID
        }))
        setIsModalVisible(false)
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
                    <div className='topbar__group__account__content' onClick={() => { dropdownActive.current.classList.toggle('active') }}>
                        <Dot bg={CheckState(userState.state).bg} />
                        <span className='name'>{userConfig.config?.displayname}</span>
                        <Text Text color={CheckState(userState.state).bg}>(<b>{CheckState(userState.state).state}</b>)</Text>
                        <img src={arrow} />
                    </div>

                    <div className='drop-down' ref={dropdownActive}>
                        {
                            userStates.map((item) => (
                                <div className='drop-down-item' onClick={() => { item.code === 103 ? chooseAwayReason() : handleSetUser(item) }}>
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

            <Modal title="away reason" onCancel={() => setIsModalVisible(false)} visible={isModalVisible} onOk={handleAway} cancelButtonProps={{ style: { display: 'none' } }} okButtonProps={{ style: { borderRadius: "8px" } }}>
                <h3>Choose one reason:</h3>
                <div className='reason-body'>
                    {/* {
                        awayReasons.away_reasons?.map((item) => (
                            <div className='ant-modal-item' >
                                <input type="radio" name='rdReason' id={item.id} onClick={() => setReasonID(item.id)}/>
                                <label for={item.id}>{item.text}</label>
                            </div>
                        ))
                    } */}
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

                    &:hover{
                        background-color: #F7FFE1;
                        
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
            img{
                
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