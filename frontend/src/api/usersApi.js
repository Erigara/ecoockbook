const axios = require('axios');

export const login = (credentials) => {
    return axios.post("api/users/login", credentials);
}

export const registration = (credentials) => {
    return axios.post("api/users/registration", credentials);
}

export const getUsers = () => {
    return axios.get('api/users');
}

export const getUser = (id = 'self') => {
    return axios.get(`api/users/${id}`);
}

export const updateUser = (user, data) => {
    return axios.update(user.url, data);
}