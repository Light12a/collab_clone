import React, { useEffect, useRef } from 'react';
import { Form, Button, InputNumber } from 'antd';
import { useSelector } from 'react-redux';
import axios from 'axios'

const SettingJB = () => {
    const hasJBRef = useRef(false)
    const { user: { userName } } = useSelector(state => state.auth)
    useEffect(() => {
        axios.get(` http://13.113.23.145:8000/api/jitterbuffer?username=${userName}`)
            .then(({ data }) => data.status ? hasJBRef.current = true : hasJBRef.current = false)
    }, [userName])
    const onFinish = async (values) => {
        let data
        if (hasJBRef.current) {
            const data = await axios.put(`http://13.113.23.145:8000/api/jitterbuffer?username=${userName}`, { jitterbuffer: values.size })
        } else {
            const data = await axios.post('http://13.113.23.145:8000/api/jitterbuffers', { username: userName, jitterbuffer: values.size })
            hasJBRef.current = true
        }
    };

    const onFinishFailed = (errorInfo) => {
        console.log('Failed:', errorInfo);
    };
    return (
        <div>
            <Form
                name="basic"
                labelCol={{ span: 16 }}
                wrapperCol={{ span: 8 }}
                initialValues={{ remember: true }}
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
                autoComplete="off"
            >
                <Form.Item
                    label="jitter buffer maxsize"
                    name="size"
                // rules={[{ required: true, message: 'Please input your username!' }]}
                >
                    <InputNumber min={0} max={200} defaultValue={'default'} />
                </Form.Item>

                <Form.Item wrapperCol={{ offset: 16, span: 8 }}>
                    <Button type="primary" htmlType="submit">
                        Submit
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
};

export default SettingJB;