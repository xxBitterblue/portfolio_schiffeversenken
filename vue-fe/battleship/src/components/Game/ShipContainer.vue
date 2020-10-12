<template>
    <div class="ship_container" id="ship_container">
        <Ship :id="'1'" :size="1" :life="base_life * 1" :dragallowed="true" :alignment="'horizontal'"/>
        <Ship :id="'2'" :size="2" :life="base_life * 2" :dragallowed="true" :alignment="'horizontal'"/>
        <Ship :id="'3'" :size="3" :life="base_life * 3" :dragallowed="true" :alignment="'horizontal'"/>
    </div>
</template>

<script>
import {defineComponent} from "vue"
import Ship from "./Ship"
import * as statics from "../../helper/Statics"

    export default defineComponent ({
        name: "ShipContainer",

        components: {
                Ship
        },

        setup() {
            const base_life = statics.ship_base_life

            return {
                base_life
            }
        }
    })
</script>

<style>
    div .ship_container {
        width: 300px;
        border:1px solid black;
        position: relative;
    }
</style>