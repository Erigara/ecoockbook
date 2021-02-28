import React, {useState, useEffect} from 'react';
import {Form, Input, Button, Modal, Tabs, Space} from 'antd';
import {UserOutlined, LockOutlined, MailOutlined} from '@ant-design/icons';
import {login} from "../api/usersApi";
import {setFormErrors} from "../utils";

const {TabPane} = Tabs;

export function LoginRegisterModal(props = {}) {
    const [visible, setVisible] = useState(false);
    const [display, setDisplay] = useState('block');
    const [activeTab, setActiveTab] = useState("login");
    const {user, setUser} = props;

    const showModal = () => {
        setVisible(true);
    };

    const hideModal = () => {
        setVisible(false);
    }

    const enterLogin = () => {
        setActiveTab("login");
        showModal();
    }

    const enterRegistration = () => {
        setActiveTab("register");
        showModal();
    }

    useEffect(() => {
        if (user === null) {
            setDisplay('block');
        } else {
            setDisplay('none');
            hideModal();
        }
    }, [user])

    return (
        <div style={{display: display}}>
            <Space>
                <Button type="primary" onClick={enterLogin}>
                    Log in
                </Button>
                <Button type="primary" onClick={enterRegistration}>
                    Register
                </Button>
            </Space>
            <Modal
                visible={visible}
                title="Welcome!"
                onCancel={hideModal}
                footer={null}
                width={300}
            >
                <Tabs
                    activeKey={activeTab}
                    onTabClick={(key, _) => {
                        setActiveTab(key)
                    }}
                >
                    <TabPane tab="Log in" key="login">
                        <LoginForm setUser={setUser} enterRegistration={enterRegistration}/>
                    </TabPane>
                    <TabPane tab="Registration" key="register">
                        <RegistrationForm setUser={setUser} enterLogin={enterLogin}/>
                    </TabPane>
                </Tabs>
            </Modal>
        </div>
    );
}

function LoginForm(props = {}) {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const {enterRegistration, setUser} = props;

    const error = () => {
        Modal.error({
            title: 'Authentication Error',
            content: 'Something went wrong with authentication...',
        });
    }

    const onFinish = (values) => {
        setLoading(true);
        login(values).then(res => {
            if (res.status == 200) {
                setUser(res.data);
            }
        }).catch(err => {
            if (err && err.response && err.response.data) {
                setFormErrors(err.response.data, form.getFieldsValue, form.setFields);
            } else {
                error();
            }
        }).finally(() => {
            setLoading(false);
        })
    }

    return (
        <>
            <Form
                form={form}
                name="login"
                className="login-form"
                onFinish={onFinish}
            >
                <Form.Item
                    name="username"
                    rules={[{required: true, message: 'Please input your Username!'}]}
                >
                    <Input prefix={<UserOutlined className="site-form-item-icon"/>} placeholder="Username"/>
                </Form.Item>
                <Form.Item
                    name="password"
                    rules={[{required: true, message: 'Please input your Password!'}]}
                >
                    <Input
                        prefix={<LockOutlined className="site-form-item-icon"/>}
                        type="password"
                        placeholder="Password"
                    />
                </Form.Item>
                <Form.Item>
                    <Button
                        type="primary"
                        htmlType="submit"
                        className="login-form-button"
                        loading={loading}
                    >
                        Log in
                    </Button>
                    Or <a onClick={enterRegistration}>register now!</a>
                </Form.Item>
            </Form>
        </>
    );
}

function RegistrationForm(props = {}) {
    const {onFinish, enterLogin} = props;

    return (
        <Form
            name="registration"
            className="login-form"
            onFinish={onFinish}
        >
            <Form.Item
                name="username"
                rules={[{required: true, message: 'Please input your Username!'}]}
            >
                <Input prefix={<UserOutlined className="site-form-item-icon"/>} placeholder="Username"/>
            </Form.Item>
            <Form.Item
                name="email"
                rules={[
                    {
                        type: 'email',
                        message: 'The input is not valid E-mail!',
                    },
                    {
                        required: true,
                        message: 'Please input your E-mail!',
                    },
                ]}
            >
                <Input
                    prefix={<MailOutlined className="site-form-item-icon"/>}
                    placeholder={"E-mail"}
                />
            </Form.Item>
            <Form.Item
                name="password"
                hasFeedback
                rules={[{required: true, message: 'Please input your Password!'}]}
            >
                <Input.Password
                    prefix={<LockOutlined className="site-form-item-icon"/>}
                    placeholder="Password"
                />
            </Form.Item>
            <Form.Item
                name="confirm"
                dependencies={['password']}
                hasFeedback
                rules={[
                    {
                        required: true,
                        message: 'Please confirm your password!',
                    },
                    ({getFieldValue}) => ({
                        validator(_, value) {
                            if (!value || getFieldValue('password') === value) {
                                return Promise.resolve();
                            }
                            return Promise.reject(new Error('The two passwords that you entered do not match!'));
                        },
                    }),
                ]}
            >
                <Input.Password
                    prefix={<LockOutlined className="site-form-item-icon"/>}
                    placeholder="Confirm Password"
                />
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit" className="login-form-button">
                    Register
                </Button>
                Or <a onClick={enterLogin}>already has account? Log in</a>
            </Form.Item>
        </Form>
    );
}
