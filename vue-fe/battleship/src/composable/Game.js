import { ref, computed } from "vue"

const game_data = ref({
    game_id: "",
    game_socket: null
})

export default function use_game() {
    const socket_prefix = 'ws://localhost:8080/ws'
    const game = computed(() => game_data.value)
    function set_game_data(id, socket_name) {
        game_data.value["game_id"] = id
        game_data.value["game_socket"] = new WebSocket(socket_prefix + socket_name)
    }

    return {
        game, set_game_data
    }
}