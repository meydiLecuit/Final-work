'use strict';
//import bcrypt from 'bcrypt';

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


async function getProducts() {
    let url = 'http://localhost/products';
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        console.log(error);
        console.log("Products not found");

    }
}

async function getUsers() {
    let url = 'http://localhost/getUsers';
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        console.log(error);
        console.log("Products not found");

    }
}

async function getProduct(id) {
    let url = 'http://localhost//product/' + id;
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        console.log(error);
        console.log("Product of edit not found");

    }
}

async function getUser(id) {
    let url = 'http://localhost//getUser/' + id;
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        console.log(error);
        console.log("Product of edit not found");

    }
}

async function deleteProduct(id){
    
    let url = 'http://localhost/deleteProduct/' + id;
    try {
        let res = await fetch(url, {method: 'DELETE'});
        window.location.reload();
        return await res.json();
        
    } catch (error) {
        console.log(error);
        console.log("Product is not deleted");

    }
    
}

async function editSave(id) {
    let url = 'http://localhost/editProduct/' + id;

    let formData = new FormData();

    formData.append('name', document.getElementById("name").value)
    formData.append('prijs', document.getElementById("prijs").value)
    formData.append('merk', document.getElementById("merk").value)
    
    try {
        let res = await fetch(url, {
            method: 'PATCH',
            body: formData
    
    });
        console.log("data sent edit");
        return await res.json();
    } catch (error) {
        console.log(error);
        console.log("Products not edited");

    }
}
async function loadEditPage(id){
    let product = await getProduct(id);

    if(document.getElementById('name').value != null){
    document.getElementById('name').value = product.name;
    }
    if(document.getElementById('prijs').value != null){
    document.getElementById('prijs').value = product.prijs;
    }
    if(document.getElementById('merk').value != null){
    document.getElementById('merk').value = product.merk;
    }

}

async function createProductSave(){
    let url = 'http://localhost/products';

    let formData = new FormData();
    let products = await getProducts();

    let name = document.getElementById('naam').value;
    let prijs = document.getElementById('prijs').value;
    let merk = document.getElementById('merk').value;

    let checkDb = false;

    products.forEach(product => {
        if(product.name === name && product.prijs === prijs && product.merk === merk){
            checkDb = true;
        }
    })

    if(naam === '' || prijs === '' || merk === '' ){
        document.getElementById('alert').innerHTML = `<div class="bg-red-200 relative text-red-500 py-3 px-3 rounded-lg">
        Gelieve heel het formulier in te vullen
    </div>` ;
    }
    if(checkDb == true){
        document.getElementById('alert').innerHTML = `<div class="bg-red-200 relative text-red-500 py-3 px-3 rounded-lg">
        Product ${name} ${merk} bestaat al
    </div>` ;
    }
    else{
        formData.append('name', name);
        formData.append('prijs', prijs);
        formData.append('merk', merk);

        try {
            let res = await fetch(url, {
                method: 'POST',
                body: formData
    
            });
        console.log("data send register");
        document.getElementById('alert').innerHTML = `<div class="bg-green-200 relative text-green-500 py-3 px-3 rounded-lg">
        Het Product is succesvol opgeslagen!
    </div>`
        return await res.json();
    } catch (error) {
        console.log(error);
        console.log("User is not created");

    }

    }


}


async function savePicture(){
    let url = 'http://localhost/savePicture';

    let formData = new FormData();
   
    
    let files = document.getElementById('files[]');
    let name = document.getElementById('naam').value;
  
        formData.append('name', name)
   for(const file of files.files){
         formData.append('files[]', file);
   }

        console.log(formData)
        

     

        try {
            let res = await fetch(url, {
                method: 'POST',
                body: formData
    
            });
            console.log(res.body);
        console.log("picture send register");
        document.getElementById('alert').innerHTML = `<div class="bg-green-200 relative text-green-500 py-3 px-3 rounded-lg">
        Het Product is succesvol opgeslagen!
    </div>`
        return await res.json();
    } catch (error) {
        console.log(error);
        console.log("User is not created");

    }

    


}
async function registerSave() {
    let url = 'http://localhost/createUser';

    let users = await getUsers();
    
    let formData = new FormData();

    let name = document.getElementById('firstname').value;
    let lastName = document.getElementById('lastname').value;
    let email = document.getElementById('email').value;
    let username = name + lastName;
    let password1 = document.getElementById('password1').value;
    let password2 = document.getElementById('password2').value;
    let admin = 0

    const salt = await bcrypt.genSalt(10);
    if(document.getElementById("admin").checked){
        admin = document.getElementById("admin").value;
    }
    let checkDb = false;


    users.forEach(user => {
        if(user.name === name && user.lastName === lastName){
            checkDb = true;
        }
    });

    if(name === '' || lastName === '' || email === '' ){
        document.getElementById('alert').innerHTML = `<div class="bg-red-200 relative text-red-500 py-3 px-3 rounded-lg">
        Gelieve heel het formulier in te vullen
    </div>` ;
    }
    else if(password1.length < 6){
        document.getElementById('alert').innerHTML = `<div class="bg-red-200 relative text-red-500 py-3 px-3 rounded-lg">
        wachtwoord moet meer dan 6 karakters bevatten
    </div>` ;
    }
    else if(checkDb === true){
        document.getElementById('alert').innerHTML = `<div class="bg-red-200 relative text-red-500 py-3 px-3 rounded-lg">
        User ${name} ${lastName} bestaat al
    </div>` ;
    }
    else{

        if(password1 === password2){
            formData.append('name', name);
            formData.append('lastName', lastName);
            formData.append('username', username);
            formData.append('email', email);
            formData.append('password', await bcrypt.hash(password2, salt));
            formData.append('admin', admin);

            
            try {
                let res = await fetch(url, {
                    method: 'POST',
                    body: formData
        
                });
            console.log("data send register");
            document.getElementById('alert').innerHTML = `<div class="bg-green-200 relative text-green-500 py-3 px-3 rounded-lg">
            User succesvol opgeslagen!
        </div>`
            return await res.json();
        } catch (error) {
            console.log(error);
            console.log("User is not created");
    
        }

    }
    else{
        alert("Password Confirmation is not the same as the first password!");

    }
    }


}

async function renderProducts() {
    let products = await getProducts();
    let html = '';
    products.forEach(product => {
        let htmlSegment = `    
                                <li>Naam: ${product.name} </li>
                                <li>€ ${product.prijs}</li>
                                <li> ${product.merk}</li>
                                <br>
                                <button id="${product._id}" value="${product._id}" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 border border-blue-700 rounded">
                                Edit
                            </button>
                              <button id="delete${product._id}" value="${product._id}" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 border border-red-700 rounded">
                                Delete
                              </button>
                              <hr class="border-solid border-4 border-gray-900 ">
                            
                        `;                    
        
                        html += htmlSegment;
                       

    });

  

    let container = document.getElementById('list');
    if(container != null){
        container.innerHTML = html;
    }


    products.forEach(product => {
        let button = document.getElementById(`${product._id}`);
        
        if(button != null){
        button.addEventListener("click", function(){
            localStorage.setItem('editId', button.value);
            window.location.href='editProduct.html';
        });
        }
        document.getElementById(`delete${product._id}`).addEventListener('click', function(){

            deleteProduct(product._id);
        });
        
    });
}


let hpCharacters = [];
if(document.getElementById('list') != null){

    document.getElementById('searchInput').addEventListener('keyup', (e) => {
        const searchString = e.target.value.toLowerCase();
        const filteredCharacters = hpCharacters.filter((product) => {
        
            return (
                product.name.toLowerCase().includes(searchString) ||
                product.merk.toLowerCase().includes(searchString)
                );
    
            });
    
            displayCharacters(filteredCharacters);
});
}
const loadCharacters = async () => {
    try {
        const res = await fetch('http://localhost/products');
        hpCharacters = await res.json();
        displayCharacters(hpCharacters);
    } catch (err) {
        console.error(err);
    }
};

const displayCharacters = (products) => {
    const htmlString = products
        .map((product) => {
            return `    
            <li>Naam: ${product.name} </li>
            <li>€ ${product.prijs}</li>
            <li> ${product.merk}</li>
            <br>
            <button id="${product._id}" value="${product._id}" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 border border-blue-700 rounded" onclick="window.location.href='editProduct.html';">
            Edit
        </button>
          <button id="delete${product._id}" value="${product._id}" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 border border-red-700 rounded">
            Delete
          </button>
          <hr class="border-solid border-4 border-gray-900 ">
          `;
        })
        .join('');
        document.getElementById('list').innerHTML = htmlString;

        products.forEach(product => {
            let button = document.getElementById(`${product._id}`);
            
            if(button != null){
            button.addEventListener("click", function(){
                localStorage.setItem('editId', button.value);
                window.location.href='editProduct.html';
            });
            }
            document.getElementById(`delete${product._id}`).addEventListener('click', function(){
    
                deleteProduct(product._id);
            });
            
        });
    
    
};

window.onload = async () => {
   if(document.getElementById('menu') != null){
    let data = sessionStorage.getItem('userSession');
    let id = JSON.parse(data).ID;
    let user = await getUser(id);
    if(user["admin"] == 1){
        document.getElementById('menu').innerHTML = `
        <a href="home.html" class="p-4">Home</a>
        <a href="productenLijst.html" class="p-4">Producten</a>
        <a id="logout" class="p-4">Log out</a>
        <a href="admin.html" class="p-4">Admin</a>`;
    }
    }
    isAthenticated();
    
    if(document.getElementById('list') != null){
    renderProducts();
    loadCharacters();
    }
    if(document.getElementById('prijs') != null){
    loadEditPage(localStorage.getItem('editId'));
    }
 
    if(document.querySelector('.js-password-toggle') != null){
        document.getElementById('toggle1').addEventListener('change', function() {
 
            if (document.getElementById('password1').type === 'password') {
                document.getElementById('password1').type = 'text'
            } 
            else {
                document.getElementById('password1').type = 'password'
            }
            document.getElementById('password1').focus();
        })

        document.getElementById('toggle2').addEventListener('change', function() {
 
            if (document.getElementById('password2').type === 'password') {
                document.getElementById('password2').type = 'text'
            } 
            else {
                document.getElementById('password2').type = 'password'
            }
            document.getElementById('password2').focus();
        })
    }


if(document.getElementById('loginButton') != null){
    document.getElementById('loginButton').addEventListener("click", async function (e) {
        e.preventDefault();

        login();
        loadSession();
        
    
    });

}if(document.getElementById('createButton') != null){
    document.getElementById('createButton').addEventListener("click", async function (e) {
        e.preventDefault();

        createProductSave();
        savePicture();
        
    
    });

}

if(document.getElementById('welcome') != null){

    let id = JSON.parse(sessionStorage.getItem('userSession'))["ID"];
    let user = await getUser(id);
    let html = `<h1 class="text-4x1 font-bold text-center text-purple-700"> Welkom ${user.name} ${user.lastName} </h1>`;

    document.getElementById('welcome').innerHTML = html;

}

if(document.getElementById('registerButton') != null){
    document.getElementById('registerButton').addEventListener("click", async function (e) {
        e.preventDefault();

        registerSave();
    
    });

}

if(document.getElementById('editButton') != null){
    document.getElementById('editButton').addEventListener("click",  async function (e) {
        e.preventDefault();

        editSave(localStorage.getItem('editId'))
    
    })
}

if(document.getElementById('logout') != null){
    document.getElementById('logout').addEventListener("click",  async function (e) {
        
        sessionStorage.clear();
        window.location.replace("http://localhost:3000"); 

    })
}
};
