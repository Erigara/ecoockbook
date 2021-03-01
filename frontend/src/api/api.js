import Cookies from 'js-cookie'

export const axios = require('axios');

axios.interceptors.request.use(config => {
    let csrftoken = Cookies.get('csrftoken');
    if (csrftoken !== undefined) {
        config.headers.post['X-CSRFToken'] = csrftoken;
        config.headers.put['X-CSRFToken'] = csrftoken;
    }
    return config;
});