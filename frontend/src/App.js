import React, {useState, useEffect} from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";
import {render} from "react-dom";
import {Layout, Menu, Typography} from 'antd';
import {UserOutlined, LogoutOutlined} from '@ant-design/icons';

import './App.css';
import {LoginRegisterModal} from "./components/Login";
import MainMenu from "./components/MainMenu";
import ProfileMenu from "./components/ProfileMenu";
import {getUser} from "./api/usersApi";


const {Header, Content, Sider, Footer} = Layout;
const {Title} = Typography;
const {SubMenu} = Menu;


export default function App() {
    const [user, setUser] = useState(null);

    // try to get current user
    useEffect(() => {
       getUser().then(res => {
           console.log(res);
           if (res.status == 200) {
               setUser(res.data);
           }
       })
    }, []);


    return (
        <>
            <Router>
                <Layout className="layout">
                    <Header>
                        <Title className="logo" style={{color: 'white'}}>
                            eCookBook
                        </Title>
                        <div className="header-inline">
                            <LoginRegisterModal user={user} setUser={setUser}/>
                            <ProfileMenu user={user} setUser={setUser}/>
                        </div>
                    </Header>
                    <Layout>
                        <Sider className="site-layout-background" width={200}>
                            <MainMenu/>
                        </Sider>
                        <Content style={{padding: '0 50px'}}>
                            <div className="site-layout-content">
                                <Switch>
                                    <Route path="/categories">
                                        <Categories/>
                                    </Route>
                                    <Route path="/user">
                                        <User/>
                                    </Route>
                                    <Route path="/own">
                                        <Recipes kind={"own"}/>
                                    </Route>
                                    <Route path="/feed">
                                        <Recipes kind={"feed"}/>
                                    </Route>
                                    <Route path="/favorites">
                                        <Recipes kind={"favorites"}/>
                                    </Route>
                                    <Route path="/">
                                        <Home/>
                                    </Route>
                                </Switch>
                            </div>
                        </Content>
                    </Layout>
                    <Footer style={{textAlign: 'center'}}>eCookBook©2020 Created by Erigara</Footer>
                </Layout>
            </Router>
        </>
    )
}

function Home() {
    return <h2>Home</h2>;
}

function Categories() {
    return <h2>Categories</h2>;
}

function User() {
    return <h2>User</h2>;
}

function Recipes(props = {}) {
    const {kind} = props;
    return <h2>{kind}</h2>;
}

const container = document.getElementById("app");
render(<App/>, container);