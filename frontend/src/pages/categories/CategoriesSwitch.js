import React from "react";
import {Switch, Route, useRouteMatch} from "react-router-dom";
import Categories from "./Categories";

export default function CategoriesSwitch() {
    let match = useRouteMatch();

    return (
        <Switch>
            <Route exact path={match.path}>
                <Categories/>
            </Route>
            <Route path={`${match.path}/:categoryId`}>
                <h3>Please select a topic.</h3>
            </Route>
        </Switch>
    );
}