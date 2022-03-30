import React, {useRef, useState} from 'react';
import { Menu } from 'antd';
import styled from 'styled-components';
import { useDispatch, useSelector } from 'react-redux';
import { setCurentRoute } from '../../redux/reducers/route/route';
import { setIsWaitingListOpen, setZIndexWaitingList } from '../../redux/reducers/waitingList/waitingListStatus';
import { setIsFullScreen } from '../../redux/reducers/homePage/homePageSlice';
import imgBar from '../../asset/menu.svg'
import imgArrow from '../../asset/arrow-2.svg'
import './Sidebar.css'
import { setIsKeypadOpen, setZIndexKeyPad } from '../../redux/reducers/keypad/keypadStatus';
import { setAgentListOpen, setZIndexAgentList } from '../../redux/reducers/agentList/agentListStatus';


function Sidebar({ t }) {
    const menuRef = useRef()
    const [imgMenu, setImgMenu] = useState(imgBar)
    const dispatch = useDispatch()
    const waitingCallList = useSelector(state => state.waiting);
    const waitingListStatus = useSelector(state => state.waitingListStatus)
    const keypadStatus = useSelector(state => state.keypadStatus)
    const currentRoute = useSelector(state => state.route.currentRoute)




    const hanldeSelectPage = ({ key }) => {
        dispatch(setCurentRoute(key))

    }

    const activeSideBar = () =>{
        menuRef.current.classList.toggle('side-bar-active')

        if(menuRef.current.classList.contains('side-bar-active')){
            setImgMenu(imgArrow)
        }else{
            setImgMenu(imgBar)
        }
        
    }

    return (
        <div className='side-bar' ref={menuRef}>
            <div className='menu-bar' onClick={activeSideBar}>
                <img src={imgMenu}/>
            </div>
            <Wrapper
                mode="inline"
            >
                <li onClick={e => {
                    dispatch(setIsWaitingListOpen(true));
                    //  dispatch(setZIndexWaitingList());
                    dispatch(setIsKeypadOpen(false));
                    dispatch(setAgentListOpen(false));
                }} className={`${waitingCallList.length > 0 ? 'ant-menu-item blink_me' : 'ant-menu-item'} ${waitingListStatus.isWaitingListOpen && 'active' }`}>
                    <div className='ant-menu-title-content'>
                        <img src={require('../../asset/phone.svg').default} />
                        <span>{t('waitingList')}</span>
                    </div>

                </li>
                <li className={`ant-menu-item ${currentRoute === "incoming" ? 'active' : ''}`} onClick={() => { dispatch(setCurentRoute("incoming")) }}>
                    <div className='ant-menu-title-content'>
                        <img src={require('../../asset/talkscript.svg').default} />
                        <span>{t('taskscript')}</span>
                    </div>

                </li>
                <li className={`ant-menu-item ${keypadStatus.isKeypadOpen && 'active'}`} onClick={e => { dispatch(setIsKeypadOpen(true)); dispatch(setIsWaitingListOpen(false)) }}>
                    <div className='ant-menu-title-content'>
                        <img src={require('../../asset/Dial pad.svg').default} />
                        <span>{t('dialPad')}</span>
                    </div>
                </li>
                <li className={`ant-menu-item ${currentRoute === "setting" ? 'active' : ''}`} onClick={() => { dispatch(setCurentRoute("setting")) }}>
                    <div className='ant-menu-title-content'>
                        <img src={require('../../asset/setting.svg').default} />
                        <span>{t('setting')}</span>
                    </div>
                </li>
            </Wrapper>
        </div>
    );
};

// const SideBar = styled.div`
//     width: 100px;
//     margin-top: 20px;
//     position: fixed;
//     right: 0; 

//     @media screen and (max-width: 768px) {
//         width: 0;
//     }

//     .side-bar-active{
//         width: 100%;
//     }

//     .menu-bar{
//         position: absolute;
//         background: #547100;
//         right: 100%;
//         top: 0;
//         box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.06);
//         border-radius: 4px 0px 0px 4px;
//         padding: 9px 11px;
//         cursor: pointer;
//         display: none;
        
//         @media screen and (max-width: 768px) {
//             display: initial;
//         }
//     }
// `

const Wrapper = styled(Menu)`
    border-radius: 7px 0 0 7px;
    background: #99CC00;
    height: calc(100vh - 92px);
    border-right:none !important;

    .blink_me {
        animation: blinker 1s linear infinite;
      }
      
    @keyframes blinker {  
        50% { opacity: 0; }
    }

    .ant-menu-title-content{
        display: flex;
        align-items: center;
        justify-content: center;
        gap:0.5rem;
        text-align: center;
        flex-direction: column;
        white-space: normal;
        border-radius: 8px;
        height: 116px;
        padding: 0.5rem;
        transition: none;
        
        img{
            filter: brightness(0) saturate(100%) invert(37%) sepia(16%) saturate(3331%) hue-rotate(39deg) brightness(97%) contrast(101%);
        }
    }
    .ant-menu-item{      
        line-height: 1.5;
        height: auto;
        padding: 0px  !important;
        border-right: #99CC00 4px solid;
        border-left: #99CC00 4px solid;
        margin-top: 0 !important;

        &:first-child{
            border-radius: 7px 0 0 0 ;
        }
    }



    /* .ant-menu-item:not(:last-child){      
        padding-bottom: 4px !important;
    }
    .ant-menu-item:not(:first-child){      
        padding-top: 4px !important;
    } */
    
    .ant-menu-item.active{
        background: #7BA400;
        color: #fff;
        border-right: #222222 4px solid;
        border-left: #7BA400 4px solid;

        img{
            filter: brightness(0) saturate(100%) invert(98%) sepia(0%) saturate(87%) hue-rotate(167deg) brightness(117%) contrast(100%);
        }

        
    }


    /* .ant-menu-item:nth-child(2) .ant-menu-title-content{
        padding: 6px !important;
    } */

    .ant-menu-item:hover{
        color: #fff  !important;

        img{
            filter: brightness(0) saturate(100%) invert(98%) sepia(0%) saturate(87%) hue-rotate(167deg) brightness(117%) contrast(100%);
            
        }
    }


    .ant-menu-item-selected{
        background-color: #FFFFFF  !important;
        color: #000000 !important;
    }

    .ant-menu-item-selected::after {
        opacity: 0 !important;
    }
    
`
export default React.memo(Sidebar);