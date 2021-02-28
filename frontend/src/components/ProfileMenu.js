import React, {useEffect, useState} from "react";
import {Avatar, Menu} from 'antd';
import {UserOutlined, LogoutOutlined} from '@ant-design/icons';

const {SubMenu} = Menu;

export default function ProfileMenu(props = {}) {
    const [display, setDisplay] = useState('block');
    const {user, setUser} = props;

    const handleClick = (e) => {
        switch (e.key) {
            case "profile":
                //
                break;
            case "logout":
                setUser(null);
                break;
        }
    }

    useEffect(() => {
        if (user !== null) {
            setDisplay('block');
        } else {
            setDisplay('none');
        }
    }, [user])

    return (
        <div style={{display: display}}>
            <Menu
                mode="horizontal"
                theme="dark"
                onClick={handleClick}
            >
                <SubMenu
                    key="SubMenu"
                    icon={<Avatar size="large" src={user !== null ? user.avatar : ""}/>}
                    title={`  ${user !== null ? user.username : ""}`}
                >
                    <Menu.Item key="profile" icon={<UserOutlined/>}>Profile</Menu.Item>
                    <Menu.Item key="logout" icon={<LogoutOutlined/>}>Log out</Menu.Item>
                </SubMenu>
            </Menu>
        </div>
    );
}