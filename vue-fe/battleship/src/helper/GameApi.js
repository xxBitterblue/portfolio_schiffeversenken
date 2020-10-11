import use_user from "../composable/User"
import * as statics from "./Statics"

const { user } = use_user()

export function start_game(game_id, player_id, ship_list) {
    return fetch(`${statics.game_api_base_path}${game_id}/start`, {
        method: "post",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": "Token " + user.value["user_token"]
        },
        body: JSON.stringify({
                "player_id": player_id,
                "ships": ship_list 
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

export function attack(game_id, player_id, enemy_id, coordinates) {
    return fetch(`${statics.game_api_base_path}${game_id}/attack`, {
        method: "post",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": "Token " + user.value["user_token"]
        },
        body: JSON.stringify({
                "attacked_player_id": enemy_id,
                "coordinates": {
                    "x": coordinates[0],
                    "y": coordinates[1]
                }
            })
    })
    .then( respo => {
        if(!respo.ok) {
            throw new Error(respo)
        } 
        return true
    })
    .catch(reason => {
        return `Failed: ${reason}`
    })
}

export function launch_game(game_id) {
    return fetch(`${statics.game_api_base_path}${game_id}/`, {
        method: "post",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": "Token " + user.value["user_token"]
        }
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