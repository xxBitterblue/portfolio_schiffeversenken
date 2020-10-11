<template>
    <div>
        <div v-if="is_logged_in">
            <label>Spiel starten oder beitreten</label>
            <input type="text" required v-model="game_name"/>
            <button v-on:click="launch_game">Bestätigen</button> 
            <p v-if="failure_msg">{{ failure_msg }}</p>
            <p v-if="success_msg">{{ success_msg }}</p>
        </div>
        <div v-else>
            <p>Bitte logge dich ein bevor du einem Spiel beitrittst.</p>
            <router-link :to="`/`">Zum Login</router-link>
        </div>
    </div>
</template>

<script>
import { defineComponent, ref, onMounted } from "vue"
import * as GameApi from "../helper/GameApi" 
import router from "@/router"
import use_game from "../composable/Game"
import use_user from "../composable/User"

    export default defineComponent ({
        name: "Lobby",

        setup() {
            let game_name = ref("")
            let failure_msg = ref("")
            let success_msg = ref("")
            let is_logged_in = ref(false)
            const { game, set_game_data } = use_game()
            const { user } = use_user()

            onMounted(() => {
                is_logged_in.value = user.value[`is_logged_in`]
            })

            async function launch_game() {
                if (game_name.value !== "") {
                    const answer = await GameApi.launch_game(game_name.value)
                    if (answer["socket_name"]) {
                        set_game_data(answer["game_id"], answer["socket_name"])
                        game.value["game_socket"].onmessage = handleMsg
                        success_msg.value = "Das hat geklappt. Wir warten noch auf deinen Mitspieler."
                        if (answer["game_ready"]) {
                            router.push(`/game`)
                        }
                    } else {
                        failure_msg.value = "Das hat nicht geklappt. Versuch es noch mal."
                    }
                }
            }
            
            function handleMsg(e) {
                const data = JSON.parse(e.data)

                if (data.type == 'launch_game') {
                    router.push(`/game`)
                }
            }

            return {
                game_name,
                launch_game,
                success_msg,
                failure_msg,
                is_logged_in
            }
        }
    })
</script>