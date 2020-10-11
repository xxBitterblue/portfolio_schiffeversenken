import * as statics from "./Statics"

export function calculate_collision(ship_list, id,  x, y, size, alignment) {
    let has_collision = false
    let ship_width = alignment == "horizontal" ? statics.base_size * size : statics.base_size 
    let ship_height = alignment == "vertikal" ? statics.base_size * size : statics.base_size

    ship_list.value.forEach(ele => {
        if (id != ele.id) {
            let current_ship_width = ele.alignment == "horizontal" ? statics.base_size * ele.size : statics.base_size 
            let current_ship_height = ele.alignment == "vertikal" ? statics.base_size * ele.size : statics.base_size

            if ((x < ele.x + current_ship_width) && (x + ship_width > ele.x) &&
                (y < ele.y + current_ship_height) && (y + ship_height > ele.y)) {
                has_collision = true
            }
        }
    })

    if (x + ship_width > statics.board_size || y + ship_height > statics.board_size) {
        has_collision = true
    }

    return has_collision
}