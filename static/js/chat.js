// =====================================================
// Current Chat
// =====================================================

let currentChatId = null;


// =====================================================
// Elements
// =====================================================

const messages = document.getElementById("messages");

const input = document.getElementById("user-input");

const sendBtn = document.getElementById("send-btn");

const typingIndicator = document.getElementById("typing-indicator");

const pdfList = document.getElementById("pdf-list");

const totalPdfs = document.getElementById("total-pdfs");


// =====================================================
// Load PDFs
// =====================================================

async function loadPDFs() {

    try {

        const response = await fetch("/files/pdfs");

        const pdfs = await response.json();

        totalPdfs.textContent = pdfs.length;

        pdfList.innerHTML = "";


        if (pdfs.length === 0) {

            pdfList.innerHTML = `
                <div class="loading-text">
                    No PDFs uploaded.
                </div>
            `;

            return;

        }


        pdfs.forEach(pdf => {

            pdfList.innerHTML += `

                <div class="pdf-item">

                    <div class="pdf-icon">
                        📄
                    </div>


                    <div class="pdf-info">

                        <div class="pdf-name">
                            ${pdf.name}
                        </div>


                        <div class="pdf-size">

                            ${(pdf.size / 1024 / 1024).toFixed(2)} MB

                        </div>

                    </div>

                </div>

            `;

        });

    }

    catch (error) {

        pdfList.innerHTML = `

            <div class="loading-text">
                Failed to load PDFs.
            </div>

        `;

        console.error(error);

    }

}


// =====================================================
// Scroll
// =====================================================

function scrollBottom() {

    messages.scrollTop = messages.scrollHeight;

}


// =====================================================
// User Bubble
// =====================================================

function addUserMessage(text) {

    const div = document.createElement("div");

    div.className = "message user";


    div.innerHTML = `

        <div class="message-content">

            ${text}

        </div>

    `;


    messages.appendChild(div);

    scrollBottom();

}


// =====================================================
// AI Bubble
// =====================================================

function addAIMessage(answer, sources = []) {

    let sourceHTML = "";


    if (sources.length) {

        sourceHTML = `

            <div class="sources">

                <h6>Sources</h6>


                ${sources.map(source => `

                    <div class="source-item">

                        <span>
                            📄 ${source.name || source}
                        </span>


                        <a
                            href="/download-source?path=${encodeURIComponent(source.path || source)}"
                            target="_blank"
                            class="download-btn"
                        >
                            ⬇ Download
                        </a>

                    </div>

                `).join("")}


            </div>

        `;

    }


    const div = document.createElement("div");

    div.className = "message ai";


    div.innerHTML = `

        <div class="message-content">

            ${answer.replace(/\n/g, "<br>")}

            ${sourceHTML}

        </div>

    `;


    messages.appendChild(div);

    scrollBottom();

}


// =====================================================
// Send Message
// =====================================================

async function sendMessage() {

    const question = input.value.trim();


    if (!question) return;


    const welcome = document.querySelector(".welcome-screen");


    if (welcome) {

        welcome.remove();

    }


    addUserMessage(question);


    input.value = "";

    input.style.height = "60px";


    typingIndicator.style.display = "flex";


    scrollBottom();


    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },


            body: JSON.stringify({

                question: question,

                chat_id: currentChatId

            })

        });


        const data = await response.json();


        if (data.chat_id) {

            currentChatId = data.chat_id;

            await loadHistory();

        }


        typingIndicator.style.display = "none";


        addAIMessage(

            data.answer || "No answer returned.",

            data.sources || []

        );

    }


    catch (error) {

        typingIndicator.style.display = "none";


        addAIMessage(

            "❌ Sorry, something went wrong while contacting the server."

        );


        console.error(error);

    }

}
// =====================================================
// Enter to Send
// =====================================================

input.addEventListener("keydown", function (event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();

    }

});


// =====================================================
// Auto Grow Textarea
// =====================================================

input.addEventListener("input", function () {

    this.style.height = "60px";

    this.style.height = this.scrollHeight + "px";

});


// =====================================================
// Load Chat History
// =====================================================

async function loadHistory() {

    try {

        const response = await fetch("/history/");

        const chats = await response.json();


        const list = document.querySelector(".chat-list");


        if (!list) return;


        list.innerHTML = "";


        chats.forEach(chat => {

            const item = document.createElement("div");

            item.className = "chat-item";


            if (chat.id === currentChatId) {

                item.classList.add("active");

            }


            item.innerHTML = `

                <i class="bi bi-chat-left-text"></i>

                <span>${chat.title}</span>

            `;


            item.onclick = () => {

                loadConversation(chat.id);

            };


            list.appendChild(item);

        });

    }


    catch (error) {

        console.error(error);

    }

}


// =====================================================
// Load One Conversation
// =====================================================

async function loadConversation(chatId) {

    try {

        const response = await fetch("/history/" + chatId);


        const chat = await response.json();


        currentChatId = chat.id;


        messages.innerHTML = "";


        chat.messages.forEach(msg => {

            if (msg.role === "user") {

                addUserMessage(msg.content);

            }


            else {

                addAIMessage(

                    msg.content,

                    msg.sources || []

                );

            }

        });


        // Refresh sidebar to highlight active chat

        loadHistory();

    }


    catch (error) {

        console.error(error);

    }

}
// =====================================================
// Initialize
// =====================================================

window.onload = function () {

    loadPDFs();

    loadHistory();

    input.focus();

};


// =====================================================
// Optional: New Chat Button
// =====================================================

const newChatBtn = document.querySelector(".new-chat-btn");


if (newChatBtn) {

    newChatBtn.addEventListener("click", () => {


        currentChatId = null;


        loadHistory();


        messages.innerHTML = `

            <div class="welcome-screen">


                <div class="welcome-icon">

                    🧠

                </div>


                <h1>

                    Welcome to ResearchMind AI

                </h1>


                <p>

                    Upload research papers, ask questions,
                    compare documents and discover insights.

                </p>


                <div class="welcome-cards">


                    <div class="welcome-card">


                        <i class="bi bi-upload"></i>


                        <h4>
                            Upload PDFs
                        </h4>


                        <p>
                            Upload one or more research papers.
                        </p>


                    </div>



                    <div class="welcome-card">


                        <i class="bi bi-search"></i>


                        <h4>
                            Semantic Search
                        </h4>


                        <p>
                            Search across every uploaded document.
                        </p>


                    </div>



                    <div class="welcome-card">


                        <i class="bi bi-stars"></i>


                        <h4>
                            AI Answers
                        </h4>


                        <p>
                            Receive answers with cited sources.
                        </p>


                    </div>


                </div>


            </div>

        `;


        input.value = "";


        input.focus();


    });

}