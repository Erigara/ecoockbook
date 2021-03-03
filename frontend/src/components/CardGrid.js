import React from 'react';
import {Row, Col} from "antd";


export default function CardGrid(props = {}) {
    const {cards} = props;

    const createCardGrid = (cards) => {
        let width = 4;
        let cols = cards.map(value => <Col span={6} style={{padding: 24}}>{value}</Col>);
        let rows = toMatrix(cols, width).map(value => {
            return (
                <Row>
                    {value}
                </Row>
            );
        });

        return (
            <>
                {rows}
            </>
        );
    }

    return createCardGrid(cards);
}

const toMatrix = (arr, width) =>
    arr.reduce((rows, key, index) => (index % width == 0 ? rows.push([key])
        : rows[rows.length - 1].push(key)) && rows, []);