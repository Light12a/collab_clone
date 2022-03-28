import { React, useEffect, useState } from 'react'
import '../features/agentList/AgentListScreen.css'
import styled from 'styled-components';

const Pagination = (props) => {

    const [pageNumber, setPageNumber] = useState([]);
    let [currentPage, setCurrentPage] = useState(1)

    const {total, itemsPerPage, t} = props

    const totalPageNumber = Math.floor(total.length/itemsPerPage) + 1
    // totalPageNumber !== 1 ? setPageNumber([1,2,3]) : setPageNumber([1])
    // console.log("My PageNumber: " + pageNumber)
    useEffect(()=>{
        renderPageNumber(1)
    }, [])

    const renderPageNumber = (page)=> {
        setCurrentPage(page)
        props.onPageChange(page)
        let maxPageNumber = 3;
        if (totalPageNumber < maxPageNumber) {
            maxPageNumber = totalPageNumber;
        }

        if (page === 1) {
            for (let i = 0; i < maxPageNumber; i++) {
                pageNumber.splice(i, 1, i + 1);
            }
        }
        else if (page === totalPageNumber) {
            for (let i = 0; i < maxPageNumber; i++) {
                pageNumber.splice(i, 1, totalPageNumber - 2 + i);
            }
        }
        else {
            for (let i = 0; i < maxPageNumber; i++) {
                pageNumber.splice(i, 1, page - 1 + i);
            }
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
        <Wrapper>

            <div className="pagination-wrap">
                <div style={{ display: 'flex' }}>
                <span
                        style={currentPage === 1 ?
                            { opacity: 0.3, marginRight: '5px', pointerEvents: 'none' }
                            : { marginRight: '5px', cursor: 'pointer' }}
                        onClick={e => { renderPageNumber(1) }}
                    >{t('first')}</span>
                    <span
                        style={currentPage === 1 ?
                            { opacity: 0.3, marginRight: '5px', pointerEvents: 'none' }
                            : { marginRight: '5px', cursor: 'pointer' }}
                        onClick={e => { renderPageNumber(currentPage - 1) }}
                    > {t('previous')}</span>


                    {(currentPage > 2) &&
                        <span style={{ paginationItem }}>...</span>
                    }

                    {pageNumber.map((page, index) =>
                    (
                        <span style={(page) === currentPage
                            ? Object.assign({}, paginationItem,
                                { backgroundColor: '#99CC00', border: '1px solid #99CC00', cursor: 'pointer' })
                            : Object.assign({}, paginationItem, { cursor: 'pointer' })}
                            onClick={e => { renderPageNumber(page) }}
                        >{page}</span>
                    ))}

                    {(currentPage + 1 < totalPageNumber) &&
                    
                        <span style={{ paginationItem }}>...</span>
                        
                    }


                    <span style={currentPage >= totalPageNumber
                        ? { opacity: 0.3, marginRight: '5px', pointerEvents: 'none' }
                        : { marginLeft: '5px', cursor: 'pointer' }}
                        onClick={e => { renderPageNumber(currentPage + 1) }}
                    >{t('next')}</span>
                    <span style={currentPage >= totalPageNumber
                        ? { opacity: 0.3, marginRight: '5px', pointerEvents: 'none' }
                        : { marginLeft: '5px', cursor: 'pointer' }}
                        onClick={e => { renderPageNumber(totalPageNumber) }}
                    > {t('last')}</span>
                </div>
            </div>

        </Wrapper>
    )

}
const Wrapper = styled.div`
    .pagination-wrap{
            margin-top: 12px;
            display:flex;
            flex-direction: row-reverse;
        }
`
export default Pagination;