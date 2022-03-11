import { React, useState } from 'react'
import '../features/agentList/AgentListScreen.css'
import searchIcon from '../asset/search.svg'

const SearchBar = (props) => {


    return (
        <div className='search'>
            <input
                placeholder={props.t('holderInputSearch')}
                onChange={props.onSearch()}

            ></input>
            <img
                src={searchIcon}
                onClick={() => alert('hi')}
                className='iconSearch'
            />
        </div>
    )

}

export default SearchBar;