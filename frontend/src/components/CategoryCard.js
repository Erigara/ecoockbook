import React from 'react';
import {Card} from "antd";
import {Link} from "react-router-dom";

const {Meta} = Card;


export default function CategoryCard(props = {}) {
    const {category} = props;

    return (
        <Link to={"/categories/detail"}>
            <Card
                hoverable
                cover={<img alt="example" src={category.image}/>}
            >
                <Meta title={category.name}/>
            </Card>
        </Link>
    );
}