import React, { useState, useEffect, useCallback } from 'react';
import sortDown from '../../asset/sortDown.svg';
import sortUp from '../../asset/sortUp.svg';
import './AgentListScreen.css'
import { callConstant } from '../../util/constant';
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

const AgentListScreen = (props) => {
    const { Option } = Select;
    const ua = useSip()
    const dispatch = useDispatch()
    const { t, i18n } = useTranslation();
    const { currentState } = useSelector(state => state.connectStatus)
    const { skillGroupList } = useSelector(state => state.waiting)

    console.log("My Skill group: " + JSON.stringify(skillGroupList))
    //get user infomation
    const { agentList } = useSelector(state => state.AgentList)
    const { agentListType } = useSelector(state => state.agentListStatus)
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
    const itemsPerPage = 10


    // get state
    const status = ListAgent.state
    const [bufferListAgent, setBufferListAgent] = useState(xListAgent)


    useEffect(() => {


    }, [])


    useEffect(() => {
        let newList = [];
        console.log("My bufferListAgent: " + JSON.stringify(bufferListAgent))
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
        console.log("My List: " + JSON.stringify(list))
        setBufferListAgent(list)
    }
    const onPageChange = (page) => {
        setCurrentPage(page)
    }
    const makeCall = (callNumber) => {
        if(agentListType === agentListTypeConstant.CALL){
            if (currentState !== 'connected') {
                message.error('not connect to PBX')
                return
            }
            if (callNumber.trim() === '') return
            dispatch(changeCurrentCallState(callConstant.MAKE_CALL))
            dispatch(setActiveCallExtNumber(callNumber))
            ua.call(callNumber, callOptions)
        }
        else if(agentListType === agentListTypeConstant.TRANSFER){
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
        xListAgent.map((el) => {
            if (el.username.toLowerCase().includes(e.target.value) ||
                el.ext_number.toLowerCase().includes(e.target.value)) {
                filterListAgent.push(el)
                return el;
            } else {
                return ''
            }
        })
        setBufferListAgent(filterListAgent)
        e.target.value ?
            ListAgent = []
            : ListAgent = agentList.agentList.users

    }
    const RenderUserItem = () => {
        return (
            listAgentForShow && listAgentForShow !== null ?
                listAgentForShow.map((item) => {
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
                                <button src={call} onClick={e => console.log("hi")} />
                            </td>
                        </tr>
                    )
                }
                )
        )
    }

    return (
        <>
            <div className="agent-list__header drag-header">
                <span>{t('agentList')}</span>
                <img src={require('../../asset/Close.svg').default} alt="" onClick={e => { dispatch(setAgentListOpen(false)) }} />
            </div>

            <div className='agent-list__body'>
                <div className='noti-number'>
                    <p>{t('yourNotiNumber')}<span>*</span></p>
                    <div className='noti-number__group'>
                        <Select style={{ width: '376px' }} defaultValue={'123-444-444'} suffixIcon={<img src={arrowIcon} />}>
                            <Option value="123-444-444">123-444-444</Option>
                            <Option value="123-555-555">123-555-555</Option>
                        </Select>
                        <button onClick={e => { dispatch(setIsKeypadOpen(true)) }}><img src={dialpad} alt="" />{t("dialPad")}</button>
                    </div>
                </div>

                <div className='container-bar'>
                    <div className='form-group'>
                        <span className='title'>{t('search')}</span>
                        <SearchBar data={listAgentForShow} t={t} onSearch={e => onSearch} />

                    </div>
                    <div className='form-group'>
                        <span className='title'>{t('skillGroup')}</span>
                        <CustomSelect
                            defaultText="Select skill group"
                            optionsList={skillGroupList}
                            
                            // onSelectGroup={e => onSelect(e)}
                        />
                    </div>

                    <div className='form-group'>
                        <span className='title'>{t('status')}</span>
                        <CustomSelect 
                            defaultText="Select status"
                            optionsList={skillGroupList}
                            // onSelectGroup={e => onSelect(e)}
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
        </>
    )
}
export default React.memo(AgentListScreen);