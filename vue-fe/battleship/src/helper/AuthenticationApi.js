import * as statics from "./Statics"

export function login(username, password) {
    return fetch(`${statics.auth_api_base_path}login/`, {
        method: "post",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
                "username": username,
                "password": password 
            })
    })
    .then( respo => {
        if(!respo.ok) {
            throw new Error(respo.statusText)
        } 
        return respo.json()
    })
    .catch(reason => {
        return `Failed: ${reason}`
    })
}

export function register(username, password) {
    return fetch(`${statics.auth_api_base_path}register/`, {
        method: "post",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
                "username": username,
                "password": password 
            })
    })
    .then( respo => {
        if(!respo.ok) {
            throw new Error(respo.statusText)
        } 
        return true
    })
    .catch(reason => {
        return `Failed: ${reason}`
    })
}