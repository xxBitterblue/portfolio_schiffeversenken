<template>
    <div class="board">  
        <h1 v-if="is_player_field">Dein Spielfeld</h1>
        <h1 v-if="!is_player_field">Gegnerisches Spielfeld</h1>  
        <div 
            ref="board_container"
            class="board_container" 
            v-on:click="last_click($event)"
            @dragover.prevent
            @drop.prevent="drop"
        >
            <Ship 
                v-for="ship in ship_list"
                v-bind:key="`${ship.id}`"
                :x="ship.x" :y="ship.y" :life="ship.life" :size="ship.size" :id="ship.id" :alignment="ship.alignment" :started="game_started"
                :dragallowed="!game_started"
                @delete-ship="delete_ship($event)"
                @flip-ship="flip_ship($event)"
            />
            <div
                v-if="last_attack_click" 
                class="last_attack_click"
                :style="{top: last_attack_click[1] + 'px', left: last_attack_click[0] + 'px'}"
            />
        </div>
        <div>
            <button 
                v-if="is_player_field && !game_setup_successful"
                v-on:click="start_game"
            >
                Spiel starten
            </button>
            <button
                v-if="!is_player_field && game_started && current_player_turn"
                v-on:click="attack"
            >
                Angreifen
            </button>
            <p>{{ error_text }}</p>
            <p>{{ information_text }}</p>
        </div>
    </div>
</template>

<script>
import { defineComponent, ref } from "vue"
import Ship from "./Ship"
import * as GameApi from "../../helper/GameApi" 
import * as statics from "../../helper/Statics"
import * as CalculationHelper from "../../helper/CalculationHelper"
import use_user from "../../composable/User"
import use_game from "../../composable/Game"

export default defineComponent ({
    name: 'Board',

    components: {
        Ship
    },

    props: {
        player_field: {type: Boolean, required: true}
    },

    setup(props) {
        const { user } = use_user()
        const { game } = use_game()

        const is_player_field = ref(props.player_field)
        let game_setup_successful = ref(false)
        let game_started = ref(false)
        let information_text = ref("") 
        let error_text = ref("")       
        
        let last_attack_click = ref(null)
        const board_container = ref(null)
        
        const ship_list = ref([])
        const enemy_id = ref("")
        let current_player_turn = ref(false)

        function last_click(e) {
            if (!is_player_field.value) {
                let x = e.pageX - board_container.value.offsetLeft
                let y = e.pageY - board_container.value.offsetTop
                if(!(x + statics.attack_size > statics.board_size || y + statics.attack_size > statics.board_size)){
                    last_attack_click.value = [x, y]
                }
            }
        }

        function drop(e) {
            if (is_player_field.value && !game_started.value) { 
                const ship_id = e.dataTransfer.getData('ship_id')
                const ship_size = parseInt(e.dataTransfer.getData('ship_size'))

                let x = e.pageX - board_container.value.offsetLeft
                let y = e.pageY - board_container.value.offsetTop
                let ship = ship_list.value.find(ship => ship.id == ship_id)
                let alignment = ship ? ship.alignment : statics.horizontal_alignment
                let curr_id = ship ? ship.id : ''

                if (!CalculationHelper.calculate_collision(ship_list, curr_id, x, y, ship_size, alignment)) {
                    if(ship) {
                        const idx = ship_list.value.indexOf(ship)
                        ship_list.value[idx].x = x
                        ship_list.value[idx].y = y
                    } else {
                        let current_ships_life_points = 0

                        ship_list.value.forEach(ship => {
                            current_ships_life_points += ship.life
                        })
                        if ((statics.ship_base_life * ship_size) + current_ships_life_points <= statics.max_ships_life_in_board) {
                            ship_list.value.push({
                                id: `${user.value["user_id"]}_${ship_list.value.length}`,
                                x: x,
                                y: y,
                                life: statics.ship_base_life * ship_size,
                                size: ship_size,
                                alignment: alignment
                            })  
                        } else {
                            error_text.value = "Platzieren des Schiffes nicht möglich. Es würde die maximal erlaubten Lebenspunkte von "+ statics.ship_base_life + "überschreiten."
                        }
                    }
                }  else {
                        error_text.value = "Das Platzieren des Schiffes an dieser Stelle ist nicht erlaubt.."
                }  
            } 
        }

        function delete_ship(ship_id) {
            const ship = ship_list.value.find(ship => ship.id == ship_id)
            const idx = ship_list.value.indexOf(ship)
            ship_list.value.splice(idx,1)
        }

        function flip_ship(event) {
            const ship = ship_list.value.find(ship => ship.id == event.id)
            const idx = ship_list.value.indexOf(ship)
            if (!CalculationHelper.calculate_collision(ship_list, ship.id, ship.x, ship.y, ship.size, event.alignment)) {
                ship_list.value[idx].alignment = event.alignment
            } else {
                error_text.value = "Das Drehen ist an dieser Stelle nicht erlaubt."
            }
        }

        async function start_game() {
            if (ship_list.value.length > 0) {
                let answer = await GameApi.start_game(game.value["game_id"], user.value["user_id"], ship_list.value)
                game_setup_successful.value = true
                if (answer["allPlayersReady"]) {
                    information_text.value = "Das Spiel startet gleich"
                }  else {
                    information_text.value = "Wir warten noch auf deinen Mitspieler"
                }
            } 
        }

        async function attack() {
            if (last_attack_click.value !== null) {
                let answer = await GameApi.attack(game.value["game_id"], user.value["user_id"], enemy_id.value, last_attack_click.value)
                if (answer != true) {
                    error_text.value = answer
                }
            }
        }
        
        function handleMsg(data) {
            const message = data.message

            if (data.type == 'start_game') {
                handle_game_start(message)
            } else if (data.type == 'attack_evaluation') {
                handle_attack_evaluation(message)
            }
        }

        function handle_game_start(message) {
            information_text.value = "Das Spiel startet nun."
            game_started.value = message['start_game']
            enemy_id.value = message['all_player'].find(player => player.id != user.value["user_id"]).id
            current_player_turn.value = message['start_player'] == user.value["user_id"]
            information_text.value = ""
        }

        function handle_attack_evaluation(message) {
            if((message.attacked_player_id == user.value.user_id && is_player_field.value) || (message.attacker_player_id == user.value.user_id && !is_player_field.value)){
                    last_attack_click.value = null
                    information_text.value = "Es wurden " + message['total_hits'] + " Schiffe getroffen!"
                    const affected_ships = message['affected_ships']
                    for (let i = 0; i < affected_ships.length; i++) {
                        const hit_ship = ship_list.value.find(ele => ele.id == affected_ships[i].id)
                        if (hit_ship == undefined) {
                            const ship = {
                                id: String(affected_ships[i]["id"]),
                                x: affected_ships[i]["x"],
                                y: affected_ships[i]["y"],
                                life: affected_ships[i]["life_points"],
                                size: affected_ships[i]["size"],
                                alignment: affected_ships[i]["alignment"]
                                }
                            ship_list.value.push(ship)
                        } else {            
                            const idx = ship_list.value.indexOf(hit_ship)
                            ship_list.value[idx].life = affected_ships[i].life_points
                        }
                    }
                }
            current_player_turn.value = message['attacked_player_id'] == user.value["user_id"]
        }

        return {
            is_player_field,
            information_text,
            game_started,
            game_setup_successful,
            board_container,
            ship_list,
            last_click,
            start_game,
            current_player_turn,
            attack,
            last_attack_click,
            handleMsg,
            drop,
            delete_ship,
            flip_ship,
            error_text
        }
    }
})
</script>

<style>
    div .board {
        float: left;
        width: 50%;
    }
    div .board_container {
        border:1px solid black;
        position: relative;
        width: 400px;
        height: 400px;
        background-image: url('../../assets/Water_Background.png');
        background-repeat: no-repeat;
    }

    div .last_attack_click {
        position: absolute;
        background-color: orange;
        height: 20px;
        width: 20px;
    }
</style>
