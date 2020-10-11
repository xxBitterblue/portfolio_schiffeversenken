<template>
    <div>
        <label>Username:</label>
        <input type="text" required v-model="username"/>
        <label>Passwort:</label>
        <input type="password" required v-model="password"/>
        <button v-on:click="login">Login</button> 
        <button v-on:click="register">Registrieren</button> 
        <p v-if="failure_msg">{{ failure_msg }}</p>
        <p v-if="success_msg">{{ success_msg }}</p>
    </div>
</template>

<script>
import { defineComponent, ref } from "vue"
import * as AuthenticationApi from "../helper/AuthenticationApi"
import use_user from "../composable/User"
import router from "@/router"

    export default defineComponent ({
        name: "Home",

        setup() {
            const { setUserData } = use_user()
            let username = ref("")
            let password = ref("")
            let failure_msg = ref("")
            let success_msg = ref("")

            async function login() {
                if (username.value != "" && password.value) {
                    const answer = await AuthenticationApi.login(username.value, password.value)
            
                    if (answer["token"]) {
                        setUserData(answer["user_id"], username.value, answer["token"])
                        router.push(`/lobby`)
                    } else {
                        failure_msg.value = answer
                    }
                }
            }

            async function register() {
                if (username.value != "" && password.value) {
                    const answer = await AuthenticationApi.register(username.value, password.value)
                    if (answer == true) {
                        success_msg.value = "Erfolgreich registriert"
                    } else {
                        failure_msg.value = answer
                    }
                }
            }

            return {
                username,
                password,
                login,
                register,
                failure_msg,
                success_msg
            }
        }
    })
</script>