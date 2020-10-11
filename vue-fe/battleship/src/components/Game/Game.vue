<template>
    <div>
        <div v-if="is_logged_in">
            <ShipContainer />
            <Score ref="score_display"/> 
            <div>
                <Board ref="player_board" :player_field="true"/>
                <Board ref="enemy_board" :player_field="false"/>
            </div>
        </div>
        <div v-else>
            <p>Bitte logge dich ein bevor du spielen kannst.</p>
            <router-link :to="`/`">Zum Login</router-link>
        </div>
    </div>
</template>

<script>
import {defineComponent, onMounted, ref} from "vue"
import Board from "./Board"
import Score from "./Score"
import ShipContainer from "./ShipContainer"
import use_user from "../../composable/User"
import use_game from "../../composable/Game"
import router from "@/router"

    export default defineComponent ({
        name: "Game",

        components: {
                Board,
                ShipContainer,
                Score
        },

        setup() {
            const { user } = use_user()
            const { game } = use_game()
            let is_logged_in = ref(false)
            const player_board = ref(null)
            const enemy_board = ref(null)
            const score_display = ref(null)

            onMounted(() => {
                if (game.value["game_socket"]) {
                    game.value["game_socket"].onmessage = handleMsg
                } else {
                    console.error("Error: No socket")
                }
                is_logged_in.value = true//user.value[`is_logged_in`]
            })

            function handleMsg(e) {
                const data = JSON.parse(e.data)

                if (data.type == 'game_finished') {
                    const winner = data.message['winner_player_id']
                    router.push(`/endscreen/${winner}`)
                }

                score_display.value.handle_score_changes(e)
                enemy_board.value.handleMsg(data)
                player_board.value.handleMsg(data)          
            }

            return {
                user,
                player_board,
                enemy_board,
                score_display,
                is_logged_in
            }
        }
    })
</script>