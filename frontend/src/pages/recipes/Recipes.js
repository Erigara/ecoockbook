import React, {useState, useEffect} from "react";
import {recipeList} from "../../api/recipesApi";
import {message, Pagination} from "antd";
import CardGrid from "../../components/CardGrid";
import RecipeCard from "../../components/RecipeCard";


export default function Recipes({kind}) {
    const [recipes, setRecipes] = useState([]);
    const [total, setTotal] = useState(1);

    const getRecipes = (page = 1, pageSize = 12) => {
        recipeList(page, kind).then(res => {
            console.log(res);
            if (res.status === 200) {
                setRecipes(res.data.results);
                setTotal(res.data.count);
            }
        }).catch(err => {
            message.error("Can't get recipes!");
        })
    }

    useEffect(() => {
        getRecipes();
    }, []);

    return (
        <>
            <CardGrid cards={recipes ? recipes.map(value => <RecipeCard recipe={value}/>) : []}/>
            <Pagination
                showSizeChanger={false}
                hideOnSinglePage={true}
                pageSize={12}
                total={total}
                onChange={getRecipes}
            />
        </>
    );
}