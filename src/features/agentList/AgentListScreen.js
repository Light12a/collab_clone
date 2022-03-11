import React, { useState, useEffect, useCallback } from 'react';
import sortDown from '../../asset/sortDown.svg';
import sortUp from '../../asset/sortUp.svg';
import './AgentListScreen.css'
import { useDispatch, useSelector } from 'react-redux';
import { setAgentListOpen } from '../../redux/reducers/agentList/agentListStatus';
import { useTranslation } from 'react-i18next';
import { changeCurrentCallState, setCurrentCall } from '../../redux/reducers/call/currentCall';
import { appColor } from '../../value/color';
import Pagination from '../../components/Pagination';
import { Select } from 'antd';
import arrowIcon from '../../asset/ic.svg'
import Checkbox from 'antd/lib/checkbox/Checkbox';
import dialpad from '../../asset/dialpad.svg'
import { setIsKeypadOpen } from '../../redux/reducers/keypad/keypadStatus';
import SearchBar from '../../components/SearchBar'
import call from '../../asset/call.svg'

const AgentListScreen = (props) => {
    const { Option } = Select;
    const dispatch = useDispatch()
    const { t, i18n } = useTranslation();

    //get user infomation
    // const { isWaitingListOpen } = useSelector(state => state.waitingListStatus)
    const { agentList } = useSelector(state => state.AgentList)
    let ListAgent = agentList.agentList.users;
    let filterListAgent = [];

    // pagination
    let [totalItems, setTotalItem] = useState(0)
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10
    //x list
    let xListAgent = ListAgent;
    xListAgent = xListAgent.concat(xListAgent, ListAgent)
    xListAgent = xListAgent.concat(xListAgent, ListAgent)
    

    // get state
    const status = ListAgent.state

    let [listAgentForShow, setListAgentForShow] = useState([])

  

    useEffect(()=>{
        let newList = [];
        for(let i = 0; i < itemsPerPage; i++){
            console.log((currentPage-1)*itemsPerPage + i )
            newList.splice(i, 1, xListAgent[(currentPage-1)*itemsPerPage + i])
        }

        setListAgentForShow(newList)

    },[currentPage])

    const onSort = (sortTimeDes, sortCallNumberDes, sortNameDes) => {
        
    }
    const onPageChange = (page) =>{
        setCurrentPage(page)
    }

    const onSearch = (e) => {
        ListAgent.map((el) => {
            if (el.username.toLowerCase().includes(e.target.value) ||
                el.ext_number.toLowerCase().includes(e.target.value)) {
                filterListAgent.push(el)
                return el;
            } else {

                return ''
            }
        })
        setListAgentForShow(filterListAgent)
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
                        <td className='containercbStatus'>
                            <Checkbox className='checkboxStatus' />
                        </td>
                        <td>
                            {
                                RenderItemStatus(item.state)
                            }
                        </td>
                        <td>
                            {item.username}
                        </td>
                        <td>
                            {item.ext_number}
                        </td>
                        <td><img src={call} /></td>
                    </tr>
                    )
                })
                :
                filterListAgent && filterListAgent !== null &&
                    filterListAgent.map((item) => {
                        return (item && item !== null &&

                            <tr className='itemAgent'>
                                <td className='containercbStatus'>
                                    <Checkbox className='checkboxStatus' />
                                </td>

                                <td>
                                    {
                                        RenderItemStatus(item.state)
                                    }
                                </td>
                                <td>
                                    {item.username}
                                </td>
                                <td>
                                    {item.ext_number}
                                </td>
                                <td><img src={call} /></td>
                            </tr>
                        )
                    }
                    )
        )
    }

    const RenderItemStatus = (item) => {

        switch (item) {
            case 100:
                return <span className='statusAcceptable'>{t('acceptable')}</span>
            case 101:
                return <span className='statusOnHoding'>{t('afterTreatment')}</span>
            case 102:
                <span className='statusOnHoding'>{t('onHoding')}</span>
            case 103:
                return <span className='statusIncomingCall'>{t('incomingCall')}</span>
            case 104:
                return <span className='statusInACall'>{t('inACall')}</span>
            default:
                return null;
        }

        {/* {status === "on Hoding" ?
                                            <span className='statusOnHoding'>{t('onHoding')}</span>
                                            :
                                            status === 'Acceptable' ?
                                                <span className='statusAcceptable'>{t('acceptable')}</span>
                                                :
                                                status !== 'after-Treatment' ?
                                                    <span className='statusOnHoding'>{t('afterTreatment')}</span>
                                                    :
                                                    status === 'after-Treatment' ?
                                                        <span className='statusOnHodingInTransferredCall'>{t('onHoding')} ({t('in transferred call')})</span>
                                                        :
                                                        status === 'after-Treatment' ?
                                                            <span className='statusIncomingCall'>{t('incomingCall')}</span>
                                                            :
                                                            <span className='statusInACall'>{t('inACall')}</span>

                                        } */}

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
                        <Select defaultValue={t('all')} suffixIcon={<img src={arrowIcon} />}>
                            <Option value={t('all')}>{t('all')}</Option>
                            <Option value={t('selectSkillGroup')}>{t('selectSkillGroup')}</Option>
                        </Select>
                    </div>

                    <div className='form-group'>
                        <span className='title'>{t('status')}</span>
                        <Select defaultValue={t('all')} suffixIcon={<img src={arrowIcon} />}>
                            <Option value={t('all')}>{t('all')}</Option>
                            <Option value={t('status')}>{t('status')}</Option>
                        </Select>
                    </div>


                </div>
                <div className='agent-list__body__table'>
                    <table>
                        <thead>
                            <th></th>
                            <th>
                                <div className="table-th">
                                    <span>{t('status')}</span>
                                    <div className='table-sort' onClick={e => { onSort(null, null, true) }}>
                                        <img src={sortUp}></img>
                                        <img src={sortDown}></img>
                                    </div>

                                </div>
                            </th>

                            <th>
                                <div className="table-th">
                                    <span>{t('agentName')}</span>
                                    <div className='table-sort' onClick={e => { onSort(null, null, true) }}>
                                        <img src={sortUp}></img>
                                        <img src={sortDown}></img>
                                    </div>
                                </div>
                            </th>

                            <th>
                                <div className="table-th">
                                    <span>{t('extensionNumber')}</span>
                                    <div className='table-sort' onClick={e => { onSort(null, null, true) }}>
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
                        onPageChange={(e) =>onPageChange(e)}
                    />
                    <div>

                    </div>
                </div>
            </div>
        </>
    )
}

export default React.memo(AgentListScreen);