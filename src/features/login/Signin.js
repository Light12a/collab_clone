import React, { useState, useEffect } from 'react';
import styled from 'styled-components'
import { calculateMD5, } from 'jssip/lib/Utils';

import logo from '../../asset/logo-clb.svg'
import { Form, Input, message, Button, Space, Checkbox } from 'antd';
import { useDispatch } from 'react-redux';
import { signin } from '../../redux/reducers/authen/auth'
import { appString } from '../../value/string'
import { useTranslation } from 'react-i18next';

import loginLogo from '../../asset/login-logo.svg'


const Signin = () => {


    const { t, i18n } = useTranslation();
    const [isRemember, setIsRemember] = useState(true);
    const [param, setparam] = useState('');
    const [loginError, setLoginError] = useState('')


    const location = window.location.href.split('?');

    // useEffect(() => {
    //     if (process.env.REACT_APP_PLATFORM === 'app') {
    //         require('electron').ipcRenderer.on('ping', (event, message) => {
    //             setparam(message)
    //         })
    //     }
    //     console.log('electron' + param)
    // }, [])

    useEffect(() => {
        if (!isRemember) {
            localStorage.removeItem('userRemember')
        }
    }, [isRemember])

    useEffect(() => {
        if (location[1]) {
            if (!localStorage.getItem('user')) {
                message.error('Please sign in!');
            }
        }
    }, [])

    const dispatch = useDispatch()

    const clearLoginError = () => {
        if (loginError)
            setLoginError('')
    }

    const onFinish = async (e) => {
        clearLoginError()
        // message.success('Submit success!');
        try {
            dispatch(signin({
                body: {
                    ...e,
                    password: calculateMD5(e.password),

                },
                ha1: calculateMD5(`${e.username}:asterisk:${e.password}`),
                setLoginError
            })).then(() => {
                if (isRemember) {
                    localStorage.setItem('userRemember', JSON.stringify({ domain: e.domain, username: e.username }))
                }
            })


        }
        catch (error) {
            if (error.response)
                message.error(error.response.data.message)
            message.error(String(error))
        }
    };

    const handleCheck = (e) => {
        setIsRemember(e.target.checked);
    }


    return (
        <Wrapper>
            <div className='left-login'>
                <img src={logo} alt='clb logo' />
                <img src={loginLogo} alt='login logo' />
            </div>
            <div className='signin'>
                <div className='title'>
                    <h4>LOGIN</h4>
                </div>
                <div className='content'>
                    <Form
                        layout="vertical"
                        onFinish={onFinish}
                        autoComplete="off"
                        requiredMark={false}
                        initialValues={{
                            domain: !localStorage.getItem('userRemember') ? "" : JSON.parse(localStorage.getItem('userRemember')).domain,
                            username: !localStorage.getItem('userRemember') ? "" : JSON.parse(localStorage.getItem('userRemember')).username,
                            remember: !!localStorage.getItem('userRemember'),
                        }}
                    >
                        <Form.Item
                            name="domain"
                            label={t('contract_company_ID')}

                            rules={[
                                { required: true, message: 'Mandatory field' },
                                { type: 'string', min: 1 },
                                { pattern: /^[a-zA-Z0-9_.-]*$/, message: 'Just allow a-zA-Z and . _' }
                            ]}
                        >
                            <Input
                                placeholder={t('enter_ID')}
                                defaultValue={!localStorage.getItem('userRemember') ? "" : JSON.parse(localStorage.getItem('userRemember')).companyId}
                                onFocus={clearLoginError}
                                onChange={clearLoginError}
                            />
                        </Form.Item>
                        <Form.Item
                            name="username"
                            label={t('user_ID')}
                            rules={[
                                { required: true, message: 'Mandatory field' },
                                { type: 'string', min: 6 },
                                { pattern: /^[a-zA-Z0-9_.-]*$/, message: 'Just allow a-zA-Z and . _' }
                            ]}
                        >
                            <Input
                                placeholder={t('holder_enter_user_ID')}
                                defaultValue={!localStorage.getItem('userRemember') ? "" : JSON.parse(localStorage.getItem('userRemember')).userName}
                                onFocus={clearLoginError}
                                onChange={clearLoginError}
                            />
                        </Form.Item>
                        <Form.Item
                            name="password"
                            label={t('password')}
                            className='password'
                            rules={[
                                { required: true, message: 'Mandatory field' },
                                { type: 'string', min: 6 }
                            ]}
                        >
                            <Input.Password
                                placeholder={t('holder_enter_password')}
                                visibilityToggle={false}
                                onFocus={clearLoginError}
                                onChange={clearLoginError}
                            />
                        </Form.Item>
                        <div className='error__area'>
                            <span >
                                {loginError}
                            </span>
                        </div>
                        <Form.Item name="remember" valuePropName="checked" >
                            <Checkbox onChange={handleCheck}>{t('remember_me')}</Checkbox>
                        </Form.Item>

                        <div className='action'>
                            <Button className='btn-brown' type="primary" htmlType="submit" block >
                                {t('login')}
                            </Button>
                        </div>

                    </Form>
                </div>

            </div>
        </Wrapper>
    );
};



const Wrapper = styled.div`
  height:100vh;
  width:100%;
  display: flex;
  justify-content:center;
  align-items:center;

  .left-login {
    background-color: #99CC0012;
    width: 50%;
    height: 100vh;
    display: flex;
    flex-direction: column;
    gap: 64px;
    justify-content: center;
    align-items: center;
  }
  .title {
      display:flex;
      justify-content:center;
      margin-bottom:32px;
      font-weight: 700;
      font-size: 40px;
      text-transform: uppercase;
  }

  .title > h1 {
      margin: 0;
  }

  .signin {
    width: 520px;
    background: white;
    padding: 150px 120px;
    min-height: 580px;
    width:50%;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .signin > div {
      width: 100%;
      max-width: 500px;
  }
  .action {
      display: flex;
      gap:16px;

  }
  .action button {
    box-sizing: border-box;
    border-radius: 4px;
    padding: 1.25rem; 
    display:flex;
    justify-content:center;
    align-items:center;
    background: #99CC00;
    color: #FFFFFF !important;
    font-weight: 700;
    text-transform: uppercase;
    border: none;
    border-radius: 8px;
  }
  .btn-outline {
    background: none;
  }

  .ant-form-item {
      margin-bottom:16px;
    }

    .ant-form-item-label {
        margin-bottom:7px;
        padding:0;
    }
    .ant-form-item-has-error .ant-input, .ant-form-item-has-error :not(.ant-input-affix-wrapper-disabled):not(.ant-input-affix-wrapper-borderless).ant-input-affix-wrapper{
        border-color:#C02323!important;
    }
    .ant-form-item-explain-error,.error__area {
    color: #C02323!important;
    }
    .ant-form-item-has-error label {
        color: #C02323;
    }

  label {
    font-size:14px;
    line-height:16px;
  }
  .ant-input{
      height:40px;
      padding:10px 15px;
      border: 1px solid #C5C5C5;
      border-radius:2px;
  }
  .ant-input-password{
    padding: 10px 15px;
    border: 1px solid #C5C5C5;
    border-radius: 2px;
  }
  .ant-checkbox-wrapper span{
      color:#828282
  }
    .ant-input-affix-wrapper:not(.ant-input-affix-wrapper-disabled):hover {
        border-color: #C5C5C5;
    }
    .ant-input-affix-wrapper:focus, .ant-input-affix-wrapper-focused, .ant-input:focus {
        box-shadow: 0 0 0 2px rgb(0 153 68 / 20%);
    }
    input:not(:placeholder-shown) {
        font-weight: 500;
    }
  @media (max-width: 900px) {
    .signin{
        padding: 30px 40px;
    }
  }
  @media (max-width:600px) {
    .left-login {
        display: none;
    } 
    .signin {
        width: 100%;
    }
    .title > h1 {
      font-size: 50px;
    }
  }
`
export default Signin;