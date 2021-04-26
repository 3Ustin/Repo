function open_inventory() {
    inv_menu = document.getElementById("inventory_menu");
    inv_menu.style.removeProperty("display");
    inv_menu.style.display = "block";
}

function close_inventory() {
    inv_menu = document.getElementById("inventory_menu");
    inv_menu.style.removeProperty("display");
    inv_menu.style.display = "none";
}

function open_shop() {
    tav_shop = document.getElementById("tavern_shop");
    tav_feed = document.getElementById("tavern_activity_feed");
    tav_parent = document.getElementById("tavern_lower_box")

    tav_feed.style.removeProperty("display");
    tav_feed.style.display = "none";

    tav_shop.style.removeProperty("display");
    tav_shop.style.display = "flex";
}

function close_shop() {
    tav_shop = document.getElementById("tavern_shop");
    tav_feed = document.getElementById("tavern_activity_feed");
    tav_parent = document.getElementById("tavern_lower_box")

    tav_shop.style.removeProperty("display");
    tav_shop.style.display = "none";

    tav_feed.style.removeProperty("display");
    tav_feed.style.display = "flex";

}