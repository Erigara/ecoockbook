import React from "react";
import {Switch, Route, useRouteMatch} from "react-router-dom";
import Recipes from "./Recipes";

export default function RecipesSwitch() {
    let match = useRouteMatch();

    return (
        <Switch>
            <Route key="own" exact path={`${match.path}/own`}>
                <Recipes kind="own"/>
            </Route>
            <Route key="feed" exact path={`${match.path}/feed`}>
                <Recipes kind="feed"/>
            </Route>
            <Route key="favorites" exact path={`${match.path}/favorites`}>
                <Recipes kind="favorites"/>
            </Route>
            <Route path={`${match.path}/:recipeId`}>
                <h3>Please select a topic.</h3>
            </Route>
        </Switch>
    );
}