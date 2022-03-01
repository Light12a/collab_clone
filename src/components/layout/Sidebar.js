import React from 'react';
import { Menu } from 'antd';
import { AppstoreOutlined, MailOutlined, SettingOutlined } from '@ant-design/icons';
import styled from 'styled-components';
import logo from '../../asset/logo-clb.svg'
import { useDispatch, useSelector } from 'react-redux';
import { setCurentRoute } from '../../redux/reducers/route/route';
import { setIsWaitingListOpen } from '../../redux/reducers/waitingList/waitingListStatus';
import { setIsKeypadOpen } from '../../redux/reducers/keypad/keypadStatus';
import { setAgentListOpen } from '../../redux/reducers/agentList/agentListStatus';
import { setIsFullScreen } from '../../redux/reducers/homePage/homePageSlice';

const rootSubmenuKeys = ['sub1', 'sub2', 'sub4'];

function Sidebar({ t }) {

    const dispatch = useDispatch()
    const waitingCallList = useSelector(state => state.waiting);
    const waitingListStatus = useSelector(state => state.waitingListStatus)
    const currentRoute = useSelector(state => state.route.currentRoute)



    const hanldeSelectPage = ({ key }) => {
        dispatch(setCurentRoute(key))

    }

    console.log(currentRoute)

    return (
        <SideBar>
            <Wrapper
                mode="inline"
            >
                <li onClick={e => {
                    dispatch(setIsWaitingListOpen(true));
                    dispatch(setIsFullScreen(false))
                }} className={`${waitingCallList.length > 0 ? 'ant-menu-item blink_me' : 'ant-menu-item'} ${waitingListStatus.isWaitingListOpen ? 'active' : ''}`}>
                    <div className='ant-menu-title-content'>
                        <img src={require('../../asset/phone.svg').default} />
                        <span>{t('waitingList')}</span>
                    </div>

                </li>
                {/* <li className='ant-menu-item'>
                    <div className='ant-menu-title-content'>
                        <img src={require('../../asset/phone.svg').default} />
                        <span>{t('conferenceList')}</span>
                    </div>

                </li> */}
                <li className={`ant-menu-item ${currentRoute === "incoming" ? 'active' : ''}`} onClick={() => { dispatch(setCurentRoute("incoming")) }}>
                    <div className='ant-menu-title-content'>
                        <img src={require('../../asset/talkscript.svg').default} />
                        <span>{t('taskscript')}</span>
                    </div>

                </li>
                <li className={`ant-menu-item ${currentRoute === "setting" ? 'active' : ''}`} onClick={() => { dispatch(setCurentRoute("setting")) }}>
                    <div className='ant-menu-title-content'>
                        <img src={require('../../asset/setting.svg').default} />
                        <span>{t('setting')}</span>
                    </div>
                </li>
            </Wrapper>
        </SideBar>
    );
};

const SideBar = styled.div`
    width: 100px;
    margin-top: 20px;
    position: fixed;
    right: 0;
`

const Wrapper = styled(Menu)`
    border-radius: 4px 0 0 4px;
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
        
    }
    .ant-menu-item{      
        line-height: 1.5;
        height: auto;
        padding: 8px  !important;
        margin: 0 !important;
        border-radius: 8px;
    }



    .ant-menu-item:not(:last-child){      
        padding-bottom: 4px !important;
    }
    .ant-menu-item:not(:first-child){      
        padding-top: 4px !important;
    }

    .ant-menu-item.active .ant-menu-title-content, .ant-menu-item:hover .ant-menu-title-content{
        background: #F7FFE1;

        img{
            filter: brightness(0) saturate(100%) invert(76%) sepia(37%) saturate(5461%) hue-rotate(34deg) brightness(104%) contrast(101%);
        }

        span{
            font-weight: 700;
        }
    }

    .ant-menu-item:hover{
        color: #000000  !important;
    }

    .ant-menu-item.active .ant-menu-title-content::after, .ant-menu-item:hover .ant-menu-title-content::after{
        content: '';
        position: absolute;
        top: 6px;
        background: #99CC00;
        right: 0;
        height: 92%;
        width: 4px;
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