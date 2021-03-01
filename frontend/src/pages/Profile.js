import React, {useState} from 'react';
import {Avatar, Button, Col, Divider, Drawer, Empty, Form, Row, Input, Modal} from "antd";
import {PlusOutlined} from '@ant-design/icons';
import {updateUser} from "../api/usersApi";
import {setFormErrors} from "../utils";


export default function Profile(props = {}) {
    const {user, setUser} = props;
    const [drawerVisible, setDrawerVisible] = useState(false);

    return (
        user !== null
            ? <>
                <div style={{display: "inline-block", float: "left"}}>
                    <h1 className="site-description-item-profile-p">
                        User Profile
                    </h1>
                </div>
                <div style={{display: "inline-block", float: "right"}}>
                    <Button type="primary" onClick={() => setDrawerVisible(true)}>
                        <PlusOutlined/> Edit profile
                    </Button>
                </div>
                <EditProfile visible={drawerVisible} setVisible={setDrawerVisible} user={user} setUser={setUser}/>
                <Divider plain>Personal</Divider>
                <Row>
                    <Col span={12}>
                        <DescriptionItem title="Username" content={user.username}/>
                        <DescriptionItem title="Email" content={user.email}/>
                        <DescriptionItem title="Full Name" content={`${user.first_name} ${user.last_name}`}/>
                    </Col>
                    <Col span={12}>
                        <Avatar size={128} src={user.avatar}/>
                    </Col>
                </Row>
                <Divider plain>About</Divider>
                <p className="site-description-item-profile-p">{user.about}</p>
            </>
            : <Empty description="Log in to see profile"/>
    );
}

function EditProfile(props = {}) {
    const {user, setUser} = props;
    const {visible, setVisible} = props;
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);

    const hideDrawer = () => {
        setVisible(false);
    }

    const showDrawer = () => {
        setVisible(true);
    }

    const error = () => {
        Modal.error({
            title: 'Edit Profile Error',
            content: 'Something went wrong during profile update...',
        });
    }

    const onFinish = (values) => {
        setLoading(true);
        updateUser(user, values).then(res => {
            if (res.status === 200) {
                setUser(res.data);
                hideDrawer();
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
            <Drawer
                title="Edit profile"
                width={720}
                onClose={hideDrawer}
                visible={visible}
                bodyStyle={{paddingBottom: 80}}
                footer={
                    <div
                        style={{
                            textAlign: 'right',
                        }}
                    >
                        <Button onClick={hideDrawer} style={{marginRight: 8}}>
                            Cancel
                        </Button>
                        <Button
                            form="edit-profile-form"
                            key="submit"
                            htmlType="submit"
                            type="primary"
                            loading={loading}
                        >
                            Submit
                        </Button>
                    </div>
                }
            >
                <Form
                    id="edit-profile-form"
                    layout="vertical"
                    form={form}
                    onFinish={onFinish}
                    hideRequiredMark
                >
                    <Row gutter={16}>
                        <Col span={12}>
                            <Form.Item
                                name="first_name"
                                label="First name"
                                rules={[{required: true, message: 'Please enter first name'}]}
                                initialValue={user.first_name}
                            >
                                <Input placeholder="Please enter first name"/>
                            </Form.Item>
                        </Col>
                        <Col span={12}>
                            <Form.Item
                                name="last_name"
                                label="Last name"
                                rules={[{required: true, message: 'Please enter last name'}]}
                                initialValue={user.last_name}
                            >
                                <Input placeholder="Please enter last name"/>
                            </Form.Item>
                        </Col>
                    </Row>
                    <Row gutter={16}>
                        <Col span={24}>
                            <Form.Item
                                name="email"
                                label="Email"
                                rules={[
                                    {
                                        type: 'email',
                                        message: 'The input is not valid E-mail!',
                                    },
                                    {
                                        required: true,
                                        message: 'Please enter your E-mail',
                                    },
                                ]}
                                initialValue={user.email}
                            >
                                <Input placeholder="Please enter your E-smail"/>
                            </Form.Item>
                        </Col>
                    </Row>
                    <Row gutter={16}>
                        <Col span={24}>
                            <Form.Item
                                name="about"
                                label="About"
                                initialValue={user.about}
                            >
                                <Input.TextArea rows={4} placeholder="please, write something about yourself"/>
                            </Form.Item>
                        </Col>
                    </Row>
                </Form>
            </Drawer>
        </>
    );
}

const DescriptionItem = ({title, content}) => (
    <div className="site-description-item-profile-wrapper">
        <p className="site-description-item-profile-p-label">{title}:</p>
        {content}
    </div>
);