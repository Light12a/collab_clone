import { React, useState } from 'react'
import '../features/agentList/AgentListScreen.css'
import searchIcon from '../asset/search.svg'
// import searchIcon from '../asset/search.svg'
const SearchBar = (props) => {
    const[textSearch, setTextSearch] = useState('56');

    function handleChangeTextSearch(){
        console.log("in my search text")
        
        // getTextSearch(text)
    }
    return (
        <div className='search'>
            <input
                placeholder={props.t('holderInputSearch')}
                onChange={props.onSearch()}
                
                // value= {textSearch}
            ></input>
            {
                props.isSearching ?
                <div className='iconSearchDelete'>X</div>
                :
                <img
                src={searchIcon}
                onClick={() => alert('hi')}
                className='iconSearch'
            />
            }
           
        </div>
    )

}

export default SearchBar;