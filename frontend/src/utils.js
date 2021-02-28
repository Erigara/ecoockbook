const convertErrors = (values, keys = [], res = []) => {
    if (Array.isArray(values)) {
        res.push({key: [...keys], value: values})
    } else if (typeof values === 'object') {
        for (let [key, value] of Object.entries(values)) {
            keys.push(key);
            convertErrors(value, keys, res);
            keys.pop()
        }
    }
    return res
};

export const setFormErrors = (errors, getFieldsValue, setFields) => {
    if (errors && Object.keys(errors).length !== 0) {
        let errorsObj = convertErrors(errors);
        for (let err of errorsObj) {
            setFields(
                [{
                    'name': err.key,
                    'errors': err.value
                }]
            )
        }
    }
};