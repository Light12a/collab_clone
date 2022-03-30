import React, { useState, useEffect, useRef, useMemo } from 'react';
import sortDown from '../../asset/sortDown.png';
import sortUp from '../../asset/sortUp.png';
import { useDispatch, useSelector } from 'react-redux';
import { setIsWaitingListOpen } from '../../redux/reducers/waitingList/waitingListStatus';
import { useTranslation } from 'react-i18next';
import { callConstant } from '../../util/constant';
import { changeCurrentCallState, setCurrentCall } from '../../redux/reducers/call/currentCall';
import CustomSelect from "../../components/CustomSelect";
import styled from 'styled-components';
import { Select, Radio } from "antd";
import TimerClock from './TimerClock';

const WaitingList = React.forwardRef((props, ref) => {
    const log = require('electron-log');
    const dispatch = useDispatch()
    const { t, i18n } = useTranslation();

    const [isSortWaitingTimeDes, setIsSortWaitingTimeDes] = useState(null);
    const [isSortWaitingCallDes, setIsSortWaitingCallDes] = useState(null);
    const [isSortNameDes, setIsSortNameDes] = useState(null);
    //use for render
    var pageNo = 1;
    const pageSize = 9;
    const [pages, setPages] = useState([]);
    const [renderPage, setRenderPage] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [renderItems, setRenderItems] = useState([]);
    const isFirstLoop = useRef(true);
    const skillGroups = useRef([]);
    const [selectedGroup, setSelectedGroup] = useState(null);


    //redux
    const { waitingList, skillGroupList, newestCall, removedCall } = useSelector(state => state.waiting)

    const { Option } = Select;

    //apply change when change page, sort
    useEffect(() => {
        if (isFirstLoop.current) return;
        renderTable();

    }, [isSortWaitingTimeDes, currentPage, isSortWaitingCallDes, isSortNameDes]);

    //load call from store when open waiting list
    useEffect(() => {
        loadCalls();
    }, []);

    //trigger when new call coming
    useEffect(() => {
        if (isFirstLoop.current || !newestCall) return;
        addACall(newestCall);
        onSort(isSortWaitingTimeDes === null ? null : true, isSortWaitingCallDes === null ? null : true, isSortNameDes === null ? null : true, false);
    }, [newestCall]);

    //trigger when call timeout to remove call from list
    useEffect(() => {
        if (isFirstLoop.current || !removedCall) return;
        removeACall(removedCall)
        onSort(isSortWaitingTimeDes === null ? null : true, isSortWaitingCallDes === null ? null : true, isSortNameDes === null ? null : true, false);
    }, [removedCall]);

    //load waiting calls when open waiting list
    const loadCalls = () => {
        var skillGroupsCopy = JSON.parse(JSON.stringify(skillGroupList))
        
        skillGroupsCopy.forEach(group => {
            waitingList.forEach(waiting => {
                if (waiting.group_id === group.group_id) {
                    group.calls.push(waiting);
                }
            });
        });
        
        skillGroups.current.splice(0, skillGroups.current.length, ...skillGroupsCopy);
        calculatePagination();
        onDataChange();
        onPageChange(1);
    }

    //add new call
    const addACall = (call) => {
        skillGroups.current.forEach(group => {
            if (group.group_id === call.group_id) {
                group.calls.push(call);
            }
        });
        onDataChange();
    }

    //remove canceled call
    const removeACall = (sessionId) => {
        skillGroups.current.forEach(group => {
            group.calls = group.calls?.filter(item => item.ssId !== sessionId);
        });
        onDataChange();
    }

    const calculatePagination = () => {
        if (skillGroups.current.length % pageSize === 0) {
            pageNo = Math.floor(skillGroups.current.length / pageSize);
        }
        else {
            pageNo = Math.floor(skillGroups.current.length / pageSize) + 1;
        }
        for (let i = 1; i <= pageNo; i++) {
            pages.splice(i -1, 1, i);
        }
        pages.length = pageNo;
        log.info("WaitingList.js::calculatePagination() page list after calculated: ", pages);
    }

    //use for re-format data after add/remove skillGroups
    const onDataChange = () => {
        //get longest waiting call
        skillGroups.current.forEach(element => {
            element.calls?.sort((a, b) => new Date(a.arrivedTime) - new Date(b.arrivedTime));
            element.longestWait = element.calls[0]?.arrivedTime;
        });

        //sort by time when first time add data
        if (isFirstLoop.current) {
            skillGroups.current.sort((a, b) => new Date(a.longestWait) - new Date(b.longestWait));
            isFirstLoop.current = false;
            setIsSortWaitingTimeDes(!isSortWaitingTimeDes);
        }
        renderTable();
    }

    //render table of skillGroups
    const renderTable = () => {
        for (let i = 0; i < pageSize; i++) {
            renderItems.splice(i, 1, skillGroups.current[(currentPage - 1) * pageSize + i] ? skillGroups.current[(currentPage - 1) * pageSize + i] : {})
        }
        log.info("WaitingList.js::renderTable() items will be rendered in table: ", renderItems);
        setRenderItems([...renderItems])
    }

    const onSort = (sortTimeDes, sortCallNumberDes, sortNameDes, sortFromClick) => {
        let sortNameDec = isSortNameDes;
        let sortWaitingCallDec = isSortWaitingCallDes;
        let sortWaitingTimeDec = isSortWaitingTimeDes;
        if (!sortFromClick) {
            sortNameDec = !isSortNameDes;
            sortWaitingCallDec = !isSortWaitingCallDes;
            sortWaitingTimeDec = !isSortWaitingTimeDes;
        }
        //seperate list skill group to 2 list, have and don't have calls in
        var hadCallGroups = [];
        var noCallGroups = [];
        skillGroups.current.forEach(group => {
            if (group.calls?.length > 0) {
                hadCallGroups.push(group)
            }
            else {
                noCallGroups.push(group)
            }
        });

        //sort by waiting time
        if (sortTimeDes) {
            if (!sortWaitingTimeDec) {
                hadCallGroups.sort((a, b) => new Date(a.longestWait) - new Date(b.longestWait));
                noCallGroups.sort((a, b) => new Date(a.longestWait) - new Date(b.longestWait));
            }
            else {
                hadCallGroups.sort((a, b) => new Date(b.longestWait) - new Date(a.longestWait));
                noCallGroups.sort((a, b) => new Date(b.longestWait) - new Date(a.longestWait));
            }
            if (sortFromClick) {
                setIsSortNameDes(null);
                setIsSortWaitingCallDes(null);
                setIsSortWaitingTimeDes(!isSortWaitingTimeDes);
            }
        }

        //sort by number of waiting calls
        if (sortCallNumberDes) {
            if (!sortWaitingCallDec) {
                hadCallGroups.sort((a, b) => b.calls.length - a.calls.length);
                noCallGroups.sort((a, b) => b.calls.length - a.calls.length);
            }
            else {
                hadCallGroups.sort((a, b) => a.calls.length - b.calls.length);
                noCallGroups.sort((a, b) => a.calls.length - b.calls.length);
            }
            if (sortFromClick) {
                setIsSortNameDes(null);
                setIsSortWaitingCallDes(!isSortWaitingCallDes);
                setIsSortWaitingTimeDes(null);
            }
        }

        //sort by name
        if (sortNameDes) {
            if (!sortNameDec) {
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

        skillGroups.current.splice(0, skillGroups.current.length, ...hadCallGroups, ...noCallGroups);
        
        log.info("WaitingList.js::onSort() Skill groups list after sort: ", skillGroups.current);
        renderTable();
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
        renderPage.length = maxRenderPage;
    }

    const answer = () => {
        skillGroups.current.forEach(group => {
            if (group.group_id === selectedGroup.group_id
                && group?.calls?.length > 0) {
                group.calls.sort((a, b) => new Date(a.arrivedTime) - new Date(b.arrivedTime));
                dispatch(setCurrentCall({ sessionId: group.calls[0].ssId, state: callConstant.ANSWER, displayName: group.calls[0].userName }));
            }
        });
        dispatch(setIsWaitingListOpen(false));
    }

    //filter
    const onSelect = (group) => {
        if (group.group_id > 0) {
            loadCalls();
            skillGroups.current = skillGroups.current.filter(item => item.group_id === group.group_id);
            onDataChange();
            calculatePagination();
            renderTable();
            onPageChange(1);
        }
        else{
            loadCalls();
        }
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

    return (
        <Wrapper ref={ref}>
            <div className='waiting-list__header drag-header'>
                <span>{t('waitingList')}</span>
                <img src={require('../../asset/Close.svg').default} alt="" onClick={e => { dispatch(setIsWaitingListOpen(false)) }} />
            </div>
            <div className='waiting-list__body drag-body'>
                <p>{t('skillGroup')}</p>
                <CustomSelect
                    defaultText="Select skill group"
                    optionsList={skillGroupList}
                    selectWidth ="300px"
                    onSelectGroup={e => onSelect(e)}
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
                                            style={{ verticalAlign: 'middle', visibility: item.group_name ? 'visible' : 'hidden' }}
                                            type="radio"
                                            name='rdCall'
                                            disabled={item.calls?.length > 0 ? false : true}
                                            onChange={e => setSelectedGroup(item)}
                                        />
                                    </td>
                                    <td>{item.group_name}</td>
                                    <td>{item.calls ? item.calls.length : ''}</td>
                                    {item.group_id &&
                                        <TimerClock
                                            longestWait={item.longestWait}
                                        />
                                    }
                                    {!item.group_id &&
                                        <td></td>
                                    }

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
                    disabled={selectedGroup?.calls?.length > 0 ? false : true}
                    className={selectedGroup?.calls?.length > 0 ? 'btn-primary' : 'btn-primary disable'}
                    onClick={e => answer()}
                >Answer</button>
            </div>

        </Wrapper>

    );
});

const Wrapper = styled.div`
    background-color: white;
    box-shadow: 0px 6px 60px rgba(0, 0, 0, 0.16);
    border-radius: 4px;
    max-width: 90vw;

    .drag-header {
        display: flex;
        justify-content: space-between;
        padding: 16px;
        border-bottom: 1px solid #ececec;
        align-items: center;
    }

    .drag-body {
        padding: 16px;
    }

    .drag-footer {
        border-top: #ececec 1px solid;
        padding: 16px;
    }

    .waiting-list{
        width: 569px;
    }

    .drag-table{
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

    .tr-selected td{
        background-color: #F7FBEB;
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


export default WaitingList;
