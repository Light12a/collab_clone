import React from "react";
import styled from 'styled-components'
import imgArrow from '../../asset/arrow_green.png'

class CustomSelect extends React.Component {
  constructor(props) {
    super(props);

    // @defaultSelectText => Show default text in select
    // @showOptionList => Show / Hide List options
    // @optionsList => List of options
    this.state = {
      defaultSelectText: "",
      showOptionList: false,
      optionsList: []
    };
  }

  componentDidMount() {
    // Add Event Listner to handle the click that happens outside
    // the Custom Select Container
    document.addEventListener("mousedown", this.handleClickOutside);
    this.setState({
      defaultSelectText: this.props.defaultText
    });
  }

  componentWillUnmount() {
    // Remove the event listner on component unmounting
    document.removeEventListener("mousedown", this.handleClickOutside);
  }

  // This method handles the click that happens outside the
  // select text and list area
  handleClickOutside = e => {
    if (
      !e.target.classList.contains("custom-select-option") &&
      !e.target.classList.contains("selected-text")
    ) {
      this.setState({
        showOptionList: false
      });
    }
  };

  // This method handles the display of option list
  handleListDisplay = () => {
    this.setState(prevState => {
      return {
        showOptionList: !prevState.showOptionList
      };
    });
  };

  // This method handles the setting of name in select text area
  // and list display on selection
  handleOptionClick = e => {
    this.setState({
      defaultSelectText: e.target.getAttribute("data-name"),
      showOptionList: false
    });
  };

  render() {
    const { optionsList } = this.props;
    const { showOptionList, defaultSelectText } = this.state;
    return (
      <CustomSelectWrapper>
        <div
          className={showOptionList ? "selected-text active" : "selected-text"}
          onClick={this.handleListDisplay}
        >
          {defaultSelectText}
        </div>
        {showOptionList && (
          <ul className="select-options">
            {optionsList.map(option => {
              return (
                <li
                  className={`custom-select-option ${defaultSelectText === option.name && 'active'}`}
                  data-name={option.name}
                  key={option.id}
                  onClick={this.handleOptionClick}
                >
                  {option.name}
                </li>
              );
            })}
          </ul>
        )}
      </CustomSelectWrapper>
    );
  }
}

const CustomSelectWrapper = styled.div`
  display: inline-block;
  width: 300px;
  position: relative;
  cursor: pointer;

  .selected-text {
  background-color: #fff;
  padding: 6px 10px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  height: 40px;
}
.selected-text:hover{
    border-color: #b1d923;
}
.selected-text.active {
    color: #bfbfbf;
  }

.selected-text::after {
    position: absolute;
    content: "";
    top: 14px;
    right: 10px;
    width: 0;
    height: 0;
    border: 6px solid transparent;
    background: url(${imgArrow}) no-repeat center #fff;
}

.select-options{
  margin: 0;
  padding: 0;
  z-index: 10;
  margin-top: 2px;
}

.select-options {
  position: absolute;
  width: 100%;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
}

.custom-select-option {
  list-style-type: none;
  padding: 10px;
  background: #fff;
  cursor: pointer;
  border-bottom: 1px solid #ECECEC;
}

.custom-select-option:first-child {
    border-radius: 4px 4px 0 0;
}

.custom-select-option:last-child{
    border-radius: 0 0 4px 4px;
    border: none;
}
  

.custom-select-option:hover {
  background-color: #f5f5f5;
}

.custom-select-option.active{
    background-color: #F7FFE1;
}
`

export default CustomSelect;