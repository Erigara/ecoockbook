import React, {useEffect, useState} from "react";
import {Avatar, Menu} from 'antd';
import {UserOutlined, LogoutOutlined} from '@ant-design/icons';
import {logout} from "../api/usersApi";
import {Link, useHistory} from "react-router-dom";

const {SubMenu} = Menu;

export default function ProfileMenu(props = {}) {
    const history = useHistory();
    const [display, setDisplay] = useState('block');
    const {user, setUser} = props;

    const handleClick = (e) => {
        switch (e.key) {
            case "profile":
                history.push("/profile");
                break;
            case "logout":
                logout().then(res => {
                    if (res.status === 200) {
                        setUser(null);
                        history.push("/");
                    }
                }).catch(err => {
                    console.log(err);
                });
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