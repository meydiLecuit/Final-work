
window.onload = async () => {
    let data = sessionStorage.getItem('userSession');
    let id = JSON.parse(data).ID;
    let user = await getUser(id);
    
    if(user["admin"] != 1 || user["admin"] == null){
        window.location.href='home.html';
    }

}