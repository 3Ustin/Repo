function animate_basic() {
    //animate enemy//
        var enemy_img = document.getElementById("enemy_img");
        enemy_img.src = "{{ url_for('static', filename='img/Zombie_hit.png') }}";
        setTimeout(() => { enemy_img.src = "{{ url_for('static', filename='img/Zombie_1.png') }}"; }, 200);
        
    //animate player//
        var paladin_img = document.getElementById("paladin_img");
        paladin_img.src = "{{ url_for('static', filename='img/paladin_hit.png') }}";
        setTimeout(() => {paladin_img.src = "{{ url_for('static', filename='img/paladin_combat.png') }}"; }, 200);
}