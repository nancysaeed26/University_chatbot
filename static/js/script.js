document.addEventListener("DOMContentLoaded", function () {


    // استرجاع آخر وضع
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme) {
        document.body.classList.add(savedTheme);
    }

    // الوضع النهاري
    document.getElementById("lightMode").onclick = function () {

        document.body.classList.remove("dark");
        document.body.classList.remove("contrast");

        localStorage.removeItem("theme");

    };

    // الوضع الليلي
    document.getElementById("darkMode").onclick = function () {

        document.body.classList.remove("contrast");
        document.body.classList.add("dark");

        localStorage.setItem("theme", "dark");

    };

    // وضع التباين
    document.getElementById("contrast").onclick = function () {

        document.body.classList.remove("dark");
        document.body.classList.add("contrast");

        localStorage.setItem("theme", "contrast");

    };

});
const chatForm = document.getElementById("chatForm");

if (chatForm) {

    chatForm.addEventListener("submit", function (e) {

        e.preventDefault();

        const questionInput = document.getElementById("question");
        const messages = document.getElementById("messages");

        const question = questionInput.value.trim();

        if (question === "") return;

        messages.innerHTML += `
            <div class="user-message">
                👤 ${question}
            </div>
        `;

        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Requested-With": "XMLHttpRequest"
            },
            body: "question=" + encodeURIComponent(question)
        })

        .then(response => response.json())

        .then(data => {

    // إنشاء رسالة البوت
    const botMessage = document.createElement("div");
    botMessage.className = "bot-message";

    botMessage.innerHTML = "🤖 جاري التفكير...";

    messages.appendChild(botMessage);

    messages.scrollTop = messages.scrollHeight;

    setTimeout(() => {

        botMessage.innerHTML = "🤖 ";

         let i = 0;

function typeWriter() {

    if (i < data.answer.length) {

        // إذا وصل إلى <br>
        if (data.answer.substring(i, i + 4) === "<br>") {

            botMessage.innerHTML += "<br>";
            i += 4;

        } else {

            botMessage.innerHTML += data.answer.charAt(i);
            i++;

        }

        messages.scrollTop = messages.scrollHeight;

        setTimeout(typeWriter, 20);

    }

}

typeWriter();


        

    }, 700);

    questionInput.value = "";

    questionInput.focus();

});

    });

}
