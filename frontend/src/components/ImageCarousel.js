import React from "react";
import {Carousel} from "antd";

export default function ImageCarousel({images}) {
    return (
        <Carousel
            dots={false}
            autoplay
        >
            {images && images.map(image => <img alt="example" src={image.image}/>)}
        </Carousel>
    );
}