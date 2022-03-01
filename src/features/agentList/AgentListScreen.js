import React, { useState, useEffect } from 'react';
import sortDown from '../../asset/sortDown.svg';
import sortUp from '../../asset/sortUp.svg';
import './AgentListScreen.css'
import { useDispatch, useSelector } from 'react-redux';
import { setAgentListOpen } from '../../redux/reducers/agentList/agentListStatus';
import { useTranslation } from 'react-i18next';
import { callStatsContraint } from '../../redux/reducers/call/currentCall';
import { changeCurrentCallState, setCurrentCall } from '../../redux/reducers/call/currentCall';
import { appColor } from '../../value/color';
import { Select } from 'antd';
import arrowIcon from '../../asset/ic.svg'
import searchIcon from '../../asset/search.svg'
import Checkbox from 'antd/lib/checkbox/Checkbox';
import dialpad from '../../asset/dialpad.svg'
import { setIsKeypadOpen } from '../../redux/reducers/keypad/keypadStatus';
import call from '../../asset/call.svg'
const AgentListScreen = (props) => {
    const { Option } = Select;
    const dispatch = useDispatch()
    const { t, i18n } = useTranslation();

    //get user infomation
    // const { isWaitingListOpen } = useSelector(state => state.waitingListStatus)
    const { agentList } = useSelector(state => state.AgentList)
    const ListAgent = agentList.agentList.users;

    console.log("My Agent List: " + JSON.stringify(ListAgent))

    const status = ListAgent.state
    console.log("My status: " + status)
    // t("onHoding")

    const onSort = (sortTimeDes, sortCallNumberDes, sortNameDes) => {

    }

    const RenderItemStatus = (item) => {

        console.log("My Status: " + item)
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
                return <span className='statusAcceptable'>{t('acceptable')}</span>
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
                        <div className='search'>
                            <input placeholder={t('holderInputSearch')}></input>
                            <img
                                src={searchIcon}
                                onClick={() => alert('hi')}
                                className='iconSearch'
                            />
                        </div>
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

                            {ListAgent &&
                                ListAgent.map((item) =>
                                (
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
                                ))}
                        </tbody>

                    </table>
                </div>
            </div>
        </>
    )
}

export default React.memo(AgentListScreen);