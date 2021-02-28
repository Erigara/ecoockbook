const axios = require('axios');

export const feed = () => {
    return axios.get("api/cookbook/recipes/feed/");
}

export const recipeLikes = (recipe) => {
    const {likes} = recipe;
    return axios.get(likes);
}

export const recipeAuthor = (recipe) => {
    const {author} = recipe;
    return axios.get(author);
}

export const recipeImages = (recipe) => {
    const {images} = recipe;
    return axios.get(images);
}

export const recipeProducts = (recipe) => {
    const {products} = recipe;
    return axios.get(products);
}

export const recipeSteps = (recipe) => {
    const {steps} = recipe;
    return axios.get(steps);
}

export const recipeComments = (recipe) => {
    const {comments} = recipe;
    return axios.get(comments);
}
