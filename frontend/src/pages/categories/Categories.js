import React, {useState, useEffect} from "react";
import {categoryList} from "../../api/recipesApi";
import {message, Pagination} from "antd";
import CardGrid from "../../components/CardGrid";
import CategoryCard from "../../components/CategoryCard";

export default function Categories() {
    const [categories, setCategories] = useState([]);
    const [total, setTotal] = useState(1);

    const getCategories = (page = 1, pageSize = 12) => {
        categoryList(page).then(res => {
            console.log(res);
            if (res.status === 200) {
                setCategories(res.data.results);
                setTotal(res.data.count);
            }
        }).catch(err => {
            message.error("Can't get categories!");
        })
    }
    useEffect(() => {
        getCategories();
    }, []);

    return (
        <>
            <CardGrid cards={categories ? categories.map(value => <CategoryCard category={value}/>) : []}/>
            <Pagination
                showSizeChanger={false}
                hideOnSinglePage={true}
                pageSize={12}
                total={total}
                onChange={getCategories}
            />
        </>
    );
}