import React, { useState, useEffect, useRef } from 'react';
import sortDown from '../../asset/sortDown.png';
import sortUp from '../../asset/sortUp.png';
import { useDispatch, useSelector } from 'react-redux';
import { setIsWaitingListOpen } from '../../redux/reducers/waitingList/waitingListStatus';
import { useTranslation } from 'react-i18next';
import { callConstant } from '../../util/constant';
import { changeCurrentCallState, setCurrentCall } from '../../redux/reducers/call/currentCall';
import CustomSelect from "./CustomSelect";
import styled from 'styled-components';
import { Select, Radio } from "antd";
import arrowIcon from '../../asset/arrow_green.png'

const WaitingList = React.forwardRef((props, ref) => {
    const dispatch = useDispatch()
    const { t, i18n } = useTranslation();

    const [callList, setCallList] = useState([]);
    const [callInfo, setCallInfo] = useState([]);
    const [isSortWaitingTimeDes, setIsSortWaitingTimeDes] = useState(true);
    const [isSortWaitingCallDes, setIsSortWaitingCallDes] = useState(null);
    const [isSortNameDes, setIsSortNameDes] = useState(null);
    //use for render
    const intervalId = useRef(null);
    var pageNo = 1;
    const pageSize = 9;
    const [pages, setPages] = useState([]);
    const [renderPage, setRenderPage] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [renderItems, setRenderItems] = useState([]);
    const [isFirstLoop, setIsFirstLoop] = useState(true);
    const [skillGroups, setSkillGroups] = useState([]);
    const [selectedGroup, setSelectedGroup] = useState(null);

    //redux
    const { waitingList, skillGroupList, newestCall, removedCall } = useSelector(state => state.waiting)

    const { Option } = Select;

    //apply change when change page, sort
    useEffect(() => {
        if (isFirstLoop) return;
        restartInterval();

    }, [isSortWaitingTimeDes, currentPage, isSortWaitingCallDes, isSortNameDes]);

    //load call from store when open waiting list
    useEffect(() => {
        loadCalls();
        restartInterval();

        return () => {
            if (intervalId.current) {
                clearInterval(intervalId.current);
            }
        }
    }, []);

    //trigger when new call coming
    useEffect(() => {
        if (isFirstLoop || !newestCall) return;
        addACall(newestCall);
        onSort(isSortWaitingTimeDes, isSortWaitingCallDes, isSortNameDes, false);
        //restartInterval();
    }, [newestCall]);

    //trigger when call timeout to remove call from list
    useEffect(() => {
        if (isFirstLoop || !removedCall) return;
        removeACall(removedCall)
        onSort(isSortWaitingTimeDes, isSortWaitingCallDes, isSortNameDes, false);
        //restartInterval();
    }, [removedCall]);

    //load waiting calls when open waiting list
    const loadCalls = () => {
        var skillGroupsCopy = JSON.parse(JSON.stringify(skillGroupList))
        skillGroupsCopy.push({
            "group_id": 98,
            "group_name": "Conference"
        },
            {
                "group_id": 99,
                "group_name": "Other"
            });
        skillGroupsCopy.forEach(group => {
            group.calls = [];
            waitingList.forEach(waiting => {
                if (waiting.group_id === group.group_id) {
                    group.calls.push(waiting);
                }
            });
        });

        for (let i = 0; i < 9; i++) {
            skillGroupsCopy.push({
                "group_id": 100 + i,
                "group_name": "group " + 100 + i,
                "calls": []
            })
        }

        skillGroups.splice(0, skillGroups.length, ...skillGroupsCopy);
        setSkillGroups([...skillGroups]);

        if (skillGroups.length % pageSize === 0) {
            pageNo = Math.floor(skillGroups.length / pageSize);
        }
        else {
            pageNo = Math.floor(skillGroups.length / pageSize) + 1;
        }
        for (let i = 1; i <= pageNo; i++) {
            pages.push(i)
        }

        console.log("pageNo: " + pageNo);

        onPageChange(1);



    }

    //add new call
    const addACall = (call) => {
        skillGroups.forEach(group => {
            if (group.group_id === call.group_id) {
                group.calls.push(call);
            }
        });

        setSkillGroups([...skillGroups]);
    }

    //remove canceled call
    const removeACall = (sessionId) => {
        console.log("removeACall ssId: ", sessionId);
        console.log("removeACall before filter: ", JSON.stringify(skillGroups));
        skillGroups.forEach(group => {
            group.calls = group.calls?.filter(item => item.ssId !== sessionId);
            console.log("removeACall group.calls: ", group.calls);
        });

        console.log("removeACall after filter: ", JSON.stringify(skillGroups));
        setSkillGroups([...skillGroups]);
    }

    //restart interval to apply data change
    const restartInterval = () => {
        if (intervalId.current) {
            clearInterval(intervalId.current);
        }
        intervalId.current = setInterval(runLoop, 1000);
    }

    const runLoop = () => {
        console.log("Skill group list: ", JSON.stringify(skillGroups))
        skillGroups.forEach(element => {
            let longestWait = 0;
            element.calls?.forEach(call => {
                let now = new Date();
                let wait = Math.abs(now - new Date(call.arrivedTime));
                if (wait > longestWait) {
                    longestWait = wait;
                }
            });
            element.waitingTimeMilisecond = longestWait;
            let waitSeconds = Math.floor(longestWait / 1000);
            let waitMinutes = Math.floor(waitSeconds / 60);
            if (waitMinutes > 0) {
                if (waitMinutes < 10) {
                    waitMinutes = "0" + waitMinutes.toString();
                }
                waitSeconds = waitSeconds % 60;
            }
            else {
                waitMinutes = "00"
            }
            if (waitSeconds < 10) {
                waitSeconds = "0" + waitSeconds.toString();
            }
            element.waitingTime = waitMinutes + ":" + waitSeconds;

            element.waitingCall = element.calls?.length || 0;
        });

        if (isFirstLoop) {
            skillGroups.sort((a, b) => b.waitingTimeMilisecond - a.waitingTimeMilisecond);
            setIsFirstLoop(false);
        }

        for (let i = 0; i < pageSize; i++) {
            renderItems.splice(i, 1, skillGroups[(currentPage - 1) * pageSize + i] ? skillGroups[(currentPage - 1) * pageSize + i] : {})
        }

        setSkillGroups([...skillGroups]);
    }

    const onSort = (sortTimeDes, sortCallNumberDes, sortNameDes, sortFromClick) => {
        console.log("onSort: " + sortTimeDes + sortCallNumberDes + sortNameDes);
        //seperate list skill group to 2 list, have and don't have calls in
        var hadCallGroups = [];
        var noCallGroups = [];
        skillGroups.forEach(group => {
            if (group.calls?.length > 0) {
                hadCallGroups.push(group)
            }
            else {
                noCallGroups.push(group)
            }
        });
        console.log("hadCallGroups: ", JSON.stringify(hadCallGroups));
        console.log("noCallGroups: ", JSON.stringify(noCallGroups));

        //sort by waiting time
        if (sortTimeDes) {
            if (!isSortWaitingTimeDes) {
                hadCallGroups.sort((a, b) => b.waitingTimeMilisecond - a.waitingTimeMilisecond);
                noCallGroups.sort((a, b) => b.waitingTimeMilisecond - a.waitingTimeMilisecond);
            }
            else {
                hadCallGroups.sort((a, b) => a.waitingTimeMilisecond - b.waitingTimeMilisecond);
                noCallGroups.sort((a, b) => a.waitingTimeMilisecond - b.waitingTimeMilisecond);
            }
            if (sortFromClick) {
                setIsSortNameDes(null);
                setIsSortWaitingCallDes(null);
                setIsSortWaitingTimeDes(!isSortWaitingTimeDes);
            }
        }

        //sort by number of waiting calls
        if (sortCallNumberDes) {
            if (!isSortWaitingCallDes) {
                hadCallGroups.sort((a, b) => b.waitingCall - a.waitingCall);
                noCallGroups.sort((a, b) => b.waitingCall - a.waitingCall);
            }
            else {
                hadCallGroups.sort((a, b) => a.waitingCall - b.waitingCall);
                noCallGroups.sort((a, b) => a.waitingCall - b.waitingCall);
            }
            if (sortFromClick) {
                setIsSortNameDes(null);
                setIsSortWaitingCallDes(!isSortWaitingCallDes);
                setIsSortWaitingTimeDes(null);
            }
        }

        //sort by name
        if (sortNameDes) {
            if (!isSortNameDes) {
                hadCallGroups.sort((a, b) => a.group_name.localeCompare(b.group_name));
                noCallGroups.sort((a, b) => a.group_name.localeCompare(b.group_name));
            }
            else {
                hadCallGroups.sort((a, b) => b.group_name.localeCompare(a.group_name));
                noCallGroups.sort((a, b) => b.group_name.localeCompare(a.group_name));
            }
            if (sortFromClick) {
                setIsSortNameDes(!isSortNameDes);
                setIsSortWaitingCallDes(null);
                setIsSortWaitingTimeDes(null);
            }
        }

        skillGroups.splice(0, skillGroups.length, ...hadCallGroups, ...noCallGroups);

        setSkillGroups([...skillGroups]);
    }

    const onPageChange = (pageNumber) => {
        setCurrentPage(pageNumber);
        let maxRenderPage = 3;
        if (pages.length < maxRenderPage) {
            maxRenderPage = pages.length;
        }
        if (pageNumber === 1) {
            for (let i = 0; i < maxRenderPage; i++) {
                renderPage.splice(i, 1, i + 1);
            }
        }
        else if (pageNumber === pages.length) {
            if (maxRenderPage === 2) {
                for (let i = 0; i < maxRenderPage; i++) {
                    renderPage.splice(i, 1, pages.length - 1 + i);
                }
            }
            else {
                for (let i = 0; i < maxRenderPage; i++) {
                    renderPage.splice(i, 1, pages.length - 2 + i);
                }
            }

        }
        else {
            for (let i = 0; i < maxRenderPage; i++) {
                renderPage.splice(i, 1, pageNumber - 1 + i);
            }
        }
    }

    const answer = () => {
        skillGroups.forEach(group => {
            if (group.group_id === selectedGroup.group_id
                && group?.calls?.length > 0) {
                group.calls.sort((a, b) => new Date(a.arrivedTime) - new Date(b.arrivedTime));
                dispatch(setCurrentCall({ sessionId: group.calls[0].ssId, state: callConstant.ANSWER, displayName: group.calls[0].userName }));
            }
        });
        dispatch(setIsWaitingListOpen(false));
    }

    const paginationItem = {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '24px',
        width: '24px',
        fontSize: '14px',
        marginLeft: '5px',
        marginRight: '5px',
        border: '1px solid #CDCDCD',
        borderRadius: '4px'
    }
    const skillGroup = [
        { id: 1, name: "Skill group 1" },
        { id: 2, name: "Skill group 2" },
        { id: 3, name: "Skill group 3" },
      ]

    return (
        <Wrapper ref={ref}>
            <div className='waiting-list__header drag-header'>
                <span>{t('waitingList')}</span>
                <img src={require('../../asset/Close.svg').default} alt="" onClick={e => { dispatch(setIsWaitingListOpen(false)) }} />
            </div>
            <div className='waiting-list__body drag-body'>
                <p>{t('skillGroup')}</p>
                {/* <Select style={{ width: '300px' }} defaultValue={t('selectSkillGroup')} suffixIcon={<img src={arrowIcon} />}>
                    <Option value="skillGroup1">Skillgroup 1</Option>
                    <Option value="skillGroup2">Skillgroup 2</Option>
                    <Option value="skillGroup3">Skillgroup 3</Option>
                </Select> */}

                <CustomSelect
                    defaultText="Select skill group"
                    optionsList={skillGroup}
                />


                <table className='drag-table'>
                    <thead>
                        <th></th>
                        <th>
                            <div className='table-th'>
                                <span>{t('skillGroupName')}</span>
                                <div className='table-sort' onClick={e => { onSort(null, null, true, true) }}>
                                    <img className={isSortNameDes === null ? 'filter-disable' : isSortNameDes ? 'filter-disable' : ''} src={sortUp}></img>
                                    <img className={isSortNameDes === null ? 'filter-disable' : isSortNameDes ? '' : 'filter-disable'} src={sortDown}></img>
                                </div>
                            </div>
                        </th>
                        <th>
                            <div className='table-th'>
                                <span>{t('waiting')}</span>
                                <div className='table-sort' onClick={e => { onSort(null, true, null, true) }}>
                                    <img className={isSortWaitingCallDes === null ? 'filter-disable' : isSortWaitingCallDes ? 'filter-disable' : ''} src={sortUp}></img>
                                    <img className={isSortWaitingCallDes === null ? 'filter-disable' : isSortWaitingCallDes ? '' : 'filter-disable'} src={sortDown}></img>
                                </div>
                            </div>
                        </th>
                        <th>
                            <div className='table-th'>
                                <span>{t('waitingTime')}</span>
                                <div className='table-sort' onClick={e => { onSort(true, null, null, true) }}>
                                    <img className={isSortWaitingTimeDes === null ? 'filter-disable' : isSortWaitingTimeDes ? 'filter-disable' : ''} src={sortUp}></img>
                                    <img className={isSortWaitingTimeDes === null ? 'filter-disable' : isSortWaitingTimeDes ? '' : 'filter-disable'} src={sortDown}></img>
                                </div>
                            </div>
                        </th>
                    </thead>
                    <tbody>
                        {(renderItems.length > 0) &&
                            renderItems.map((item, index) =>
                            (
                                <tr>
                                    <td>
                                        <input
                                            style={{ verticalAlign: 'middle' }} type="radio" name='rdCall' disabled={item.waitingCall > 0 ? false : true}
                                            onChange={e => setSelectedGroup(item)}
                                        />
                                    </td>
                                    <td>{item.group_name}</td>
                                    <td>{item.waitingCall}</td>
                                    <td>{item.waitingTime}</td>
                                </tr>
                            ))
                        }
                    </tbody>
                </table>
                <div className="pagination-wrap">
                    <div style={{ display: 'flex' }}>
                        <span
                            className={currentPage === 1 ? 'pagination-disable' : 'pagination-move-to'}
                            onClick={e => onPageChange(1)}
                        >{t('toFirst')}</span>
                        <span
                            className={currentPage === 1 ? 'pagination-disable' : 'pagination-move-to'}
                            onClick={e => { onPageChange(currentPage - 1) }}
                        >{t('previous')}</span>
                        {renderPage.map((page, index) =>
                        (
                            <span style={(page) === currentPage ? Object.assign({}, paginationItem, { backgroundColor: '#99CC00', border: '1px solid #99CC00', cursor: 'pointer' }) : Object.assign({}, paginationItem, { cursor: 'pointer' })} onClick={e => { onPageChange(page) }}>{page}</span>
                        ))}
                        <span
                            className={currentPage >= pages.length ? 'pagination-disable' : 'pagination-move-to'}
                            onClick={e => { onPageChange(currentPage + 1) }}
                        >{t('next')}</span>
                        <span
                            className={currentPage >= pages.length ? 'pagination-disable' : 'pagination-move-to'}
                            onClick={e => onPageChange(pages.length)}
                        >{t('last')}</span>
                    </div>
                </div>
            </div>
            <div className='waiting-list__footer drag-footer'>
                <button
                    className={selectedGroup?.calls?.length > 0 ? 'btn-primary' : 'btn-primary disable'}
                    onClick={e => answer()}
                >Answer</button>
            </div>

        </Wrapper>

    );
});

const Wrapper = styled.div`
    .waiting-list__header{
        span{
            font-size: 20px;
            font-weight: 700;
            text-transform: uppercase;
        }
        img{
            cursor: pointer;
        }
    }

    .waiting-list__body{
        p{
            font-weight: 500;
            margin-bottom: 8px;
        }

        th, td{
            padding: 8px;
        }

        .pagination-wrap{
            margin-top: 12px;
            padding: 8px;
            display:flex;
            flex-direction: row-reverse;
        }
        
    }
    .waiting-list__footer{
        
        .btn-primary{
            width: 100%;
            border: none;
            background-color: #99CC00;
            color: #FFFFFF;
            border-radius: 8px;
            padding: 10px;
            font-weight: 700;
            cursor: pointer;
            
        }
        .btn-primary.disable{
            color: #A9A9A9;
            background: #C4C4C4;
            cursor: not-allowed;
        }
    }
    input[type='radio']{
        accent-color: olivedrab;
    }
    .filter-disable{
        filter: brightness(0) saturate(100%) invert(100%) sepia(1%) saturate(3760%) hue-rotate(177deg) brightness(111%) contrast(73%);
    }
    .pagination-move-to{
        margin-right: 5px;
        cursor: pointer;
    }
    .pagination-disable{
        opacity: 0.3;
        margin-right: 5px;
        pointer-events: none;
    }

`


export default React.memo(WaitingList);
