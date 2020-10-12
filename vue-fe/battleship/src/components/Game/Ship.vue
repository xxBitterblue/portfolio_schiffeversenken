<template>
    <div>
        <div v-if="is_setting && (x && y)" class="btn-group"
                    :style="{top: y - height + 'px', left: x + 'px'}">
                        <button v-on:click="flip_ship">Flip</button> 
                        <button v-on:click="delete_ship">Delete</button>
                        <button v-on:click="close_ship_options">Close</button>
        </div>
            <div v-if="x && y" class="ships_in_game">
                <div class="ship_in_game"               
                v-on:click="open_ship_options"
                :draggable='dragallowed'
                @dragstart="dragStart"
                @dragover.stop
                :style="{top: y + 'px', left: x + 'px', width: width + 'px', height: height + 'px', backgroundImage: 'url('+image_path+')'}"
                />
                <p :style="{top: y + (height) + 'px', left: x + 'px'}">LP: {{life}}</p>
            </div>
            <div v-else class="ships_in_container">
                <div  
                    :draggable='dragallowed'
                    @dragstart="dragStart"
                    @dragover.stop
                    class="ship_in_container"
                    :style="{width: width + 'px', height: height + 'px', backgroundImage: 'url('+image_path+')'}"
                />
                <div class="ship_information_container">
                    <p>Size: {{ size }}</p>
                    <p>Life: {{ life }}</p>
                </div>
            </div>  
    </div>
</template>

<script>
import { defineComponent, ref, computed } from "vue"
import * as statics from "../../helper/Statics.js"

    export default defineComponent ({
        name: "Ship",

        props: {
            x: {type: Number},
            y: {type: Number},
            life: {type: Number},
            size: {type: Number, required: true},
            id: {type: String},
            dragallowed: {type: Boolean, required: true},
            alignment: {type: String, required: true},
            started: {type: Boolean, required: true}
        },

        setup(props, context) {
            const is_setting = ref(false)
            let width = computed(() => props.alignment == statics.horizontal_alignment ? statics.base_size * props.size : statics.base_size )
            let height = computed(() => props.alignment == statics.vertical_alignment ? statics.base_size * props.size : statics.base_size)
            let image_path = computed(() => require('@/assets/Ship_' + props.size + '_Alive_' + props.alignment + '.png'))

            function dragStart (e) {
                e.dataTransfer.dropEffect = "copy"
                e.dataTransfer.setData('ship_id', props.id)
                e.dataTransfer.setData('ship_size', props.size)               
            }

            function open_ship_options() {
                if (!props.started) {
                    is_setting.value = true
                }
            }

            function flip_ship () {
                if (props.alignment == statics.horizontal_alignment) {
                    context.emit("flip-ship", {"id": props.id, "alignment": statics.vertical_alignment})
                } else {
                    context.emit("flip-ship", {"id": props.id, "alignment": statics.horizontal_alignment})
                }
                close_ship_options()
            }

            function delete_ship() {
                context.emit("delete-ship", props.id)
                close_ship_options()
            }

            function close_ship_options() {
                is_setting.value = false
            }

            return {
                is_setting,
                open_ship_options,
                dragStart,
                flip_ship,
                delete_ship,
                close_ship_options,
                width,
                height,
                image_path
            }
        }
    })
</script>

<style>
    div .ship_in_game {
        position: absolute;
        text-align: center;
    }

    div .ships_in_game p {
        position: absolute;
        font-size: 15px;
    }

    div .ships_in_container {
        display: grid;
        grid-template-columns: 50% 50%;
        padding: 10px;
    }

    div .ship_in_container {
        position: relative;
        text-align: center;
    }
    
    div .ships_in_container p {
        margin: 5px;
    }

    div .btn-group {
        position: absolute;
    }

    .btn-group button {
        border: 0.5px solid;
        color: white;
        padding: 1px 2px;
        cursor: pointer;
        float: left;
        background-color: black;
    }

    .btn-group button:not(:last-child) {
        border-right: none;
    }

    .btn-group:after {
        content: "";
        clear: both;
        display: table;
    }
</style>
