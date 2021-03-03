import React, {useState, useEffect} from 'react';
import {Card, Row, Col, Statistic} from "antd";
import {Link} from "react-router-dom";
import ImageCarousel from "./ImageCarousel";
import {UserOutlined, LikeOutlined, LikeTwoTone} from "@ant-design/icons";
import {recipeAuthor, recipeImages, recipeLikes} from "../api/recipesApi";
import Avatar from "antd/es/avatar/avatar";

const {Meta} = Card;


export default function RecipeCard({recipe}) {
    const [images, setImages] = useState();
    const [author, setAuthor] = useState();
    const [likes, setLikes] = useState();

    useEffect(() => {
        recipeImages(recipe).then(res => {
            if (res.status === 200) {
                // TODO: remove results after removing pagination
                setImages(res.data.results);
            }
        })

        recipeAuthor(recipe).then(res => {
            if (res.status === 200) {
                setAuthor(res.data);
            }
        })

        recipeLikes(recipe).then(res => {
            if (res.status === 200) {
                setLikes(res.data);
            }
        })
    }, [recipe]);

    return (
        recipe &&
        <Link to={"/recipes/detail"}>
            <Card
                hoverable
                title={recipe.title}
                cover={<ImageCarousel images={images}/>}
                extra={<Likes likes={likes}/>}
            >
                <Meta
                    avatar={
                        <Avatar icon={<UserOutlined/>} src={author && author.avatar}/>
                    }
                    title={author && `${author.first_name} ${author.last_name}`}
                    description={<Nutrition nutrition={recipe.nutrition}/>}
                />
            </Card>
        </Link>
    );
}

const Likes = ({likes}) => {
    return (
        <>
            {likes &&
            <Statistic
                value={likes.likes_amount}
                prefix={likes.has_like ? <LikeTwoTone twoToneColor="#52c41a"/> : <LikeOutlined/>}
            />}
        </>
    );
}

const Nutrition = ({nutrition}) => {
    const Stat = ({title, value, suffix}) => {
        return (
            <Statistic
                title={title}
                value={value}
                suffix={suffix}
                precision={0}
                valueStyle={{fontSize: "12pt"}}
            />
        );
    }

    return (
        <div>
            {nutrition &&
            <Row>
                <Col span={6}>
                    <Stat title="Calories" value={nutrition.calories} suffix="kcal"/>
                </Col>
                <Col span={6}>
                    <Stat title="Protein" value={nutrition.protein} suffix="g"/>
                </Col>
                <Col span={6}>
                    <Stat title="Carbs" value={nutrition.carbohydrates} suffix="g"/>
                </Col>
                <Col span={6}>
                    <Stat title="Fat" value={nutrition.fat} suffix="g"/>
                </Col>
            </Row>}
        </div>
    );
}