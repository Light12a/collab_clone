import React, { useState, useEffect } from 'react';
import sortDown from '../../asset/sortDown.png';
import sortUp from '../../asset/sortUp.png';
import { useDispatch, useSelector } from 'react-redux';
import { setIsWaitingListOpen } from '../../redux/reducers/waitingList/waitingListStatus';
import { useTranslation } from 'react-i18next';
import { callStatsContraint } from '../../redux/reducers/call/currentCall';
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
    const [isSortWaitingCallDes, setIsSortWaitingCallDes] = useState(false);
    const [isSortNameDes, setIsSortNameDes] = useState(false);
    const [intervalId, setIntervalId] = useState(null);
    var pageNo = 1;
    const pageSize = 9;
    const [pages, setPages] = useState([]);
    const [renderPage, setRenderPage] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [renderItems, setRenderItems] = useState([]);
    const [isFirstLoop, setIsFirstLoop] = useState(true);
    const waitingList = useSelector(state => state.waiting)

    const { Option } = Select;


    useEffect(() => {
        initValue()
        //stop interval
        if (intervalId) {
            clearInterval(intervalId);
        }
        //copy waiting list from store to local state
        var waitingListCopy = JSON.parse(JSON.stringify(waitingList))
        callList.splice(0, callList.length, ...waitingListCopy);
        setCallList([...callList]);

        let interval = setInterval(runLoop, 1000);
        setIntervalId(interval);

        return () => {
            if (intervalId) {
                clearInterval(intervalId);
            }
        }

    }, [isSortWaitingTimeDes, currentPage, isSortWaitingCallDes, isSortNameDes, waitingList]);

    const initValue = () => {
        console.log("init value");
        for (let i = 0; i < 100; i++) {
            callList.push({
                id: i,
                skillName: (Math.random() + 1).toString(36).substring(2, 7),
                calls: [
                    {
                        sipAddress: 'sip:1.com.vn',
                        optional: 'optional',
                        arrivedTime: randomDate()
                    },
                    {
                        sipAddress: 'sip:2.com.vn',
                        optional: 'optional',
                        arrivedTime: randomDate()
                    },
                    {
                        sipAddress: 'sip:3.com.vn',
                        optional: 'optional',
                        arrivedTime: randomDate()
                    },
                ],
                waitingTime: "00:00",
                waitingCall: 0,
                waitingTimeMilisecond: 0,
            });
        }
        if (callList.length % pageSize === 0) {
            pageNo = Math.floor(callList.length / pageSize);
        }
        else {
            pageNo = Math.floor(callList.length / pageSize) + 1;
        }
        console.log("pageNo: " + pageNo);
        for (let i = 1; i <= pageNo; i++) {
            pages.push(i)
        }
        onPageChange(1);
    }

    const randomDate = () => {
        let start = new Date(2021, 11, 23, 11, 19);
        let end = new Date();
        console.log("randomDate: " + start.toString() + end.toString());
        return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
    }


    const runLoop = () => {
        callList.forEach(element => {
            let longestWait = 0;
            element.calls.forEach(call => {
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

            element.waitingCall = element.calls.length;
        });

        if (isFirstLoop) {
            callList.sort((a, b) => b.waitingTimeMilisecond - a.waitingTimeMilisecond);
            setIsFirstLoop(false);
        }

        for (let i = 0; i < pageSize; i++) {
            renderItems.splice(i, 1, callList[(currentPage - 1) * pageSize + i] ? callList[(currentPage - 1) * pageSize + i] : {})
        }

        setCallList([...callList]);
    }

    const onSort = (sortTimeDes, sortCallNumberDes, sortNameDes) => {
        console.log("onSort: " + sortTimeDes + sortCallNumberDes + sortNameDes);

        //sortTime
        if (sortTimeDes) {
            if (!isSortWaitingTimeDes) {
                callList.sort((a, b) => b.waitingTimeMilisecond - a.waitingTimeMilisecond);
            }
            else {
                callList.sort((a, b) => a.waitingTimeMilisecond - b.waitingTimeMilisecond);
            }
            setIsSortWaitingTimeDes(!isSortWaitingTimeDes);
        }

        if (sortCallNumberDes) {
            if (!isSortWaitingCallDes) {
                console.log("sort here 1")
                callList.sort((a, b) => b.waitingCall - a.waitingCall);
            }
            else {
                console.log("sort here 2")
                callList.sort((a, b) => b.waitingCall - a.waitingCall);
            }
            setIsSortWaitingCallDes(!isSortWaitingCallDes);
        }

        //sort by name
        if (sortNameDes) {
            if (!isSortNameDes) {
                console.log("sort here 1")
                callList.sort((a, b) => a.skillName.localeCompare(b.skillName));
            }
            else {
                console.log("sort here 2")
                callList.sort((a, b) => b.skillName.localeCompare(a.skillName));
            }
            setIsSortNameDes(!isSortNameDes);
        }

        setCallList([...callList]);
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
            for (let i = 0; i < maxRenderPage; i++) {
                renderPage.splice(i, 1, pages.length - 2 + i);
            }
        }
        else {
            for (let i = 0; i < maxRenderPage; i++) {
                renderPage.splice(i, 1, pageNumber - 1 + i);
            }
        }
    }

    const answer = (calls, displayName) => {
        if (calls && calls.length > 0) {
            console.log("incoming im in");
            calls.sort((a, b) => new Date(a.arrivedTime) - new Date(b.arrivedTime));
            dispatch(setCurrentCall({ sessionId: calls[0].ssId, state: callStatsContraint.ANSWER, displayName: displayName }));
        }
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
                                <div className='table-sort' onClick={e => { onSort(null, null, true) }}>
                                    <img src={sortUp}></img>
                                    <img src={sortDown}></img>
                                </div>
                            </div>
                        </th>
                        <th>
                            <div className='table-th'>
                                <span>{t('waiting')}</span>
                                <div className='table-sort' onClick={e => { onSort(null, true, null) }}>
                                    <img src={sortUp}></img>
                                    <img src={sortDown}></img>
                                </div>
                            </div>
                        </th>
                        <th>
                            <div className='table-th'>
                                <span>{t('waitingTime')}</span>
                                <div className='table-sort' onClick={e => { onSort(true, null, null) }}>
                                    <img src={sortUp}></img>
                                    <img src={sortDown}></img>
                                </div>
                            </div>
                        </th>
                    </thead>
                    <tbody>
                        {(renderItems.length > 0) &&
                            renderItems.map((calls, index) =>
                            (
                                <tr onClick={e => { answer(calls.calls, calls.skillName) }}>
                                    <td>
                                        <input style={{ verticalAlign: 'middle' }} type="radio" name='rdCall' disabled={calls.skillName ? false : true} />
                                    </td>
                                    <td>{calls.skillName}</td>
                                    <td>{calls.waitingCall}</td>
                                    <td>{calls.waitingTime}</td>
                                </tr>
                            ))
                        }
                    </tbody>
                </table>
                <div className="pagination-wrap">
                    <div style={{ display: 'flex' }}>
                        <span style={currentPage === 1 ? { opacity: 0.3, marginRight: '5px', pointerEvents: 'none' } : { marginRight: '5px', cursor: 'pointer' }} onClick={e => { onPageChange(currentPage - 1) }}>前</span>
                        {(currentPage > 2) &&
                            <span style={{ paginationItem }}>...</span>
                        }
                        {renderPage.map((page, index) =>
                        (
                            <span style={(page) === currentPage ? Object.assign({}, paginationItem, { backgroundColor: '#99CC00', border: '1px solid #99CC00', cursor: 'pointer' }) : Object.assign({}, paginationItem, { cursor: 'pointer' })} onClick={e => { onPageChange(page) }}>{page}</span>
                        ))}
                        {(currentPage + 1 < pages.length) &&
                            <span style={{ paginationItem }}>...</span>
                        }
                        <span style={currentPage >= pages.length ? { opacity: 0.3, marginRight: '5px', pointerEvents: 'none' } : { marginLeft: '5px', cursor: 'pointer' }} onClick={e => { onPageChange(currentPage + 1) }}>次</span>
                    </div>
                </div>
            </div>
            <div className='waiting-list__footer drag-footer'>
                <button className='btn-primary disable'>Answer</button>
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

`


export default React.memo(WaitingList);
