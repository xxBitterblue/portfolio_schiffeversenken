<template>
    <div>
        <div v-if="is_logged_in">
            <p v-if="player_won">Herzlichen Glückwunsch! Du hast gewonnen.</p>
            <p v-else>Leider hast du verloren. Viel Glück bei der nächsten Runde.</p>
            <router-link :to="`/lobby`">Noch einmal spielen!</router-link>
        </div>
        <div v-else>
            <p>Bitte logge dich ein bevor du einem Spiel beitrittst.</p>
            <router-link :to="`/`">Zum Login</router-link>
        </div>
    </div>   
</template>

<script>
import {defineComponent, onMounted, ref} from "vue"
import use_user from "../../composable/User"

    export default defineComponent ({
        name: 'EndScreen',

        props: {
            winnerId: {type: String, required: true}
        },

        setup(props) {
            const { user } = use_user()
            let player_won = ref("")
            let is_logged_in = ref(false)

            onMounted(() => {
                is_logged_in.value = user.value[`is_logged_in`]
                player_won.value = user.value["user_id"] == props.winnerId
            })

            return {
                player_won,
                is_logged_in
            }
        }
    })
</script>

