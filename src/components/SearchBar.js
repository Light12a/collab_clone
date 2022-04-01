import styled from 'styled-components';
import searchIcon from '../asset/search.png'

import React from 'react'
// import searchIcon from '../asset/search.svg'
class SearchBar extends React.Component {
    constructor(props) {
        super(props);
    }
    // import searchIcon from '../asset/search.svg'

    render() {
        return (
            <Wrapper>
                <input
                    placeholder={this.props.t('holderInputSearch')}
                    onChange={this.props.onSearch()}
                    className="input"
                // value= {textSearch}
                ></input>
                {
                    this.props.isSearching ?
                        <div className='iconSearchDelete'>X</div>
                        :
                        <img
                            // onClick={() => alert('hi')}
                            src={searchIcon}
                            className='iconSearch'
                        ></img>
                }
            </Wrapper>
        )
    }
}
const Wrapper = styled.div`

height: 40px;
    width: 376px;
    border: 1px solid #CDCDCD;
    border-radius: 4px;
    display: flex;
    align-items: center;
.iconSearch {
    width: 20px;
    height: 20px;
    filter: brightness(0) saturate(100%) invert(81%) sepia(45%) saturate(2330%) hue-rotate(24deg) brightness(90%) contrast(101%);
    margin: 10px;
    /* background: url(${searchIcon}) no-repeat center; */
    cursor: pointer;
}
.iconSearchDelete{
    font-weight: bold;
    margin-right: 1vw;
    font-size: 3.2vh;
}
    
 .input{
    outline: none;
    width: 100%;
    border: none;
    border-radius: 4px;
    /* padding: 11px 16px; */
}
`
export default SearchBar;