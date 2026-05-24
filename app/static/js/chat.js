/* ===================================================================
   MediBot - Frontend Logic
   Handles the chat UI: sending messages, rendering replies, animations.
   Talks to the Flask backend at /api/chat.
   =================================================================== */

(function () {
  "use strict";

  const API = "/api/chat";
  const chat = document.getElementById("chat");
  const input = document.getElementById("userInput");
  const sendBtn = document.getElementById("sendBtn");

  /* ---------- helpers ------------------------------------------------ */

  // Escape user text so it cannot inject HTML (basic XSS protection).
  function escapeHtml(s) {
    return s.replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function nowTime() {
    const d = new Date();
    return (
      d.getHours().toString().padStart(2, "0") +
      ":" +
      d.getMinutes().toString().padStart(2, "0")
    );
  }

  function scrollDown() {
    chat.scrollTop = chat.scrollHeight;
  }

  /* ---------- message rendering -------------------------------------- */

  function addUserMsg(text) {
    const el = document.createElement("div");
    el.className = "msg user";
    el.innerHTML =
      '<div class="avatar user">&#128100;</div>' +
      "<div>" +
      '<div class="bubble">' + escapeHtml(text) + "</div>" +
      '<div class="time">' + nowTime() + "</div>" +
      "</div>";
    chat.appendChild(el);
    scrollDown();
  }

  function addBotMsg(innerHtml, time) {
    const el = document.createElement("div");
    el.className = "msg bot";
    el.innerHTML =
      '<div class="avatar bot">&#129658;</div>' +
      "<div>" +
      '<div class="bubble">' + innerHtml + "</div>" +
      '<div class="time">' + (time || nowTime()) + "</div>" +
      "</div>";
    chat.appendChild(el);
    scrollDown();
  }

  function showTyping() {
    const el = document.createElement("div");
    el.className = "msg bot";
    el.id = "typing";
    el.innerHTML =
      '<div class="avatar bot">&#129658;</div>' +
      '<div class="bubble">' +
      '<div class="typing"><span></span><span></span><span></span></div>' +
      "</div>";
    chat.appendChild(el);
    scrollDown();
  }

  function removeTyping() {
    const t = document.getElementById("typing");
    if (t) t.remove();
  }

  // Turn a backend reply object into chat content.
  function renderReply(data) {
    if (data.type === "diagnosis") {
      let html = "<p>Based on what you described, here is some guidance:</p>";
      data.conditions.forEach(function (c) {
        html +=
          '<div class="card">' +
          "<h3>" + escapeHtml(c.condition) + "</h3>" +
          '<p class="desc">' + escapeHtml(c.info) + "</p>" +
          "<ul>" +
          c.advice
            .map(function (a) { return "<li>" + escapeHtml(a) + "</li>"; })
            .join("") +
          "</ul>" +
          '<div class="doc-note">&#129658; When to see a doctor: ' +
          escapeHtml(c.see_doctor) +
          "</div>" +
          "</div>";
      });
      addBotMsg(html, data.timestamp);
    } else if (data.type === "emergency") {
      addBotMsg(
        '<div class="emergency-box">&#128680; ' +
          escapeHtml(data.reply) +
          "</div>",
        data.timestamp
      );
    } else {
      addBotMsg(escapeHtml(data.reply), data.timestamp);
    }
  }

  /* ---------- send to backend ---------------------------------------- */

  async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    addUserMsg(text);
    input.value = "";
    showTyping();

    try {
      const res = await fetch(API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();

      // small delay so the typing animation is visible
      setTimeout(function () {
        removeTyping();
        if (data.ok) {
          renderReply(data);
        } else {
          addBotMsg(escapeHtml(data.error || "Something went wrong."));
        }
      }, 650);
    } catch (err) {
      removeTyping();
      addBotMsg(
        "&#9888; I couldn't reach the server. Please make sure the " +
          "backend is running and try again."
      );
    }
  }

  /* ---------- event wiring ------------------------------------------- */

  sendBtn.addEventListener("click", sendMessage);

  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") sendMessage();
  });

  // Quick-chat chips: each carries its message in a data attribute.
  document.querySelectorAll(".chip").forEach(function (chip) {
    chip.addEventListener("click", function () {
      input.value = chip.getAttribute("data-msg");
      sendMessage();
    });
  });

  /* ---------- welcome message ---------------------------------------- */

  window.addEventListener("load", function () {
    addBotMsg(
      "Hello! I'm <strong>MediBot</strong>, your personal health " +
        "assistant. &#128075;<br><br>Tell me how you're feeling &mdash; " +
        'for example, <em>"I have a fever and a headache"</em> &mdash; ' +
        "or tap a quick option below to get started."
    );
  });
})();
