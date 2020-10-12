<template>
    <div class="score_container">
        <p>Deine Lebenspunkte: {{ player_life_points }}</p>
        <p>Gegnerische Lebenspunkte: {{ enemy_life_points}}</p>
    </div>
</template>

<script>
import { defineComponent, ref } from "vue"
import use_user from "../../composable/User"

    export default defineComponent ({
        name: "Score",

        setup() {
            const { user } = use_user()
            let enemy_id = ref("")
            let player_life_points = ref(0)
            let enemy_life_points = ref(0)

            function handle_score_changes(e) {
                const data = JSON.parse(e.data)
                const message = data.message

                if (data.type == 'score_changed') {
                    if (message['affected_player_id'] == user.value["user_id"]) {
                        player_life_points.value = message['new_life_points']
                    } else {
                        enemy_life_points.value = message['new_life_points']
                    }
                } else if (data.type == 'start_game') {
                    const enemy_data = message['all_player'].find(player => player.id != user.value["user_id"])

                    enemy_id.value = enemy_data.id
                    enemy_life_points.value = enemy_data.life_points
                    player_life_points.value = message['all_player'].find(player => player.id == user.value["user_id"]).life_points
                }
            }

            return {
                handle_score_changes,
                player_life_points,
                enemy_life_points
            }
        }
    })
</script>

<style>
    div .score_container {
        width: 250px;
        height: 100px;
        border:1px solid black;
        position: relative;
        margin-left: 20px;
        padding-left: 10px;
    }
</style>