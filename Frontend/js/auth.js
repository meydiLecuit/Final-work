async function login() {
    let url = 'http://localhost/login';

    let formData = new FormData();

    formData.append('username', document.getElementById("username").value)
    formData.append('password', document.getElementById("password").value)
    try {
        let res = await fetch(url, {
            method: 'POST',
            body: formData
    
    });

       
        console.log('data sent login');
        return await res.json();


        
    } catch (error) {
        console.log(error);
        console.log("Data not send login");

    }
}

async function loadSession()
{
    let data = await login();

    let session = JSON.stringify(data);


    sessionStorage['userSession'] = session;
    if(data != null){
    window.location.replace("http://localhost:3000/home.html");
    }
    else{
        alert("Login credentials are not correct!");
    }

}

async function isAthenticated()
{   
    if(window.location != "http://localhost:3000/")
    {
        let sessiondata = null ;
        let isLogedIn = null;
        let data = sessionStorage.getItem('userSession');
        let id = null;
        let user = null;

        let jsonData = null;

        if(data != null){
            jsonData = JSON.parse(data)["ID"];
        }

        if(jsonData != null)
        {
            let jsonData = JSON.parse(data);
            if(jsonData["username"] !== 'undefined'){
                sessiondata = JSON.parse(data);
                isLogedIn =sessiondata.isLogedIn;
                id = JSON.parse(data).ID;
                user = await getUser(id);
            }
        } 
            
        if(sessiondata === null || isLogedIn === false || user === null)
        {
            
             window.location.replace("http://localhost:3000");
             alert('Authentication Failed!');
        }
    }
 

    
}


window.onload = async () => {

    isAthenticated();
    
}