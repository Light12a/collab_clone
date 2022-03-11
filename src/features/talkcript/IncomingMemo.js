import React, {useEffect, useState} from 'react'
import { useTranslation } from 'react-i18next';
import styled from 'styled-components'
import HomePage from '../homepage/HomePage'
import { useDispatch, useSelector } from 'react-redux';
import { setCurentRoute } from '../../redux/reducers/route/route';
import { Modal, Select } from 'antd';
import arrowIcon from '../../asset/ic.svg'
import {getCorrespondence} from '../../redux/reducers/talkscript/correspondence'

const IncomingMemo = () => {
  const { Option } = Select;
  const [isVisible, setIsVisible] = useState(false)
  const { t, i18n } = useTranslation();
  const dispatch = useDispatch();
  const {activeCall} = useSelector(state => state.currentCall)
  const { token: { token } } = useSelector(state => state.auth)

  const {correspondenceMemo} = useSelector(state => state.correspondence)

  useEffect(() => {
    if(activeCall.state === "END") {
      setIsVisible(true)
    }
  }, [activeCall.state])
  
  // useEffect(() => {
  //   dispatch(getCorrespondence(token))
  // },[])
  

  const content = [
    {
      "name": "Salesperson",
      "content": "Hello, [Prospect name]. My name is Michael Halper and I help hiring managers like you reduce the time it takes to interview, hire, and onboard new talent in 50% less time than the industry average. How many new hires do you have planned for the year?"
    },
    {
      "name": "Prospect",
      "content": "Well, my department has the budget for seven new hires in 2019."
    },
    {
      "name": "Salesperson",
      "content": "What's your biggest pain point in the hiring process right now?"
    },
    {
      "name": "Prospect",
      "content": "I've got a million other things going on, and finding qualified candidates has been a challenge. We need to get these positions filled, but I'm having a hard time making it a priority with everything else on my plate."
    },
    {
      "name": "Salesperson",
      "content": "I hear that a lot. I'd love to set up a 10-minute call to learn more about your goals this year, and share how Recruiters International might be able to help. What about this Thursday?"
    },
    {
      "name": "Prospect",
      "content": "Um, sure. I think I've got an 11:00 open."
    }
  ]


  return (
    <Wrapper>
      <HomePage />
      <div className='incoming'>
        <div className='incoming__header'>
          <span>{t('taskscript')}</span>
          <img src={require('../../asset/Close.svg').default} onClick={() => { dispatch(setCurentRoute("main")) }} alt="" />
        </div>
        <div className='incoming__body'>
          <div className='incoming__body__top'></div>
          <div className='incoming__body__content'>
            <h3>Sales Call Script Sample</h3>
            {
              content.map((item) => (
                <div className='group'>
                  <span className='name'>{item.name}: </span>
                  <span>{item.content}</span>
                </div>
              ))
            }
          </div>
        </div>

      </div>


      <Modal title={t("correspondence_Memo")} visible={false} cancelButtonProps={{style: {display:'none'}}} okButtonProps={{style:{borderRadius: "8px"}}}>
        <div className='form-group'>
          <span>{t("correspondence_Memo")}</span>
          <Select style={{ width: '100%' }} defaultValue="Manual Registration" suffixIcon={<img src={arrowIcon} />}>
              <Option value="Manual Registration">Manual Registration</Option>
            </Select>
        </div>
        <div className='form-group'>
          <span>{t("manual_correspondence_memo_input")}</span>
          <Select style={{ width: '100%' }} defaultValue="Input correspondence memo" suffixIcon={<img src={arrowIcon} />}>
              <Option value="Input correspondence memo">Input correspondence memo</Option>
            </Select>
        </div>
      </Modal>

      <Modal title={t("correspondence_Memo")} visible={isVisible} onCancel={() => setIsVisible(false)} cancelButtonProps={{style: {display:'none'}}} okButtonProps={{style:{borderRadius: "8px"}}}>
        <div className='form-group'>
          <span>{t("correspondence_Memo")}</span>
          <Select style={{ width: '100%' }} placeholder="Select correspondence memo" suffixIcon={<img src={arrowIcon} />}>
              {
                correspondenceMemo.memo.map((item)=>(
                  <Option value={item.id}>{item.text}</Option>
                ))
              }
            </Select>
        </div>
      </Modal>
    </Wrapper>
  )
}

const Wrapper = styled.div`
  width:100%;
  display: flex;

  .incoming{
    flex: 1;
    margin: 20px 0;
    margin-left: 20px;
    background-color: #fff;
    border-radius: 4px;
    border: 1px solid #ECECEC;
    position: relative;

    &__header{
      border-bottom: 1px solid #EEEEEE;
      padding: 15px 16px;
      display: flex;
      justify-content: space-between;
      border-radius: 4px 4px 0 0 ;

      span{
        text-transform: uppercase;
        font-weight: 700;
        font-size: 20px;
      }
      img{
        cursor: pointer;
      }
    }

    &__body{
      margin:16px;
      background-color: #FCF3A7;
      border: 1px solid #EEEEEE;
      border-radius: 4px;
      height: calc(100% - 95px);
      overflow: hidden;
      position: absolute;

      &__top{
        height: 15px;
        background-color: #FAE860;
      }

      &__content{
        padding: 15px;
        height: 100%;
        overflow: auto; 

        h3{
          font-weight: 700;
        }

        .group:not(:last-child){
          margin-bottom: 16px;

        }
        span{
          font-size: 14px;
        }
        .name{
          font-weight: 700;
        }
      }
    }
  }


`

export default IncomingMemo