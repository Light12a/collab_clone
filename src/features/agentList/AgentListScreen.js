import React, { useState, useEffect, useCallback } from 'react';
import sortDown from '../../asset/sortDown.svg';
import sortUp from '../../asset/sortUp.svg';
import { callConstant } from '../../util/constant';
import styled from "styled-components";
import { useDispatch, useSelector } from 'react-redux';
import { setAgentListOpen } from '../../redux/reducers/agentList/agentListStatus';
import { useTranslation } from 'react-i18next';
import { changeCurrentCallState, setCurrentCall, setActiveCallExtNumber, setTransferToExtNumber } from '../../redux/reducers/call/currentCall';
import { appColor } from '../../value/color';
import Pagination from '../../components/Pagination';
import CustomSelect from '../../components/CustomSelect';

import { Select, message } from 'antd';
import arrowIcon from '../../asset/ic.svg'
import PresenceState from '../../components/PresenceState'
import dialpad from '../../asset/dialpad.svg'
import { setIsKeypadOpen } from '../../redux/reducers/keypad/keypadStatus';
import SearchBar from '../../components/SearchBar'
import call from '../../asset/call.svg'
import useSip from '../../hooks/useSip';
import { agentListTypeConstant } from '../../util/constant';

const AgentListScreen = React.forwardRef((props, ref) => {
    // const { Option } = Select;
    const ua = useSip()
    const dispatch = useDispatch()
    const { t, i18n } = useTranslation();
    const { currentState } = useSelector(state => state.connectStatus)
    const { skillGroupList } = useSelector(state => state.waiting)

    //get user infomation
    const { agentList } = useSelector(state => state.AgentList)
    const { agentListType } = useSelector(state => state.agentListStatus)

    const [listSkillGroupName, setListSkillGroupName] = useState([]);
    let ListAgent = agentList.agentList.users;
    let filterListAgent = [];
    //x list
    let xListAgent = ListAgent;
    xListAgent = xListAgent.concat(xListAgent, ListAgent)
    xListAgent = xListAgent.concat(xListAgent, ListAgent)

    // get group
    const [skillGroup, setSkillGroup] = useState([]);

    // pagination
    let [totalItems, setTotalItem] = useState(0)
    const [currentPage, setCurrentPage] = useState(1);
    let [listAgentForShow, setListAgentForShow] = useState([])
    const [isSearch, setIsSearch] = useState(false)
    const itemsPerPage = 10

    // get state
    const status = ListAgent.state
    const [bufferListAgent, setBufferListAgent] = useState(xListAgent)

    useEffect(() => {
        xListAgent.map((agent) => {
            // agent = 9;
            skillGroupList.map((group) => {
                if (agent.group_id === group.group_id) {
                    listSkillGroupName.push(group.group_name)
                }
            })
        })

    }, [])


    useEffect(() => {
        let newList = [];
        for (let i = 0; i < itemsPerPage; i++) {
            newList.splice(i, 1, bufferListAgent[(currentPage - 1) * itemsPerPage + i])
        }

        setListAgentForShow(newList)

    }, [currentPage, bufferListAgent])

    const onSortStatus = (list) => {
        list.sort((a, b) => {
            return b.state - a.state
        })
        setBufferListAgent(list)
    }
    const onSortSkillGroupName = (list) => {
        list.sort((a, b) => {
            return b.group_id - a.group_id
        })
        setBufferListAgent(list)
    }
    const onSortName = (list) => {
        list.sort((a, b) => {
            return b.username.localeCompare(a.username)
        })
        setBufferListAgent(list)
    }
    const onSortExtension = (list) => {
        list.sort((a, b) => {
            if (a > b)
                return b.ext_number - a.ext_number
            return a.ext_number - b.ext_number
        })
        setBufferListAgent(list)
    }
    const onPageChange = (page) => {
        setCurrentPage(page)
    }
    const makeCall = (callNumber) => {
        if (agentListType === agentListTypeConstant.CALL) {
            if (currentState !== 'connected') {
                message.error('not connect to PBX')
                return
            }
            if (callNumber.trim() === '') return
            dispatch(changeCurrentCallState(callConstant.MAKE_CALL))
            dispatch(setActiveCallExtNumber(callNumber))
            ua.call(callNumber, callOptions)
        }
        else if (agentListType === agentListTypeConstant.TRANSFER) {
            dispatch(setTransferToExtNumber(callNumber));
            dispatch(changeCurrentCallState(callConstant.TRANSFER))
        }
        dispatch(setAgentListOpen(false))
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


    const onSearch = (e) => {
        const text = e.target.value
        text ? setIsSearch(true) : setIsSearch(false)
        console.log(e)

        xListAgent.map((el) => {
            if (el.username.toLowerCase().includes(text) ||
                el.ext_number.toLowerCase().includes(text)) {
                filterListAgent.push(el)
                return el;
            } else {
                return ''
            }
        })
        setBufferListAgent(filterListAgent)
        text ?
            ListAgent = []
            : ListAgent = agentList.agentList.users

    }

    const RenderUserItem = () => {
        return (
            listAgentForShow && listAgentForShow !== null ?
                listAgentForShow.map((item, index) => {
                    return (
                        item && item !== null &&
                        <tr className='itemAgent'>
                            {/* {
                            false && 
                            <td className='containercbStatus'>
                            <Checkbox className='checkboxStatus' />
                            </td>
                        } */}

                            <td>
                                <PresenceState state={item.state} />
                            </td>
                            <td>
                                {listSkillGroupName[index]}
                            </td>
                            <td>
                                {item.username}
                            </td>
                            <td>
                                {item.ext_number}
                            </td>
                            <td>
                                <img className='callButton' src={call} onClick={e => makeCall(item.ext_number)} />
                            </td>
                        </tr>
                    )
                })
                :
                filterListAgent && filterListAgent !== null &&
                filterListAgent.map((item) => {
                    return (item && item !== null &&

                        <tr className='itemAgent'>
                            {/* <td className='containercbStatus'>
                                    <Checkbox className='checkboxStatus' />
                                </td> */}

                            <td>
                                <PresenceState state={item.state} />
                            </td>
                            <td>
                                {item.group_id}
                            </td>
                            <td>
                                {item.username}
                            </td>
                            <td>
                                {item.ext_number}
                            </td>
                            <td>
                                <img className='callButton' src={call} onClick={e => makeCall(item.ext_number)} />
                            </td>
                        </tr>
                    )
                }
                )
        )
    }

    const onSelect = () => {

    }
    return (
        <AgentListWrapper ref={ref}>
            <div className="agent-list__header drag-header">
                <span>{t('agentList')}</span>
                <img src={require('../../asset/Close.svg').default} alt="" onClick={e => { dispatch(setAgentListOpen(false)) }} />
            </div>

            <div className='agent-list__body'>
                <div className='noti-number'>
                    <p>{t('yourNotiNumber')}<span>*</span></p>
                    <div className='noti-number__group'>
                        {/* <CustomSelect style={{ width: '376px' }} defaultValue={'123-444-444'} suffixIcon={<img src={arrowIcon} />}>
                            <Option value="123-444-444">123-444-444</Option>
                            <Option value="123-555-555">123-555-555</Option>
                        </CustomSelect> */}
                        <CustomSelect
                            defaultText="123-444-444"
                            selectWidth="20vw"
                            optionsList={[123 - 444 - 444, 123 - 555 - 555]}
                            onSelectGroup={e => onSelect(e)}
                        />
                        <button onClick={e => { dispatch(setIsKeypadOpen(true)) }}><img src={dialpad} alt="" />{t("dialPad")}</button>
                    </div>
                </div>

                <div className='container-bar'>
                    <div className='form-group'>
                        <span className='title'>{t('search')}</span>
                        <SearchBar
                            data={listAgentForShow}
                            t={t}
                            onSearch={e => onSearch}
                            isSearching={isSearch} />

                    </div>
                    <div className='form-group'>
                        <span className='title'>{t('skillGroup')}</span>
                        <CustomSelect
                            defaultText="Select skill group"

                            selectWidth="18vw"
                            optionsList={skillGroupList}
                            onSelectGroup={e => onSelect(e)}
                        />
                    </div>

                    <div className='form-group'>
                        <span className='title'>{t('status')}</span>
                        <CustomSelect
                            defaultText="Select status"
                            selectWidth="18vw"
                            optionsList={skillGroupList}
                            onSelectGroup={e => onSelect(e)}
                        />
                    </div>


                </div>
                <div className='agent-list__body__table'>
                    <table>
                        <thead>

                            <th>
                                <div className="table-th">
                                    <span>{t('status')}</span>
                                    <div className='table-sort' onClick={e => { onSortStatus(xListAgent) }}>
                                        <img src={sortUp}></img>
                                        <img src={sortDown}></img>
                                    </div>

                                </div>
                            </th>

                            <th>
                                <div className="table-th">
                                    <span>{t('skillGroupName')}</span>
                                    <div className='table-sort' onClick={e => { onSortSkillGroupName(xListAgent) }}>
                                        <img src={sortUp}></img>
                                        <img src={sortDown}></img>
                                    </div>
                                </div>
                            </th>
                            <th>
                                <div className="table-th">
                                    <span>{t('agentName')}</span>
                                    <div className='table-sort' onClick={e => { onSortName(xListAgent) }}>
                                        <img src={sortUp}></img>
                                        <img src={sortDown}></img>
                                    </div>
                                </div>
                            </th>
                            <th>
                                <div className="table-th">
                                    <span>{t('extensionNumber')}</span>
                                    <div className='table-sort' onClick={() => { onSortExtension(xListAgent) }}>
                                        <img src={sortUp}></img>
                                        <img src={sortDown}></img>
                                    </div>
                                </div>
                            </th>
                            <th></th>

                        </thead>
                        <tbody>
                            {RenderUserItem()}
                        </tbody>
                    </table>
                    <Pagination
                        total={xListAgent}
                        itemsPerPage={itemsPerPage}
                        t={t}
                        onPageChange={(e) => onPageChange(e)}
                    />
                    <div>
                    </div>
                </div>
            </div>
        </AgentListWrapper>
    )
})
const AgentListWrapper = styled.div`

    background-color: white;
    position: absolute;
    box-shadow: 0px 6px 60px rgba(0, 0, 0, 0.16);
    border-radius: 4px;

.agent-list{
    width: 840px;   
    min-height: 750px;
    max-height: fit-content !important;
}
 table{
    width: 100%;
    border-collapse: separate !important;
    border-spacing: 0;
    border-radius: 4px;
    border: 1px solid #ECECEC;
    margin-top:16px;
}
.table-th{
    display: flex;
    align-items: center;
    gap:0.5rem;
}
 th{
    background: #F6F6F6;
    border-bottom: 1px solid #ECECEC;
}
 tr:not(:last-child) td{
    border-bottom: 1px solid #ECECEC;
}

 .table-sort{
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap:1px;
    transform: translateY(1px);
    
}

 .table-sort img{
    cursor: pointer;
}

.agent-list__header span{
    font-size: 20px;
    font-weight: 700;
    text-transform: uppercase;
}

.agent-list__header img{
    cursor: pointer;
}

.agent-list__body {
    height: fit-content;
}
.agent-list__body .noti-number{
    background: #FBFBFB;
    padding: 16px;
    height: fit-content;
}
.agent-list__body .noti-number p{
    font-weight: 500;
}
.agent-list__body .noti-number p span{
    color: #EE0000;
    font-weight: 400;
}

.noti-number__group{
    display: flex;
    justify-content: space-between;
}

.noti-number__group button{
    background-color: #99CC00;
    width: 140px;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    color: #FFFFFF;
    cursor: pointer;
}

.noti-number__group button img{
    margin-right: 0.5rem;
}

.agent-list__body__table{
    padding: 16px;
    padding-top: 0;
}

.table {
    /* background-color: greenyellow; */
    border-radius: 4px;
    margin-top: 10px;
    height: 100%;
    width: 100%;
    border: 1px solid #ECECEC ;
}

.container-bar {
    display: flex;
    padding: 16px;
    gap: 16px;
}


.container-bar .form-group{
    display: flex;
    flex-direction: column;
    flex: 1;

}

.container-bar .form-group .title{
    font-weight: 500;
    margin-bottom: 6px;
}

.containerItemAgentEmpty {
    display: flex;
    border: 1px solid #ECECEC;
    flex-direction: row;
    align-items: center;
    height: 4vh;
}

 th{
    padding: 8px;
}

td{
    padding: 8px;
}

/* .checkboxStatus {
    margin: 1vw;
} */
.statusOffline{
    font-size: calc(0.5vw + 0.6vh);
    color: #707070;
    background-color: #ECECEC;
    border: 1px solid #707070;
    padding: 3px 10px 3px 10px;
    border-radius: 100px;
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
.sumContainerSearch {
    flex: 2;
    width: 100%;
}
.sumContainerSkillGroup {
    flex: 1;
    width: 100%;
}
.sumContainerStatus{
    flex: 1;
    width: 100%;
}
.titleSkillGroup {
    padding-left: 1vw;
}
.containercbStatus {
    /* background-color: red; */
    width: 4vw !important;
}

.callButton{
    cursor: pointer;
    /* height: 30px;
    width: 30px;
    background-color: #009944; */
}
`
export default React.memo(AgentListScreen);