import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import styled from 'styled-components'
import Route from '../route/index'
import Sidebar from '../components/layout/Sidebar'
import Topbar from '../components/layout/Topbar';
import useSip from '../hooks/useSip';
import { setConnect } from '../redux/reducers/connection/connectStatus';
import { refreshToken } from '../redux/reducers/authen/auth';
import { withTranslation } from 'react-i18next';
import { GetAgentList } from '../redux/reducers/agentList/AgentList'

const MainApp = ({ t }) => {

    const ua = useSip()
    const dispatch = useDispatch()
    const { isConnected } = useSelector(state => state.networkStatus)
    const { isAuth, token: { haveToken, token, isSetting } } = useSelector(state => state.auth)

    useEffect(() => {
        let token = localStorage.getItem('token')
        if (isAuth)
            dispatch(GetAgentList(token))

    })

    useEffect(() => {
        let refreshTime = (+localStorage.getItem('expire') - (new Date()).getTime()) / 2
        console.log('refresh timout', refreshTime)
        let refreshTokenTimeoutID = setTimeout(() => {
            dispatch(refreshToken(token))
        }, refreshTime)
        return () => clearTimeout(refreshTokenTimeoutID)
    }, [token, dispatch])

    return (
        <Wrapper>
            <Topbar t={t} />
            <div className="main">
                <Route />
                <Sidebar t={t} />
            </div>
        </Wrapper>
    );
};

const Wrapper = styled.div`
    width: 100%;
    height: 100vh;

    .main{
        display:flex;
        justify-content:space-between;
        width: calc(100% - 100px);
        padding-right: 20px;
    }
`

export default withTranslation()(React.memo(MainApp));