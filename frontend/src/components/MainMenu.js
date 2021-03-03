import React from "react";
import {Link} from "react-router-dom";
import {Menu} from 'antd';
import {LaptopOutlined, NotificationOutlined} from '@ant-design/icons';

const {SubMenu} = Menu;

export default function MainMenu() {
    return (
        <Menu
            mode="inline"
            style={{height: '100%'}}
        >
            <Menu.Item icon={<LaptopOutlined/>} key="categories">
                <Link to="/categories">Categories</Link>
            </Menu.Item>
            <SubMenu key="recipes" icon={<NotificationOutlined/>} title="Recipes">
                <Menu.Item key="own">
                    <Link to="/recipes/own">Own</Link>
                </Menu.Item>
                <Menu.Item key="feed">
                    <Link to="/recipes/feed">Feed</Link>
                </Menu.Item>
                <Menu.Item key="favorites">
                    <Link to="/recipes/favorites">Favorites</Link>
                </Menu.Item>
            </SubMenu>
        </Menu>
    );
}