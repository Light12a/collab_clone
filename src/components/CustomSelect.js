import React from "react";
import styled from 'styled-components'
import imgArrow from '../asset/arrow_green.png'
import { withTranslation } from 'react-i18next';

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
  handleOptionClick = (group, e) => {
    if (group) {
      this.setState({
        defaultSelectText: e.target.getAttribute("data-name"),
        showOptionList: false
      });
      this.props.onSelectGroup(group);
    }
    else {
      this.setState({
        defaultSelectText: this.props.t('all'),
        showOptionList: false
      });
      this.props.onSelectGroup({
        "group_id": -1,
        "group_name": "All"
      });
    }
  };

  render() {
    const { optionsList } = this.props;
    const { showOptionList, defaultSelectText } = this.state;
    const { t } = this.props;
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
            <li
              className={`custom-select-option ${defaultSelectText === 'All' && 'active'}`}
              onClick={e => this.handleOptionClick(null, e)}
            >{t('all')}
            </li>
            {optionsList.map(option => {
              return (
                <li
                  className={`custom-select-option ${defaultSelectText === option.group_name && 'active'}`}
                  data-name={option.group_name}
                  key={option.group_id}
                  onClick={e => this.handleOptionClick(option, e)}
                >
                  {option.group_name}
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
  max-height: 250px; 
  overflow: auto;
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
export default withTranslation()(CustomSelect);