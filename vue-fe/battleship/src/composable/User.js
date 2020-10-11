import { ref, computed } from "vue"

const user_data = ref({
    user_id: "",
    username: "",
    user_token: "",
    is_logged_in: false
})

export default function use_user() {
    const user = computed(() => user_data.value)
    function setUserData(id, username, token) {
        user_data.value["user_id"] = id
        user_data.value["username"] = username
        user_data.value["user_token"] = token
        user_data.value["is_logged_in"] = true
    }

    return {
        setUserData, user
    }
}
