<template>
    <div>
        <div v-if="is_setting && (x && y)" class="btn-group"
                    :style="{top: y-20 + 'px', left: x + 'px'}">
                        <button v-on:click="flip_ship">Flip</button> 
                        <button v-on:click="delete_ship">Delete</button>
                        <button v-on:click="close_ship_options">Close</button>
        </div>
            <div class="ship_in_game"
                v-if="x && y"
                v-on:click="open_ship_options"
                :draggable='dragallowed'
                @dragstart="dragStart"
                @dragover.stop
                :style="{top: y + 'px', left: x + 'px', width: width + 'px', height: height + 'px', backgroundImage: 'url('+image_path+')', transform: 'rotate(' + image_orientation + 'deg)'}"
            >
                <p>{{life}}  {{size}}</p>
            </div>
            <div 
                v-else
                :draggable='dragallowed'
                @dragstart="dragStart"
                @dragover.stop
                class="ship_in_container"
                :style="{width: width + 'px', height: height + 'px', backgroundImage: 'url('+image_path+')', transform: 'rotate(' + image_orientation + 'deg)'}"
            >
                <p>{{ size }}</p>
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
            let width = computed(() => props.alignment == statics.horizontal_alignment ? statics.base_size * props.size : statics.base_size)
            let height = computed(() => props.alignment == statics.vertical_alignment ? statics.base_size * props.size : statics.base_size)
            let image_path = computed(() => require('@/assets/Ship_1_Alive.png'))
            let image_orientation = computed(() => props.alignment == statics.vertical_alignment ? 90 :  0)
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
                image_path,
                image_orientation
            }
        }
    })
</script>

<style>
    div .ship_in_game {
        position: absolute;
        text-align: center;

    }

    div .ship_in_container {
        position: relative;
        text-align: center;

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
