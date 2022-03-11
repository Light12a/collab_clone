import React, { useState, useEffect, useRef } from 'react';
import ProgressBar from "../../components/ProgressBar";
import { useTranslation } from 'react-i18next';
import { Input, Dropdown, Menu, Button, Select, Slider, InputNumber, Checkbox, Form, Modal } from 'antd';
import { useDispatch } from 'react-redux';
import Store from "../../redux/store";
import styled from "styled-components";
// import ReactAudioPlayer from 'react-audio-player'
import ringBackTone from '../../service/sounds/ringbacktone.wav'
import { DownOutlined, UserOutlined } from '@ant-design/icons';
import SettingJB from './SettingJB';
import { version } from '../../../package.json'
import { setCurentRoute } from '../../redux/reducers/route/route';
import HomePage from '../homepage/HomePage';
import arrowIcon from '../../asset/ic.svg'
import { sendMail, clearLogs } from '../../service/sendMailService';

const SettingScreen = () => {
  const [completed, setCompleted] = useState(20);
  const [devices, setDevices] = useState([])
  const [deviceActive, setDeviceActive] = useState([]);
  const [volume, setVolume] = useState(10);

  const { Option } = Select;
  const { t, i18n } = useTranslation();
  const [valueLanguage, setValueLanguage] = useState(t('english'))

  const dispatch = useDispatch()

  const audioRef = useRef();
  const [form] = Form.useForm();

  var ringBackAudio = new Audio();
  ringBackAudio.crossOrigin = "anonymous";

  useEffect(() => {
    console.log("My Store: " + JSON.stringify(Store))
    navigator.mediaDevices.enumerateDevices()
      .then((devices) => {
        // setoutputDevice(devices)
        setDevices(devices)
      })
  }, [])

  useEffect(() => {

    ringBackAudio.volume = volume / 10

    const constraint = {
      audio: { deviceId: deviceActive ? { exact: deviceActive } : undefined },
      // video: {deviceId: videoSource ? {exact: videoSource} : undefined}
    }
    navigator.mediaDevices.getUserMedia(constraint)

  }, [volume])

  const handleClick = (lang) => {
    i18n.changeLanguage(lang)
    setValueLanguage(lang)
  }

  const handleSelectDevice = (value) => {
    console.log("Selected: " + value)
    ringBackAudio.setSinkId(value)
      .then(() => {
        console.log("change audio success")
      })
      .catch(err => {
        console.log("change audio error: ", err)
      })
      ;
  }

  const handleSelectMic = (value) => {
    ringBackAudio.pause();
    const inputAudio = value;
    const constraints = {
      audio: { deviceId: inputAudio ? { exact: inputAudio } : undefined },
      video: false
    };
    try {
      // navigator.mediaDevices.getUserMedia(constraints).then(gotStream).catch(handleError);

    } catch (e) {
      console.log("Error: " + e)
    }
  }

  const handleError = (err) => {
    console.log("The following error occured: " + err.name);
  }

  const onVolumnChange = value => {
    //implement later
  };

  const send = async (reciever) => {
    await sendMail(reciever);
  }

  const onFinish = (values) => {
    form.resetFields();
    if (send(values.email)) {
      Modal.success({
        content: 'Send logs successfully!',
      });
    }
    else {
      Modal.error({
        content: 'Send logs failed!',
      });
    }
  }

  const onFinishFailed = (values) => {
    Modal.error({
      content: 'Send logs failed!',
    });
  }

  const clearLogFiles = () => {
    Modal.confirm({
      title: 'Clear logs',
      content: 'Do you Want to delete log files?',
      onOk() {
        if (clearLogs()) {
          Modal.success({
            content: 'Clear logs successfully!',
          });
        }
        else {
          Modal.error({
            content: 'Clear logs failed!',
          });
        }
      },
      onCancel() {
        //
      },
    });
  }

  return (
    <Wrapper>
      <HomePage />
      <div className='setting'>
        <div className='setting__header'>
          <span>{t('setting')}</span>
          <img src={require('../../asset/Close.svg').default} onClick={() => { dispatch(setCurentRoute("main")) }} alt="" />
        </div>
        <div className='setting__body'>
          <div className='form-group'>
            <p>{t("language")}</p>
            <Select style={{ width: '100%' }} value={valueLanguage} onSelect={(e) => handleClick(e)} defaultValue="en" suffixIcon={<img src={arrowIcon} />}>
              <Option value="en">{t("english")}</Option>
              <Option value="jp">{t("japan")}</Option>
            </Select>
          </div>
          <h1>{t("voiceSetting")}</h1>
          <div className='setting-voice'>
            {/* <div className="App">
          <ProgressBar bgcolor={"#6a1b9a"} completed={completed} />
          <Input
            type='number'
            value={completed}
            onChange={onChangeVolumn}
          />
        </div> */}

            <div>
              <div className='form-group'>
                <p>{t("inputDevice")}</p>
                <Select style={{ width: '100%' }} defaultValue="Choose input device" onSelect={handleSelectMic} suffixIcon={<img src={arrowIcon} />}>
                  {
                    devices.map((item, key) => {
                      if (item.kind === "audioinput") {
                        return (
                          <Option value={item.deviceId}>{item.label}</Option>
                        )
                      }
                    })
                  }
                </Select>
              </div>
              <div className='form-group'>
                <p>{t("inputVolume")}</p>
                <Slider defaultValue={volume * 10} onChange={onVolumnChange} />
              </div>

            </div>
            <div>
              <div className='form-group'>
                <p>{t("outputDevice")}</p>
                <Select style={{ width: '100%' }} onSelect={handleSelectDevice} defaultValue="Choose output device" suffixIcon={<img src={arrowIcon} />}>
                  {
                    devices.map((item, key) => {
                      if (item.kind === "audiooutput") {
                        return (
                          <Option value={item.deviceId}>{item.label}</Option>
                        )
                      }
                    })
                  }
                </Select>
              </div>
              <div className='form-group'>
                <p>{t("outputVolume")}</p>
                <Slider defaultValue={volume * 10} />
              </div>
            </div>
          </div>
          <Checkbox>{t("settingCheckboxDes")}</Checkbox>
          <h1>{t("waitingCallAlert")}</h1>
          <Checkbox>{t("voiceAlert")}</Checkbox>
          {(process.env.REACT_APP_PLATFORM === 'app') &&
            <div>
              <h1>{t("sendLogs")}</h1>
              <Form
                form={form}
                name="basic"
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
              >
                <Form.Item
                  name="email"
                  rules={[
                    {
                      required: true,
                      message: 'Please input your email address!',
                    },
                    {
                      pattern: new RegExp(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/),
                      message: 'Please input correct email address!',
                    },
                  ]}
                >
                  <Input />
                </Form.Item>
                <Button htmlType="submit">Send</Button>
                <Button onClick={e => clearLogFiles()}>Clear logs</Button>

              </Form>
            </div>
          }

          {/* <SettingJB /> */}

        </div>
        <div className='versionStyle'>{t('version')}: {version}</div>
      </div>
    </Wrapper>
  )
}

const Wrapper = styled.div`
    width:100%;
    display: flex;

    .setting{
      flex: 1;
      margin: 20px 0;
      margin-left: 20px;
      background-color: #fff;
      border-radius: 4px;
      border: 1px solid #ECECEC;
      width: 50%;
      overflow: hidden;


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
        padding:16px;

        h1{
          text-transform: uppercase;
          font-size: 14px;
          font-weight: 700;
          margin-top: 32px;
          margin-bottom: 16px;
        }


      }
    }

    .form-group{
      color: #555555;
      font-weight: 500;

      p{
        margin-bottom: 0.25rem;
      }
    }
    .versionStyle {
      color: red;
      margin-top: 35vh;
      flex: 1;
      display: flex;
      justify-content: center;
    }
    .setting-voice{
      display: grid;
      grid-template-columns: 49% 49%;
      gap:2%;

      @media screen and (max-width: 1150px){
        grid-template-columns: 100%;
      }

    }

    .ant-slider{
      margin: 20px 0px !important;
      
    }

    .ant-slider-rail {
      height: 8px;
      background-color: #4E525B;
      border-radius: 4px;
    }
  
    .ant-slider-track {
        height: 8px;
        background-color: #99CC00;
        border-radius: 4px;
    }

    .ant-slider-handle {
        width: 8px;
        height: 24px;
        margin-top: -7px;
        border-radius: 0;
        border:none;
        box-shadow: 0px 0px 9px 2px rgb(0 0 0 / 12%);
    }
`


export default SettingScreen;