/* =====================================
   USER REGISTRATION
===================================== */

function registerUser(event) {

    event.preventDefault();

    const name =
        document.getElementById("name").value;

    const userId =
        document.getElementById("userId").value;

    const dob =
        document.getElementById("dob").value;

    const phone =
        document.getElementById("phone").value;

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    const confirmPassword =
        document.getElementById("confirmPassword").value;


    /* PASSWORD CHECK */

    if (password !== confirmPassword) {

        alert("Passwords do not match!");

        return;

    }


    /* CHECK IF USER ALREADY EXISTS */

    const existingUser =
        localStorage.getItem(userId);


    if (existingUser) {

        alert(
            "This User ID is already registered!"
        );

        return;

    }


    /* USER DATA */

    const userData = {

        name: name,

        userId: userId,

        dob: dob,

        phone: phone,

        email: email,

        password: password,

        role: "user"

    };


    /* SAVE DATA */

    localStorage.setItem(

        userId,

        JSON.stringify(userData)

    );


    /* SAVE CURRENT USER */

    localStorage.setItem(

        "currentUser",

        JSON.stringify(userData)

    );


    alert(
        "Registration successful!"
    );


    /* OPEN DASHBOARD */

    window.location.href =
        "/Nit-Hackathon/frontend/user-dashboard.html";

}



/* =====================================
   USER LOGIN
===================================== */

function loginUser(event) {

    event.preventDefault();


    const userId =
        document.getElementById("loginUserId").value;


    const password =
        document.getElementById("loginPassword").value;


    const user =
        localStorage.getItem(userId);


    if (!user) {

        alert(
            "User not found. Please register first."
        );

        return;

    }


    const userData =
        JSON.parse(user);


    if (
        userData.password !== password
    ) {

        alert(
            "Incorrect password!"
        );

        return;

    }


    /* SAVE CURRENT LOGIN */

    localStorage.setItem(

        "currentUser",

        JSON.stringify(userData)

    );


    alert(
        "Login successful!"
    );


    window.location.href =
        "/Nit-Hackathon/frontend/user-dashboard.html";

}



/* =====================================
   LOAD USER DASHBOARD
===================================== */

function loadUserDashboard() {

    const currentUser =
        localStorage.getItem(
            "currentUser"
        );


    /* IF USER NOT LOGGED IN */

    if (!currentUser) {

        window.location.href =
            "/Nit-Hackathon/frontend/user-login.html";

        return;

    }


    const userData =
        JSON.parse(currentUser);


    /* SHOW USER NAME */

    const welcomeText =
        document.getElementById(
            "welcomeName"
        );


    if (welcomeText) {

        welcomeText.innerHTML =
            "Welcome, " +
            userData.name;

    }


    /* PROFILE NAME */

    const profileName =
        document.getElementById(
            "profileName"
        );


    if (profileName) {

        profileName.innerHTML =
            userData.name;

    }


    /* PROFILE USER ID */

    const profileUserId =
        document.getElementById(
            "profileUserId"
        );


    if (profileUserId) {

        profileUserId.innerHTML =
            userData.userId;

    }

}



/* =====================================
   SIDEBAR MENU
===================================== */

function toggleMenu() {

    const sidebar =
        document.getElementById(
            "sidebar"
        );


    sidebar.classList.toggle(
        "active"
    );

}



/* =====================================
   SHOW DASHBOARD SECTIONS
===================================== */

function showSection(sectionName) {

    const sections =
        document.querySelectorAll(
            ".dashboard-section"
        );


    sections.forEach(function(section) {

        section.style.display =
            "none";

    });


    const selectedSection =
        document.getElementById(
            sectionName
        );


    if (selectedSection) {

        selectedSection.style.display =
            "block";

    }


    /* CLOSE MENU */

    const sidebar =
        document.getElementById(
            "sidebar"
        );


    sidebar.classList.remove(
        "active"
    );

}



/* =====================================
   LOGOUT
===================================== */

function logout() {

    localStorage.removeItem(
        "currentUser"
    );


    alert(
        "You have successfully logged out."
    );


    window.location.href =
        "/Nit-Hackathon/frontend/javascript.js";

}



/* =====================================
   PROFILE ICON
===================================== */

function toggleProfile() {

    const profileBox =
        document.getElementById(
            "profileDropdown"
        );


    profileBox.classList.toggle(
        "show"
    );

}