window.onload=main; 

function main(){
    let samePass1 = document.getElementById('password')
    let samePass2 = document.getElementById('password_conf')
    console.log('js works')
    samePass2.onchange = function(){
        console.log('entered func')
        if (samePass1.value != samePass2.value){
            samePass2.setCustomValidity('Passwords do not match.')
            console.log('wrong comparison')
        } else {
            this.setCustomValidity('')
            console.log('correct comparison')
        }
    
    }
}